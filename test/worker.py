from rq import Connection, Queue, Worker

if __name__ == '__main__':
    with Connection():
        q=Queue()
        Worker(q).work()
