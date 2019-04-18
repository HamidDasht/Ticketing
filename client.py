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

def client_list(username, password, token):
    print("Choose what to do:\n\t1.Send ticket\n\t2.Get sent tickets"
          "\n\t3.Close sent ticket\n\t4.Logout")

    op = int(input())
    if op == 4:
        logout(username, password)
        return

def admin_list(username, password, token):
    print("Choose what to do:\n\t1.Response to tikcets\n\t2.Get sent tickets"
          "\n\t3.Change tickets status\n\t4.Logout")

    op = int(input())
    if op == 4:
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
                print(data['message'])

                print("")

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

                print("")

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

    raw_input()


main_loop()
