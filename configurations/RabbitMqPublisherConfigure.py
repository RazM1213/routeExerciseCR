class RabbitMqPublisherConfigure:

    def __init__(self, queue='students', host='localhost', routingKey='students.data', exchange='student'):
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange
