import thread
import Queue

messageLog = []
controlQueue = Queue.Queue()
clients = {}
mtx = thread.allocate_lock()
userList = {}

