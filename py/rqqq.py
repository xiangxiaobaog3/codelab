from rq import Queue, use_connection
from task import add
from redis import Redis
import time
import logging

# use redis by default
# create work queue
redis_conn = Redis()
q = Queue(connection=redis_conn)

#notice: cann't run a task function in __main__ module
#because rq save module and function name in redis
#when rqworker running, __main__ is another module
# enqueue tasks,function enqueue returns the job instance
job = q.enqueue(add, 3, 9)
print job.result
time.sleep(0.1)
#get the job result by job.result
logging.warn("result is %s", job.result)

