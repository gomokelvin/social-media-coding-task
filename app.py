from flask import Flask
import requests, logging
from queue import Queue
from threading import Thread

app = Flask(__name__)

result = []
# Queue to hold the urls
q = Queue()
urls = [
    'https://takehome.io/twitter',
    'https://takehome.io/facebook',
    'https://takehome.io/instagram'
]
num_threads = min(20, len(urls))


def get_posts(q, thread_num):
    """
    Method to get social media posts.
    :return:
    """
    while True:
        task = q.get()
        data = requests.get(task)
        result.append(data.json())
        q.task_done()
        print(f'Thread #{thread_num} is doing task #{task} in the queue.')


@app.route("/")
def social_network_activity():
    # TODO: your code here
    for i in range(4):
        worker = Thread(target=get_posts, args=(q, i,), daemon=True)
        worker.start()

    logging.info('All tasks completed.')
    q.join()
    json_response = result  # {}

    return json_response
