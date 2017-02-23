import time
from g3ar import ThreadPool

def func(arg1):
  #
  # Do something intersting
  #
  time.sleep(5)
  return arg1

pool = ThreadPool()
pool.start()
pool.feed(target_func=func, arg1=4)
queue = pool.get_result_queue()
result = queue.get()
print(result)
pool.stop()
