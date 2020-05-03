import os
from concurrent.futures import ThreadPoolExecutor

from constants import MAX_THREAD_LIMIT

cpu_limit=os.cpu_count()
workers=cpu_limit * 4 if MAX_THREAD_LIMIT <= cpu_limit * 2 else MAX_THREAD_LIMIT
executor=ThreadPoolExecutor(workers)

def process_tasks(task_fn, *args, post_process_fn=None):
    if task_fn is not None and callable(task_fn):
        task=executor.submit(task_fn, *args)
        if post_process_fn is not None and callable(post_process_fn):
            task.add_done_callback(post_process_fn)
    else:
        raise Exception('parameter to process_tasks must be valid and callable')