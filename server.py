import torndb
import os
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from binascii import hexlify

define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="ticketing", help="database name")
define("mysql_user", default="tick", help="database user")
define("mysql_password", default="tick", help="database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/login", Login),
            (r"/signup", Signup),
            (r"/logout", Logout),
            (r"/closeticket", CloseTicket),
            (r".*", DefaultHandler),

        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class DefaultHandler(BaseHandler):
    def get(self):
        pass


class Signup(BaseHandler):
    def post(self):
        username = self.get_query_argument('username')
        password = self.get_query_argument('password')
        firstname = self.get_query_argument('firstname', None)
        lastname = self.get_query_argument('lastname', None)
        type = self.get_query_argument('type')

        if self.db.get("SELECT * FROM users WHERE username=%s", username):
            msg = {'message': 'Username already exists!'}
            self.write(msg)
            return

        user = {'user': str(username), 'pass': str(password) ,
                'firstname': firstname, 'lastname': lastname, 'type': type}
        self.write(user)

        self.db.execute("INSERT INTO users (username, password, firstname, lastname, type) "
                        "VALUES (%s,%s,%s,%s,%s) ", username , password, firstname, lastname, type)


class Login(BaseHandler):
    def post(self):
        username = self.get_query_argument('username')
        password = self.get_query_argument('password')

        response = self.db.get("SELECT token FROM users WHERE username=%s AND password=%s",
                               username, password)

        if response:
            if response['token']:
                msg = {'message': 'Already logged in!'}
                self.write(msg)
                return

            token = str(hexlify(os.urandom(16)))
            self.db.execute("UPDATE users SET token=%s WHERE username=%s AND password=%s ",
                            token,username,password)

            msg = {'message': 'Logged in successfully!'}
            self.write(msg)

        else:
            msg = {'message': 'Wrong username/password pair!'}
            self.write(msg)
            return



class Logout(BaseHandler):
    def post(self):
        username = self.get_query_argument('username')
        password = self.get_query_argument('password')

        response = self.db.get("SELECT * FROM users WHERE username=%s AND password=%s",
                               username, password)

        if response:
            token = self.db.get("SELECT token FROM users WHERE username=%s AND password=%s",
                                username, password)

            if token['token']:
                self.db.execute("UPDATE users SET token=NULL WHERE username=%s AND password=%s ",
                                 username, password)
                msg = {'message': 'Logged out successfully!',
                       'token': str(token['token'])}

                self.write(msg)
            else:
                msg = {'message': 'Already Logged out!'}
                self.write(msg)
        else:
            msg = {'message': 'User doesn\'t exists!'}
            self.write(msg)


class CloseTicket(BaseHandler):
    def post(self):
        token = self.get_query_argument('token')
        ticket_id = self.get_query_argument('id')

        user = self.db.get("SELECT * FROM users WHERE token=%s", token)

        if not user:
            msg = {'message': 'Invalid token!'}
            self.write(msg)
            return

        ticket = self.db.get("SELECT * FROM tickets WHERE ticket_id=%s", ticket_id)

        if not ticket:
            msg = {'message': 'Invalid ticket id!'}
            self.write(msg)
            return

        if (ticket['user_id'] != user['user_id']):
            msg = {'message': 'Ticket belongs to another user, you can\'t change it!'}
            self.write(msg)
            return
        self.db.execute("UPDATE tickets SET status='Closed' WHERE ticket_id=%s", ticket_id)

        msg = {'message': 'Ticket closed successfully!'}
        self.write(msg)
        return


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


main()
