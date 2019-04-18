import requests
import os
import platform
import time

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def login(username, password):
    PARAMS = {'username': username, 'password': password}
    response = requests.post("http://localhost:1104/login", PARAMS)
    data = response.json()
    return data


def logout(username, passowrd):
    PARAMS = {'username': username, 'password': passowrd}
    response = requests.post("http://localhost:1104/logout", PARAMS)
    data = response.json()
    print(data)


def signup(username, password, firstname, lastname, type):
    PARAMS = {'username': username, 'password': password,
              'firstname': firstname, 'lastname': lastname,
              'type': type
              }
    response = requests.post("http://localhost:1104/signup", PARAMS)
    data = response.json()
    print(data)

    return data


def logout(username, password):
    PARAMS = {'username': username, 'password': password}
    response = requests.post("http://localhost:1104/logout", PARAMS)
    data = response.json()
    print(data)


def send_ticket(token, subject, body):
    PARAMS = {'token': token, 'subject': subject, 'body': body}
    response = requests.post("http://localhost:1104/sendticket", PARAMS)
    data = response.json()
    print(data)
    return data


def change_status(token, ticket_id, status):
    PARAMS = {'token': token, 'id': ticket_id, 'status': status}
    response = requests.post("http://localhost:1104/changestatus", PARAMS)
    data = response.json()
    print(data)
    return data


def reply_to_ticket(token, ticket_id, reply):
    PARAMS = {'token': token, 'id': ticket_id, 'body': reply}
    response = requests.post("http://localhost:1104/restoticketmod", PARAMS)
    data = response.json()
    print(data)
    return data


def close_ticket_client(token, ticket_id):
    PARAMS = {'token': token, 'id': ticket_id}
    response = requests.post("http://localhost:1104/closeticket", PARAMS)
    data = response.json()
    print(data)
    return data


def client_list(username, password, token):
    while True:
        clear()
        print("Choose what to do:\n\t1.Send ticket\n\t2.Get sent tickets"
            "\n\t3.Close sent ticket\n\t4.Logout")

        op = int(input())
        if op == 1:
            clear()
            response = 400
            tikect_id = ""
            while not response == 200:
                subject = raw_input("Subject: ")
                body = raw_input("Write your message: ")

                data = send_ticket(token, subject, body)
                response = int(data['code'])
                
                if response == 200:
                    ticket_id = data['id']

                print(data['message'])


            if response == 200:
                print("Your ticket id is " + str(ticket_id) + "\n")
                raw_input("Press Enter to continue...")
        
        elif op == 2:
            pass
        
        elif op == 3:
            clear()
            response = 400
            while not response == 200:
                ticket_id = raw_input("Enter your ticket id: ")

                data = close_ticket_client(token, ticket_id)
                response = int(data['code'])
                print(data['message'] + "\n")

            if response == 200:
                raw_input("Press Enter to continue...")

        elif op == 4:
            logout(username, password)
            return
    


def admin_list(username, password, token):
    while True:
        clear()
        print("Choose what to do:\n\t1.Reply to tikcets\n\t2.Get sent tickets"
            "\n\t3.Change tickets status\n\t4.Logout")

        op = int(input())
        if op == 1:
            clear()
            response = 400
            while not response == 200:
                ticket_id = raw_input("Enter ticket id: ")
                reply = raw_input("Write reply to ticket: ")

                data = reply_to_ticket(token, ticket_id, reply)
                response = int(data['code'])
                print(data['message'] + "\n")

            if response == 200:
                raw_input("Press Enter to continue...")
        
        elif op == 2:
            pass
        
        elif op == 3:
            clear()
            response = 400
            status = ""
            while not response == 200:
                ticket_id = raw_input("Enter ticket id: ")
                status = raw_input("Enter new status: ")

                data = change_status(token, ticket_id, status)
                response = int(data['code'])
                print(data['message'])

            if response == 200:
                print("New status is '" + status.title() + "'.\n")
                raw_input("Press Enter to continue...")

        elif op == 4:
            logout(username, password)
            return

def main_loop():
    exit = False
    while not exit:
        clear()
        print("Choose what to do:\n\t1.Signup\n\t2.Login\n\t3.Exit")
        op = int(input())

        if op == 1:
            clear()
            response = 400
            while not response == 200:
                print("Enter Username: ")
                username = raw_input()

                print("Enter Password: ")
                password = raw_input()

                print("Enter your firstname(optional, press enter to pass): ")
                firstname = raw_input()
                if not firstname:
                    firstname=None
                print("Enter your lastname(optional, press enter to pass): ")
                lastname = raw_input()
                if not lastname:
                    lastname = None

                print("Sign up as a client(c) or admin(a): ")
                type = str(raw_input()).lower()

                data = signup(username, password, firstname, lastname, type)
                response = int(data['code'])
                print(data['message'] + "\n")

            if response == 200:
                raw_input("Press Enter to continue...")

        elif op == 2:
            clear()
            response = 400
            token = ""
            username = ""
            password = ""
            user_type = ""
            logged_in = False
            while not (response == 200 or response == 202):
                print("Enter Username: ")
                username = raw_input()

                print("Enter Password: ")
                password = raw_input()

                data = login(username, password)
                response = int(data['code'])
                print(data['message'])
                if response == 200 or response == 202:
                    token = data['token']
                    user_type = data['type']
                    logged_in = True

                print("\n")

            if logged_in:
                secondary_loop(username, password, token, user_type)

        elif op == 3:
            exit = True


def secondary_loop(username, password, token, user_type):
    print(token)

    if user_type == 'c':
        client_list(username, password, token)

    if user_type == 'a':
        admin_list(username, password, token)


main_loop()
