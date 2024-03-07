import enum
import datetime
import abc
import typing


class NALException(Exception):
    pass


class Fix(enum.Enum):
    Other = enum.auto()
    NoFix = enum.auto()
    TimeOnly = enum.auto()
    DeadReckoning = enum.auto()
    GpsAndDeadReckoning = enum.auto()
    TwoDimensional = enum.auto()
    ThreeDimensional = enum.auto()
    ValidThreeDimensional = enum.auto()


class NALReport(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def latitude(self) -> float:
        pass

    @abc.abstractmethod
    def longitude(self) -> float:
        pass

    @abc.abstractmethod
    def velocity_ms(self) -> typing.Optional[float]:
        pass

    @abc.abstractmethod
    def heading(self) -> typing.Optional[float]:
        pass

    @abc.abstractmethod
    def time(self) -> typing.Optional[datetime.time]:
        pass

    @classmethod
    def parse(cls, data: bytes) -> 'NALReport':
        if len(data) == 10:
            return NAL10ByteReport.parse(data)
        elif len(data) >= 30:
            report_type = data[0]
            # 3 - 7 are defined report types, only 6 is implemented
            if report_type == 0x06:
                return NALReport6.parse(data)
            else:
                raise NALException(f"Unknown report type {report_type}")
        else:
            raise NALException("Unknown report type")


class NAL10ByteReport(NALReport):
    _latitude: float
    _longitude: float
    _timestamp: datetime.time
    _fix: Fix
    _pdop: int
    _motion: bool
    _emergency: bool
    _emergency_acknowledged: bool

    def __init__(
            self,
            longitude: float,
            latitude: float,
            timestamp: datetime.time,
            fix: Fix,
            pdop: int,
            motion: bool,
            emergency: bool,
            emergency_acknowledged: bool,
    ):
        self._latitude = latitude
        self._longitude = longitude
        self._timestamp = timestamp
        self._fix = fix
        self._pdop = pdop
        self._motion = motion
        self._emergency = emergency
        self._emergency_acknowledged = emergency_acknowledged

    def latitude(self) -> float:
        return self._latitude

    def longitude(self) -> float:
        return self._longitude

    def velocity_ms(self) -> typing.Optional[float]:
        return None

    def heading(self) -> typing.Optional[float]:
        return None

    def time(self) -> typing.Optional[datetime.time]:
        return self._timestamp

    def __str__(self):
        return (f"NAL10ByteReport("
                f"position=({self._latitude:.5f}, {self._longitude:.5f}), "
                f"timestamp={self._timestamp.isoformat()}, "
                f"fix={self._fix}, "
                f"pdop={self._pdop}, "
                f"motion={self._motion}, "
                f"emergency={self._emergency}, "
                f"emergency_acknowledged={self._emergency_acknowledged}"
                f")")

    @classmethod
    def parse(cls, data: bytes) -> 'NAL10ByteReport':
        if len(data) != 10:
            raise NALException("Unexpected report length")

        report_type = extract_bits(data, 0, 4)
        if report_type != 0b0000:
            raise NALException("Unexpected report type")

        lat_raw = extract_bits(data, 4, 25)
        long_raw = extract_bits(data, 29, 25)
        seconds = extract_bits(data, 55, 17)
        pdop_index = extract_bits(data, 72, 4)
        bits = extract_bits(data, 76, 4)

        if lat_raw > 18000000:
            raise NALException("Invalid latitude value")
        if long_raw > 36000000:
            raise NALException("Invalid longitude value")
        if seconds >= 86400:
            raise NALException("Invalid seconds value")
        if pdop_index >= 8:
            raise NALException("Invalid PDOP value")

        latitude = (lat_raw - 9000000) / 100000
        longitude = (long_raw - 18000000) / 100000

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        pdop = [1, 2, 5, 10, 20, 40, 70, 100][pdop_index]

        fix = Fix.ValidThreeDimensional if bool(bits & 0b0001) else Fix.NoFix
        emergency = bool(bits & 0b0010)
        emergency_acknowledged = bool(bits & 0b0100)
        motion = bool(bits & 0b1000)

        return cls(
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.time(hour=hours, minute=minutes, second=seconds),
            pdop=pdop,
            fix=fix,
            emergency=emergency,
            emergency_acknowledged=emergency_acknowledged,
            motion=motion,
        )


class NALReport6(NALReport):
    _latitude: float
    _longitude: float
    _timestamp: typing.Optional[datetime.datetime]
    _altitude: float
    _ground_velocity: float
    _course: float
    _vertical_velocity: float
    _fix: Fix
    _satellites: int
    _hdop: float
    _vdop: float
    _motion: bool
    _emergency: bool
    _emergency_acknowledged: bool
    _address_book_code: int
    _canned_message_code: int
    _text: typing.Optional[str]
    _emails: typing.List[str]

    def __init__(
            self,
            latitude: float,
            longitude: float,
            timestamp: typing.Optional[datetime.datetime],
            altitude: float,
            ground_velocity: float,
            course: float,
            vertical_velocity: float,
            fix: Fix,
            satellites: int,
            hdop: float,
            vdop: float,
            motion: bool,
            emergency: bool,
            emergency_acknowledged: bool,
            address_book_code: int,
            canned_message_code: int,
            text: typing.Optional[str],
            emails: typing.List[str],
    ):
        self._latitude = latitude
        self._longitude = longitude
        self._timestamp = timestamp
        self._altitude = altitude
        self._ground_velocity = ground_velocity
        self._course = course
        self._vertical_velocity = vertical_velocity
        self._fix = fix
        self._satellites = satellites
        self._hdop = hdop
        self._vdop = vdop
        self._motion = motion
        self._emergency = emergency
        self._emergency_acknowledged = emergency_acknowledged
        self._address_book_code = address_book_code
        self._canned_message_code = canned_message_code
        self._text = text
        self._emails = emails

    def latitude(self) -> float:
        return self._latitude

    def longitude(self) -> float:
        return self._longitude

    def velocity_ms(self) -> typing.Optional[float]:
        return self._ground_velocity

    def heading(self) -> typing.Optional[float]:
        return self._course

    def time(self) -> typing.Optional[datetime.time]:
        return self._timestamp.time() if self._timestamp else None

    def __str__(self):
        return (f"NALReport6("
                f"position=({self._latitude:.5f}, {self._longitude:.5f}), "
                f"timestamp={self._timestamp.isoformat() if self._timestamp else None}, "
                f"altitude={self._altitude}, "
                f"ground_velocity={self._ground_velocity}, "
                f"course={self._course}, "
                f"vertical_velocity={self._vertical_velocity}, "
                f"fix={self._fix}, "
                f"satellites={self._satellites}, "
                f"hdop={self._hdop}, "
                f"vdop={self._vdop}, "
                f"motion={self._motion}, "
                f"emergency={self._emergency}, "
                f"emergency_acknowledged={self._emergency_acknowledged}, "
                f"address_book_code={self._address_book_code}, "
                f"canned_message_code={self._canned_message_code}, "
                f"text=\"{self._text}\", "
                f"emails={self._emails}"
                f")")

    @classmethod
    def parse(cls, data: bytes) -> 'NALReport6':
        if len(data) < 30:
            raise NALException("Unexpected report length")

        if data[0] != 0x06:
            raise NALException("Unexpected report type")

        address_book_code = data[1]

        n1 = int.from_bytes(data[2:10], "little")
        n2 = int.from_bytes(data[10:18], "little")
        n3 = int.from_bytes(data[18:26], "little")
        num1 = int.from_bytes(data[26:28], "little")

        num2 = data[28]
        bitfield1 = data[29]

        lat_sign, n1 = divmod(n1, 10000000000000000000)
        lat_sign = lat_sign == 1
        long_deg, n1 = divmod(n1, 10000000000000000)
        long_min, n1 = divmod(n1, 100000000000000)
        long_min_ten_thousandths, n1 = divmod(n1, 10000000000)
        lat_deg, n1 = divmod(n1, 100000000)
        lat_min, n1 = divmod(n1, 1000000)
        lat_min_ten_thousandths, hdop_raw1 = divmod(n1, 100)

        vert_vel_sign, n2 = divmod(n2, 10000000000000000000)
        vert_vel_sign = vert_vel_sign != 1
        hour, n2 = divmod(n2, 100000000000000000)
        vdop_raw, n2 = divmod(n2, 10000000000000)
        year, n2 = divmod(n2, 1000000000)
        minute, n2 = divmod(n2, 10000000)
        second, n2 = divmod(n2, 100000)
        milisecond, n2 = divmod(n2, 10000)
        vert_vel_tenths, hdop_raw2 = divmod(n2, 100)

        alt_sign, n3 = divmod(n3, 10000000000000000000)
        alt_sign = alt_sign == 1
        course_raw, n3 = divmod(n3, 100000000000000)
        alt_exp, n3 = divmod(n3, 10000000000000)
        alt_mant, n3 = divmod(n3, 100000000)
        ground_vel_exp, n3 = divmod(n3, 10000000)
        ground_vel_mant, canned_message_code = divmod(n3, 100)

        month = num1 // 1000
        day = (num1 % 1000) // 10
        vert_vel_tens = num1 % 10
        satellites = num2 // 10
        vert_vel_hundreds = num2 % 10
        fix_flag2 = (bitfield1 & 1) > 0
        has_emails = (bitfield1 & 2) > 0
        fix_flag1 = (bitfield1 & 4) > 0
        has_text = (bitfield1 & 8) > 0
        emergency = (bitfield1 & 16) > 0
        motion = (bitfield1 & 32) > 0
        emergency_acknowledged = (bitfield1 & 64) > 0

        if long_deg < 200:
            long_sign = False
        else:
            long_sign = True
            long_deg -= 200

        time = datetime.datetime(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second,
            microsecond=milisecond * 1000, tzinfo=datetime.timezone.utc
        ) if (year != 0 and month != 0 and day != 0) else None
        latitude = (lat_deg + (lat_min + (lat_min_ten_thousandths / 10000.0)) / 60.0) * (-1 if lat_sign else 1)
        longitude = (long_deg + (long_min + (long_min_ten_thousandths / 10000.0)) / 60.0) * (-1 if long_sign else 1)
        altitude = alt_mant / 10 ** (5 - alt_exp) * (-1 if alt_sign else 1.0)
        ground_velocity = ground_vel_mant / 10 ** (5 - ground_vel_exp)
        course = course_raw / 100.0
        vertical_velocity = ((vert_vel_hundreds * 100 + vert_vel_tens * 10) + vert_vel_tenths / 10.0) \
            * (-1 if vert_vel_sign else 1)
        hdop = hdop_raw1 + hdop_raw2 / 100.0
        vdop = vdop_raw / 100.0
        fix = Fix.ValidThreeDimensional if fix_flag1 else (Fix.TwoDimensional if fix_flag2 else Fix.Other)

        emails = []
        text = None

        index = 30
        if has_emails and index + 1 <= len(data):
            n = data[index]
            index += 1
            if (n & 1) != 0 and index + 1 <= len(data):
                emails_length = data[index]
                index += 1
                if index + emails_length <= len(data):
                    d = data[index:index + emails_length].decode('cp1252')
                    emails.extend(d.split(","))
                    index += emails_length

        if has_text:
            text = data[index:].decode('cp1252').strip('\r')

        return cls(
            address_book_code=address_book_code,
            canned_message_code=canned_message_code,
            satellites=satellites,
            emergency=emergency,
            motion=motion,
            emergency_acknowledged=emergency_acknowledged,
            timestamp=time,
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            ground_velocity=ground_velocity,
            course=course,
            vertical_velocity=vertical_velocity,
            hdop=hdop,
            vdop=vdop,
            fix=fix,
            text=text,
            emails=emails,
        )


def extract_bits(data: bytes, start: int, amount: int) -> int:
    value = 0
    num = start + amount
    for index in range(start, num):
        if (data[index // 8] & (1 << (index % 8))) != 0:
            value += (1 << (index - start))
    return value
