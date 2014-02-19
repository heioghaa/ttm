import thread
import Queue
import mutex

messageLog = []
controlQueue = Queue.Queue()
clients = {}
mtx = mutex.mutex()
userList = {}

