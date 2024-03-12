import datetime
import time
import stomp
import logging
import zlib
from django.conf import settings
from django.core.management.base import BaseCommand
import xsdata.formats.dataclass.context
import xsdata.formats.dataclass.parsers
import xsdata.formats.dataclass.serializers
import darwin.push_port.rtti_pptschema_v16
import darwin.tasks


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand, stomp.ConnectionListener):
    help = "Start a STOMP listener for Darwin data"

    connection: stomp.Connection
    xml_parser: xsdata.formats.dataclass.parsers.XmlParser
    dict_encoder: xsdata.formats.dataclass.serializers.DictEncoder

    def handle(self, *args, **options):
        logging.info("Connecting to Darwin STOMP server")
        self.connection = stomp.Connection(
            [(settings.DARWIN_MESSAGING_HOST, 61613)],
            heartbeats=(15000, 15000),
            auto_decode=False,
        )
        self.connection.set_listener("", self)
        self.connect_and_subscribe()

        self.xml_parser = xsdata.formats.dataclass.parsers.XmlParser()
        self.dict_encoder = xsdata.formats.dataclass.serializers.DictEncoder()

        while True:
            time.sleep(10)

    def connect_and_subscribe(self):
        self.connection.connect(
            username=settings.DARWIN_MESSAGING_USERNAME,
            passcode=settings.DARWIN_MESSAGING_PASSWORD,
            wait=True,
            **{
                "client-id": f"{settings.DARWIN_MESSAGING_USERNAME}_emf-bus-tracking_{settings.DARWIN_CLIENT_ID}"
            }
        )
        self.connection.subscribe("/topic/darwin.pushport-v16", id="1", ack="client-individual", **{
            "activemq.subscriptionName": f"emf-bus-tracking_{settings.DARWIN_CLIENT_ID}",
        })
        logging.info("STOMP connected")

    def on_message(self, frame):
        message_body = zlib.decompress(frame.body, zlib.MAX_WBITS | 32).decode("utf-8")
        push_port_message = self.xml_parser.from_string(message_body, darwin.push_port.rtti_pptschema_v16.Pport)

        message_dict = self.dict_encoder.encode(push_port_message)

        timestamp = datetime.datetime(
            year=push_port_message.ts.year,
            month=push_port_message.ts.month,
            day=push_port_message.ts.day,
            hour=push_port_message.ts.hour,
            minute=push_port_message.ts.minute,
            second=push_port_message.ts.second,
            microsecond=int(push_port_message.ts.fractional_second * 0.001),
            tzinfo=datetime.timezone(offset=datetime.timedelta(minutes=push_port_message.ts.offset)),
        )

        darwin.tasks.process_darwin_message.delay(
            sequence_number=int(frame.headers["SequenceNumber"]),
            message_type=frame.headers["MessageType"],
            timestamp=timestamp.timestamp(),
            message=message_dict
        )

        self.connection.ack(frame.headers["message-id"], "1")

    def on_error(self, frame):
        logging.error(f"STOP error {frame.body}")

    def on_disconnected(self):
        logging.warning("STOMP disconnected")
        time.sleep(30)
        self.connect_and_subscribe()

