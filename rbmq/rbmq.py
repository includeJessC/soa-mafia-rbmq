import grpc
import pika

import protos.my_pb2 as my_pb2
import protos.my_pb2_grpc as my_pb2_grpc


class RabbitMQClient(object):
    def __init__(self, session_name, user_name):
        self.session_name = session_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0', port=5672))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=f'chat_{session_name}_{user_name}', exchange_type='fanout')
        result = self.channel.queue_declare(queue=f'chat_{session_name}_{user_name}')
        self.callback_queue = result.method.queue
        self.channel.queue_bind(exchange=f'chat_{session_name}_{user_name}', queue=self.callback_queue)
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def deleted(self):
        try:
            self.channel.close()
            self.connection.close()
        except:
            pass

    def on_response(self, ch, method, props, body):
        print(body.decode(encoding='UTF-8', errors='replace'))


class RabbitMQServer(object):
    def __init__(self, host_default='0.0.0.0'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host_default, port=5672))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=f'chat_server', exchange_type='fanout')
        result = self.channel.queue_declare(queue='chat_server')
        self.callback_queue = result.method.queue
        self.channel.queue_bind(exchange=f'chat_server', queue=self.callback_queue)

    def deleted(self):
        try:
            self.channel.close()
            self.connection.close()
        except:
            pass


def main():
    stub = None
    while stub is None:
        try:
            grpc_channel = grpc.insecure_channel('server:8080')
            stub = my_pb2_grpc.MafiaServerStub(grpc_channel)
            stub.GetConnectedPlayers(my_pb2.SessionName(session=''))
        except:
            print("cannot connect")
            stub = None
            pass
    server = RabbitMQServer('rabbitmq')

    def on_response(ch, method, props, body):
        pid = int(props.headers['pid'])
        session = props.headers['session']
        now_time = props.headers['time']
        if now_time == 'day':
            response = list(stub.GetConnectedPlayers(my_pb2.SessionName(session=session)).names)
        else:
            response = list(stub.GetMafiaPlayers(my_pb2.SessionName(session=session)).names)
        for value in response:
            if value == str(pid):
                continue
            server.channel.queue_declare(f'chat_{session}_{value}')
            server.channel.basic_publish(f'chat_{session}_{value}', routing_key='rpc_queue', body=body)

    server.channel.basic_consume(
        queue=server.callback_queue,
        on_message_callback=on_response,
        auto_ack=True)
    server.channel.start_consuming()

if __name__ == '__main__':
    main()