import os
import threading
import time
import urllib.error
import urllib.request
import socket

from fastapi import FastAPI

app = FastAPI()


@app.get("/ping", status_code=204)
async def ping():
    pass


pong = os.environ['PONG'].split(',')

error = {x: [] for x in pong}


def run():
    def req(url):
        socket.setdefaulttimeout(2)
        try:
            with urllib.request.urlopen(f'http://{url}:4455/ping') as response:
                status_code = response.getcode()
                if status_code == 204:
                    error[url].clear()
                else:
                    error[url].append('E0')
        except socket.timeout:
            error[url].append('E1')
        except urllib.error.URLError:
            error[url].append('E2')

    while True:
        time.sleep(1)
        for i in pong:
            threading.Thread(target=req, args=[i]).start()
        for i in pong:
            if len(error[i]) > 15:
                print(f'error: {i}', len(error[i]))


threading.Thread(target=run).start()
