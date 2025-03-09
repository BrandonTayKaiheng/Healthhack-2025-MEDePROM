from database import dbcontext
from chatbot.llm_bot import Chatbot

if __name__ == "__main__":
    username = 'demo'
    password = 'demo'
    hostname = 'localhost'
    port = '1972'
    namespace = 'USER'

    db = dbcontext.DbContext(username, password, hostname, port, namespace)
    bot = Chatbot("AIzaSyATyT-nX1KfRx6x1tMoOAxXDYXOcji-yPE", db)

    print(bot.test())
