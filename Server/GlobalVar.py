import thread
messageLog = []
clients = {}
mtx = thread.allocate_lock()
userList = {}

