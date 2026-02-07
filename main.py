from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db =client.get_database("Guide")

@app.route("/")
def test():
    guide_data = list(db['Guide'].find({}))
    return render_template('index.html', guides = guide_data)

app.run(host = '0.0.0.0', port=81)