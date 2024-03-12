import enum


class Days(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ServiceCategory(enum.Enum):
    METRO = "metro"
    UNADVERTISED_ORDINARY_PASSENGER = "unadvertised_ordinary_passenger"
    ORDINARY_PASSENGER = "ordinary_passenger"
    STAFF_TRAIN = "staff_train"
    MIXED = "mixed"
    CHANNEL_TUNNEL = "channel_tunnel"
    INTERNATIONAL_SLEEPER = "international_sleeper"
    DOMESTIC_SLEEPER = "domestic_sleeper"
    INTERNATIONAL = "international"
    MOTORAIL = "motorail"
    UNADVERTISED_EXPRESS_PASSENGER = "unadvertised_express_passenger"
    EXPRESS_PASSENGER = "express_passenger"
    REPLACEMENT_BUS = "replacement_bus"
    BUS = "bus"
    SHIP = "ship"
    TRAM = "tram"

    EMPTY_COACHING_STOCK = "empty_coaching_stock"
    METRO_EMPTY_COACHING_STOCK = "metro_empty_coaching_stock"
    STAFF_EMPTY_COACHING_STOCK = "staff_empty_coaching_stock"

    def name(self):
        if self == ServiceCategory.METRO:
            return "Metro"
        elif self == ServiceCategory.UNADVERTISED_ORDINARY_PASSENGER:
            return "Unadvertised Ordinary Passenger"
        elif self == ServiceCategory.ORDINARY_PASSENGER:
            return "Ordinary Passenger"
        elif self == ServiceCategory.STAFF_TRAIN:
            return "Staff Train"
        elif self == ServiceCategory.MIXED:
            return "Mixed"
        elif self == ServiceCategory.CHANNEL_TUNNEL:
            return "Channel Tunnel"
        elif self == ServiceCategory.INTERNATIONAL_SLEEPER:
            return "International Sleeper"
        elif self == ServiceCategory.DOMESTIC_SLEEPER:
            return "Domestic Sleeper"
        elif self == ServiceCategory.INTERNATIONAL:
            return "International"
        elif self == ServiceCategory.MOTORAIL:
            return "Motorail"
        elif self == ServiceCategory.UNADVERTISED_EXPRESS_PASSENGER:
            return "Unadvertised Express Passenger"
        elif self == ServiceCategory.EXPRESS_PASSENGER:
            return "Express Passenger"
        elif self == ServiceCategory.REPLACEMENT_BUS:
            return "Replacement Bus"
        elif self == ServiceCategory.BUS:
            return "Bus"
        elif self == ServiceCategory.SHIP:
            return "Ship"
        elif self == ServiceCategory.TRAM:
            return "Tram"
        elif self == ServiceCategory.EMPTY_COACHING_STOCK:
            return "Empty Coaching Stock"
        elif self == ServiceCategory.METRO_EMPTY_COACHING_STOCK:
            return "Empty Coaching Stock (Metro)"
        elif self == ServiceCategory.STAFF_EMPTY_COACHING_STOCK:
            return "Empty Coaching Stock (Staff)"
