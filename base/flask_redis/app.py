import time
import os
import socket
import redis
from flask import Flask, make_response

DB_HOST = os.getenv('REDIS_HOST', 'redis')
MY_ENV = os.getenv('ENV', 'unknown')


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)
@app.route('/')
def hello():
    count = get_hit_count()
    return f"Hello World VERSION 5! I have been seen {count} times. My name is: {socket.gethostname()} My env: {MY_ENV}\n"
