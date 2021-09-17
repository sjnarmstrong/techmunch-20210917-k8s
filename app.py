from flask import Flask, request
from names import NAMES
import random
import os
import requests
import argparse


# Config
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--job", dest='job',
                  action="store_true", default=False)

args = parser.parse_args()



if os.path.isfile('/etc/namesvol/file'):
    my_name = open('/etc/namesvol/file', 'r').read()
else:
    my_name = NAMES[random.randint(0, len(NAMES)-1)]
    try:
        with open('/etc/namesvol/file', 'w') as fp:
            fp.write(my_name)
    except Exception as e:
        print(f"Could not save my name: {e}")

my_app_config = os.environ.get('APP_CONFIG', "N/A")
my_app_secret_config = os.environ.get('APP_SECRET_CONFIG', "N/A")
my_app_name = os.environ.get('APP_NAME', "techmunch")
app_port = os.environ.get("APP_PORT", "8888")

if os.path.isfile('/etc/test/file'):
    my_app_file_contents = open('/etc/test/file', 'r').read()
else:
    my_app_file_contents = "N/A"

# Run as Job
if args.job:
    i=-1
    while True:
        i+=1
        try:
            resp = requests.get(f"http://techmunch-{i}.techmunch-headless.techmunch-sholto.svc.cluster.local:{app_port}/kill")
            # resp = requests.get(f"http://{my_app_name}-{i}:{app_port}/kill")
        except requests.exceptions.ConnectionError:
            break
        if resp.status_code != 200:
            break
    quit()


# Start server
app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"<h1>Hello, World!</h1><h2>My name is: {my_name}</h2><h2>My config is: {my_app_config}</h2><h2>My secret is: {my_app_secret_config}</h2><h2>My files hold</h2><p>{my_app_file_contents}</p>"

@app.route("/neighbour")
def neighbour():
    try:
        resp = requests.get(f"http://techmunch-internal:{app_port}/whoami")
    except requests.exceptions.ConnectionError:
        return "<h1>I have no neighbors</h1>"

    neighbors = [resp.text]

    resp = ["<h1>My neighbour is:</h1>", "<ul>"]
    resp.extend((f"<li>{i}</li>" for i in neighbors))
    resp.append('</ul>')
    return ''.join(resp)

@app.route("/neighbours")
def neighbours():
    neighbors = []
    while True:
        try:
            # resp = requests.get(f"http://{my_app_name}-{len(neighbors)}:{app_port}/whoami")
            resp = requests.get(f"http://techmunch-{len(neighbors)}.techmunch-headless.techmunch-sholto.svc.cluster.local:{app_port}/whoami")
        except requests.exceptions.ConnectionError:
            break
        if resp.status_code != 200:
            break
        neighbors.append(resp.text)
    if len(neighbors) == 0:
        return "<h1>I have no neighbors</h1>"
    resp = ["<h1>My neighbors are:</h1>", "<ul>"]
    resp.extend((f"<li>{i}</li>" for i in neighbors))
    resp.append('</ul>')
    return ''.join(resp)

@app.route("/whoami")
def whoami():
    return my_name

@app.route("/kill")
def kill():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "<p>I am no longer :(</p>"


app.run(threaded=True, host="0.0.0.0",
        port=app_port)
