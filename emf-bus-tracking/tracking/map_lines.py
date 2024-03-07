import collections
import shapely
import typing
import enum
import scipy.spatial
import heapq


MAX_LEN = 0.0001


class EdgeDirection(enum.Enum):
    FORWARD = 0
    BACKWARD = 1


EdgeProperties = collections.namedtuple("EdgeProperties", ["id", "data"])
PathEdge = collections.namedtuple("PathEdge", ["source_point", "target_point", "direction", "data"])
LinePart = collections.namedtuple("LinePart", ["line", "direction", "data"])


class GraphEdge:
    def __init__(self, point: shapely.Point, length: float, direction: EdgeDirection, data: EdgeProperties):
        self.point = point
        self.direction = direction
        self.length = length
        self.data = data


class DijkstraNode:
    def __init__(self, point: shapely.Point, current_distance: float):
        self.point = point
        self.distance = current_distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __eq__(self, other):
        return self.distance == other.distance

    def __gt__(self, other):
        return self.distance > other.distance


class Graph:
    nodes: typing.Set[shapely.Point]
    edges: typing.Dict[shapely.Point, typing.List[GraphEdge]]

    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def __len__(self):
        return len(self.nodes)

    def get_nodes(self) -> typing.List[shapely.Point]:
        return list(self.nodes)

    def add_point(self, point: shapely.Point):
        if point in self.nodes:
            return

        self.nodes.add(point)

    def add_edge(
            self,
            a: shapely.Point, b: shapely.Point,
            length: float,
            data: EdgeProperties,
            forward_direction: bool = True,
            backward_direction: bool = True
    ):
        self.add_point(a)
        self.add_point(b)

        if a not in self.edges:
            self.edges[a] = []
        if b not in self.edges:
            self.edges[b] = []

        if forward_direction:
            self.edges[a].append(GraphEdge(
                b, length, EdgeDirection.FORWARD, data
            ))
        if backward_direction:
            self.edges[b].append(GraphEdge(
                a, length, EdgeDirection.BACKWARD, data
            ))

    def _dijkstra(self, start_node: shapely.Point):
        distances = {node: float('infinity') for node in self.get_nodes()}
        distances[start_node] = 0
        previous_nodes = {}

        pq = [DijkstraNode(start_node, 0.0)]
        while len(pq) > 0:
            current_node = heapq.heappop(pq)

            if current_node.distance > distances[current_node.point]:
                continue

            edges = self.edges[current_node.point]
            for edge in edges:
                new_distance = current_node.distance + edge.length

                if new_distance < distances[edge.point]:
                    distances[edge.point] = new_distance
                    previous_nodes[edge.point] = (current_node.point, edge.data, edge.direction)
                    heapq.heappush(pq, DijkstraNode(edge.point, new_distance))

        return previous_nodes

    @staticmethod
    def _dijkstra_path(
            previous_nodes: typing.Dict[shapely.points, typing.Tuple[shapely.Point, EdgeProperties, EdgeDirection]],
            start_node: shapely.Point, end_node: shapely.Point
    ):
        if end_node not in previous_nodes:
            return None

        path = []
        node, edge, direction = previous_nodes[end_node]
        path.append(PathEdge(
            source_point=node, target_point=end_node,
            data=edge, direction=direction
        ))

        while node != start_node:
            if node not in previous_nodes:
                return None
            prev_node = node
            node, edge, direction = previous_nodes[node]
            path.append(PathEdge(
                source_point=node, target_point=prev_node,
                data=edge, direction=direction
            ))

        return path[::-1]

    def shortest_path(self, start_node: shapely.Point, end_node: shapely.Point) -> typing.List[PathEdge]:
        previous_nodes = self._dijkstra(start_node)
        return self._dijkstra_path(previous_nodes, start_node, end_node)

    def connected_components(self) -> typing.List["Graph"]:
        unvisited = set(self.nodes)
        components = []

        while unvisited:
            component = []
            stack = [list(unvisited)[0]]
            while stack:
                current_node = stack.pop()
                if current_node not in unvisited:
                    continue
                unvisited.remove(current_node)
                component.append((current_node, self.edges[current_node]))
                for edge in self.edges[current_node]:
                    stack.append(edge.point)

            component_graph = Graph()
            for node, edges in component:
                component_graph.nodes.add(node)
                component_graph.edges[node] = edges

            components.append(component_graph)

        return components

    def largest_connected_component(self) -> "Graph":
        components = self.connected_components()
        return max(components, key=len)


