from database import dbcontext
from model.model import Chatbot

if __name__ == "__main__":
    username = 'demo'
    password = 'demo'
    hostname = 'localhost'
    port = '1972'
    namespace = 'USER'

    db = dbcontext.DbContext(username, password, hostname, port, namespace)
    bot = Chatbot(db)

    r = bot.test()
    print(r)
