from database import dbcontext

if __name__ == "__main__":
    username = 'demo'
    password = 'demo'
    hostname = 'localhost'
    port = '1972'
    namespace = 'USER'

    db = dbcontext.DbContext(username, password, hostname, port, namespace)
    print(db.get_all_questions())
    print(db.get_question_options(1))
    print(db.search_question_option(1, "i am gay", 10))
