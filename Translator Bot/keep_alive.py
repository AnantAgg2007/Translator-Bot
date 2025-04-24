from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "I'm alive!"  # Simple route to keep the server alive


def run():
    app.run(host='0.0.0.0', port=8080,
            threaded=True)  # Enable threaded mode for better performance


def keep_alive():
    t = Thread(target=run)
    t.daemon = True  # Make sure the thread dies when the main program ends
    t.start()
