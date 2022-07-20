from configurations.RabbitMqServerConfigure import RabbitMqServerConfigure
from src.RabbitMqServer import RabbitMqServer

server_configure = RabbitMqServerConfigure(host='localhost', queue='student_data')
rabbitmq_server = RabbitMqServer(server=server_configure)
rabbitmq_server.start_server()