def search_start_end_points(graph: Graph, search_path: shapely.LineString):
    path_start = search_path.coords[0]
    path_end = search_path.coords[-1]

    graph_nodes = graph.get_nodes()
    graph_kd_tree = scipy.spatial.KDTree([(p.x, p.y) for p in graph_nodes])
    graph_start_idx = graph_kd_tree.query((path_start[0], path_start[1]))[1]
    graph_end_idx = graph_kd_tree.query((path_end[0], path_end[1]))[1]
    graph_start = graph_nodes[graph_start_idx]
    graph_end = graph_nodes[graph_end_idx]

    return graph_start, graph_end


def find_matching_graph_path(graph: Graph, search_path: shapely.LineString) -> typing.List[PathEdge]:
    graph_start_point, graph_end_point = search_start_end_points(graph, search_path)
    return graph.shortest_path(graph_start_point, graph_end_point)


def line_slope(line: shapely.LineString) -> float:
    return 0 if (line.coords[-1][0] - line.coords[0][0]) == 0 else \
        (line.coords[-1][1] - line.coords[0][1]) / \
        (line.coords[-1][0] - line.coords[0][0])


def coalesce_line_parts(
        line_parts: typing.List[LinePart], is_same: typing.Callable, simplify: bool = False
) -> typing.List[LinePart]:
    coalesced_path_line_parts = [line_parts[0]]
    for part in line_parts[1:]:
        prev_part = coalesced_path_line_parts[-1]

        if is_same(prev_part, part):
            if simplify:
                line = shapely.LineString([prev_part.line.coords[0], part.line.coords[-1]])
            else:
                line = shapely.LineString(list(prev_part.line.coords) + list(part.line.coords)[1:])
            coalesced_path_line_parts[-1] = LinePart(
                line=line, data=prev_part.data, direction=prev_part.direction
            )
        else:
            coalesced_path_line_parts.append(part)

    return coalesced_path_line_parts


def coalesce_step_1(prev_part: LinePart, cur_part: LinePart):
    prev_part_slope = round(line_slope(prev_part.line), 3)
    cur_part_slope = round(line_slope(cur_part.line), 3)

    prev_part_id = prev_part.data.id
    cur_part_id = cur_part.data.id

    return prev_part_slope == cur_part_slope and prev_part_id == cur_part_id


def coalesce_step_2(prev_part: LinePart, cur_part: LinePart):
    return prev_part.data.id == cur_part.data.id


def map_properties(graph_path: typing.List[PathEdge], search_path: shapely.LineString) -> typing.List[LinePart]:
    graph_line_parts = []
    graph_line_points = []
    for part in graph_path[1:]:
        line = shapely.LineString([part.source_point, part.target_point]).segmentize(MAX_LEN)
        for i, point in enumerate(line.coords):
            if i == 0:
                continue
            line_part = shapely.LineString([line.coords[i - 1], point])
            graph_line_parts.append(LinePart(
                line=line_part,
                data=part.data,
                direction=part.direction
            ))
        graph_line_points.extend(list(line.coords)[1:])

    graph_line_kd_tree = scipy.spatial.KDTree(graph_line_points)

    search_path_parts = []
    search_path = search_path.segmentize(MAX_LEN)
    for i, part in enumerate(search_path.coords[1:]):
        search_path_parts.append(shapely.LineString([search_path.coords[i], part]))

    annotated_search_line_parts = []
    for i, part in enumerate(search_path_parts):
        nearest_points_start = []
        nearest_points_end = []
        r = MAX_LEN * 2
        while not nearest_points_start:
            nearest_points_start = graph_line_kd_tree.query_ball_point((part.coords[0][0], part.coords[0][1]), r=r)
            r += MAX_LEN
        r = MAX_LEN * 2
        while not nearest_points_end:
            nearest_points_end = graph_line_kd_tree.query_ball_point((part.coords[-1][0], part.coords[-1][1]), r=r)
            r += MAX_LEN

        line_candidates = []
        for j in nearest_points_start:
            if j >= len(graph_line_parts):
                continue
            line_candidates.append(graph_line_parts[j])
        for j in nearest_points_end:
            if j == 1 or (j - 1) >= len(graph_line_parts):
                continue
            line_candidates.append(graph_line_parts[j - 1])

        min_distance = float('inf')
        min_line = None
        for line in line_candidates:
            candidate_distance = shapely.hausdorff_distance(part, line.line, densify=0.5)
            if candidate_distance < min_distance:
                min_distance = candidate_distance
                min_line = line

        annotated_search_line_parts.append(LinePart(
            line=part, data=min_line.data, direction=min_line.direction
        ))

    coalesced_search_line_parts = coalesce_line_parts(
        coalesce_line_parts(annotated_search_line_parts, coalesce_step_1, simplify=True),
        coalesce_step_2, simplify=False
    )

    return [LinePart(
        line=part.line, direction=part.direction, data=part.data.data
    ) for part in coalesced_search_line_parts]
