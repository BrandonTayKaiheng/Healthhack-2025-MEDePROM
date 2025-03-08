from database import dbcontext

if __name__ == "__main__":
    username = 'demo'
    password = 'demo'
    hostname = 'localhost'
    port = '1972'
    namespace = 'USER'

    db = dbcontext.DbContext(username, password, hostname, port, namespace)
    db.retrieve_data(1, "SQLUser.ePROM_DB")
