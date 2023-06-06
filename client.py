import threading

import grpc

import protos.my_pb2 as my_pb2
import protos.my_pb2_grpc as my_pb2_grpc

import pika
from rbmq.rbmq import RabbitMQClient, RabbitMQServer


class Client:
    def __init__(self):
        self.name = None
        self.game_name = None
        self.role = None
        self.user_id = 0
        self.connected_players = []
        self.stub = None
        self.rabbit_mq_listener = None
        self.rabbit_mq_writer = None
        self.game_channel = grpc.insecure_channel('localhost:8080')
        self.notifications_channel = grpc.insecure_channel('localhost:8080')

    def start_concuming(self):
        print("Start listening")
        self.rabbit_mq_listener.channel.start_consuming()

    def set_night(self, alive):
        print("NOW STAGE IS NIGHT")
        print("Alive players:", alive)
        if self.role == "killed" or self.role == "civilian":
            response = self.stub.SkipNight(my_pb2.SkipNightRequest(session=self.game_name))
        elif self.role == "mafia":
            self.rabbit_mq_listener = RabbitMQClient(self.game_name, self.user_id)
            print("If you want to chat with other mafia wtite w, else write k")
            command = input()
            if command == "w":
                th = threading.Thread(target=self.start_concuming, args=())
                th.start()
                print("for stop chating write s")
                self.rabbit_mq_writer = RabbitMQServer()
                while True:
                    texted = input()
                    if texted == 's':
                        break
                    else:
                        texted = texted.encode(encoding='UTF-8', errors='replace')
                        self.rabbit_mq_writer.channel.basic_publish(
                            exchange=f'chat_server',
                            routing_key='rpc_queue',
                            body=texted,
                            properties=pika.BasicProperties(
                                headers={'pid': str(self.user_id), 'session': str(self.game_name), 'time': 'night'}))
                        self.rabbit_mq_writer.deleted()
            print("Choose player to kill, write his id")
            name_to_deal = int(input())
            response = self.stub.KillPlayerMafia(my_pb2.KillPlayerMafiaRequest(session=self.game_name, id=name_to_deal))
        else:
            print("Choose player to check, write his id")
            name_to_deal = int(input())
            response = self.stub.CheckPlayer(my_pb2.CheckPlayerRequest(session=self.game_name, id=name_to_deal))
        print("NIGHT IS ENDED; RESULTS:\n")
        if self.role == "sherif" and response.checked_role:
            print(f'{name_to_deal} is {response.checked_role}')
        del alive[response.killed]
        print("Killed: ", response.killed)
        if self.user_id == response.killed:
            print("YOU WERE KILLED")
            self.role = "killed"
        if response.end_game:
            print("\nMafia won!\n")
            return
        self.set_day(alive)

    def set_day(self, alive):
        print("NOW STAGE IS DAY\n")
        if self.role == "killed":
            response = self.stub.EndDay(my_pb2.EndDayRequest(session=self.game_name, id=self.user_id))
            del alive[response.killed]
            self.set_night(alive)
        print("Alive players:", alive)
        self.rabbit_mq_listener = RabbitMQClient(self.game_name, self.user_id)
        print("If you want to chat with others write w, else write k")
        command = input()
        if command == "w":
            th = threading.Thread(target=self.start_concuming, args=())
            th.start()
            print("for stop chating write s")
            while True:
                self.rabbit_mq_writer = RabbitMQServer()
                texted = input()
                if texted == 's':
                    break
                else:
                    texted = texted.encode(encoding='UTF-8', errors='replace')
                    self.rabbit_mq_writer.channel.basic_publish(
                        exchange=f'chat_server',
                        routing_key='rpc_queue',
                        body=texted,
                        properties=pika.BasicProperties(headers={'pid': str(self.user_id), 'session': str(self.game_name), 'time': 'day'}))
                    self.rabbit_mq_writer.deleted()
        print("Choose player id to vote for him, write id")
        name_to_deal = int(input())
        self.stub.KillPlayerVote(my_pb2.KillVoteRequest(session=self.game_name, id=name_to_deal))
        print("Press any key to continue in all users")
        input()
        response = self.stub.EndDay(my_pb2.EndDayRequest(session=self.game_name, id=self.user_id))
        if response.end_game:
            print("\nCivilians won!\n")
            return
        del alive[response.killed]
        if self.user_id == response.killed:
            print("YOU WERE KILLED")
            self.role = "killed"
        self.set_night(alive)

    def get_notifications(self):
        stub = my_pb2_grpc.MafiaServerStub(self.notifications_channel)
        try:
            for event in stub.GetNotifications(my_pb2.NotificationsRequest(id=self.user_id, session=self.game_name)):
                if event.connected:
                    print("Connected:", event.user_name)
                    self.connected_players.append(event.user_name)
                else:
                    print("Disconnected:", event.user_name)
                    self.connected_players.remove(event.user_name)
        except Exception as e:
            print("ERROR")
            print(e)
        self.notifications_channel.close()

    def start(self):
        print("Enter your name")
        name_field = input()
        self.name = name_field
        stub = my_pb2_grpc.MafiaServerStub(self.game_channel)
        self.stub = stub
        print("Enter name (id) of the game")
        game_name = input()
        self.game_name = game_name
        response = stub.SetUserName(my_pb2.SetUserNameRequest(name=self.name, session=self.game_name))
        self.user_id = response.id
        self.connected_players = response.names
        th = threading.Thread(target=self.get_notifications, args=())
        th.start()
        while True:
            print("Type D - disconnect\nType L - list of online players\nType R - ready for play in this room")
            print("Only after 4 players press ready game will start")
            command = input()
            if command == 'D':
                self.stub.Disconnect(my_pb2.DisconnectRequest(session=self.game_name, id=self.user_id))
                break
            elif command == 'L':
                print(self.connected_players)
            elif command == 'R':
                response = self.stub.SetReadyStatus(my_pb2.ReadyRequest(session=self.game_name, id=self.user_id))
                print("Your role:", response.role)
                self.role = response.role
                self.set_day(dict(zip(response.ids, response.players)))
                break
            else:
                print("ERROR: NOT KNOWN COMMAND")
        self.game_channel.close()


if __name__ == '__main__':
    client = Client()
    client.start()
