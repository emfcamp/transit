import dataclasses
import typing
import datetime
import Crypto.Cipher.AES


@dataclasses.dataclass
class Track24Message:
    message_type: int
    data: bytes

    @classmethod
    def from_bytes(cls, data: bytes, aes_key: typing.Optional[bytes]) -> "Track24Message":
        if aes_key:
            cipher = Crypto.Cipher.AES.new(aes_key, Crypto.Cipher.AES.MODE_ECB)
            data = cipher.decrypt(data)

            message_type = data[0]
            padding_bytes = min(data[1], 16)
            data = data[2:-padding_bytes]

            return cls(
                message_type=message_type,
                data=data
            )
        else:
            return cls(
                message_type=data[0],
                data=data[1:]
            )


@dataclasses.dataclass
class GPSData:
    latitude: float
    longitude: float
    timestamp: datetime.time
    velocity_knots: int
    heading: int
    panic: bool

    @classmethod
    def from_message(cls, msg: Track24Message) -> "GPSData":
        latitude = (int.from_bytes(msg.data[0:3], "big") & 0x7fffff) / 60000.0
        longitude = int.from_bytes(msg.data[3:6], "big") / 60000.0

        velocity = msg.data[6]
        heading = int(((msg.data[7] & 0b00000111) - 0.5) * 45.0)

        latitude_negative = bool(msg.data[7] & 0b00001000)
        longitude_negative = bool(msg.data[7] & 0b00010000)
        panic = bool(msg.data[7] & 0b00100000)
        _bool1 = bool(msg.data[7] & 0b01000000)
        _bool2 = bool(msg.data[7] & 0b10000000)

        seconds_since_midnight = int.from_bytes(msg.data[8:10], "big")
        seconds_since_midnight_bit_17 = bool(msg.data[0] & 0b10000000)

        if seconds_since_midnight_bit_17:
            seconds_since_midnight += 0x10000

        timestamp = (datetime.datetime.min + datetime.timedelta(seconds=seconds_since_midnight)).time()

        if latitude_negative:
            latitude = -latitude
        if longitude_negative:
            longitude = -longitude

        return cls(
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp,
            velocity_knots=velocity,
            heading=heading,
            panic=panic,
        )
