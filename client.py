import threading

import grpc

import protos.my_pb2 as my_pb2
import protos.my_pb2_grpc as my_pb2_grpc


class Client:
    def __init__(self):
        self.name = None
        self.game_name = None
        self.role = None
        self.user_id = 0
        self.connected_players = []
        self.stub = None
        self.game_channel = grpc.insecure_channel('localhost:8080')
        self.notifications_channel = grpc.insecure_channel('localhost:8080')

    def set_night(self, alive):
        print("NOW STAGE IS NIGHT")
        print("Alive players:", alive)
        if self.role == "killed" or self.role == "civilian":
            response = self.stub.SkipNight(my_pb2.SkipNightRequest(session=self.game_name))
        elif self.role == "mafia":
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
