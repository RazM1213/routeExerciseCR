import json
import os.path

from configurations.RabbitMqServerConfigure import RabbitMqServerConfigure
import pika
from models.Payload import Payload
from proj_utils.Validator import Validator
from proj_utils.Parser import Parser


class RabbitMqServer:
    def __init__(self, server: RabbitMqServerConfigure):
        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)
        print("Server started...")
        print("[X] Waiting for data...")

    @staticmethod
    def callback(ch, method, properties, body):
        string_body = body.decode('utf-8')
        RabbitMqServer.validation_process(string_body)

    @staticmethod
    def validation_process(string_body):
        try:
            validator = Validator(string_body)
            if validator.is_valid_schema:
                json_body = json.loads(string_body)
                if validator.is_valid_fields():
                    if validator.is_valid_values(json_body):
                        RabbitMqServer.parse_to_text_file(string_body)
                else:
                    print("Invalid field detected !")
            else:
                print("Invalid schema detected !")
        except json.decoder.JSONDecodeError:
            print("Body cant be decoded to JSON format !")

    @staticmethod
    def parse_to_text_file(string_body):
        payload = Payload(string_body)
        parser = Parser(payload)
        parser.populate_json_object()
        print(f"[X] Data Received for: {parser.jsonObject['studentDetails']['fullName']}")
        parser.create_text_file()
        print("[X] Done !")

    def start_server(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=RabbitMqServer.callback,
            auto_ack=True
        )
        self._channel.start_consuming()


if __name__ == "__main__":
    server_configure = RabbitMqServerConfigure(host='localhost', queue='student_data')
    rabbitmq_server = RabbitMqServer(server=server_configure)
    rabbitmq_server.start_server()
