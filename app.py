from flask import Flask
import requests, logging
from queue import Queue
from threading import Thread

app = Flask(__name__)

results = {}
# Queue to hold the urls
q = Queue()

urls = [
    # ('social_media_name', 'url_name')
    ['Twitter', 'https://takehome.io/twitter'],
    ['Facebook', 'https://takehome.io/facebook'],
    ['Instagram', 'https://takehome.io/instagram']
]
num_threads = min(20, len(urls))


def get_posts(q, thread_num, r):
    """

    :re turn:
    """
    while True:
        try:
            task = q.get()
            data = requests.get(task[1])
            # create dict record
            results.update({urls[r][0]: len(data.json())})
            print(f'Thread #{thread_num} is doing task #{task} in the queue {r}.')
        except ConnectionError:
            print("Connection errors!!!")
        q.task_done()


@app.route("/")
def social_network_activity():
    # TODO: your code here

    # Starting worker threads on queue processing
    for i in range(len(urls)):
        worker = Thread(target=get_posts, args=(q, i, i), daemon=True)
        worker.start()

    # Threaded function for queue processing.
    # Starting worker threads on queue processing
    for j in range(len(urls)):
        q.put(urls[j])

    q.join()
    logging.info('All tasks completed.')

    json_response = results

    return json_response
