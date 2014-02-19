import Queue
import mutex

messageLog = []
controlQueue = Queue()
clients = {}
mtx = mutex()
userList = {}

