from flask import Flask, render_template
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/test")
def test():
    return render_template('index.html')

app.run(host = '0.0.0.0', port=81)