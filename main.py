from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()
app = Flask(__name__)

mongo = os.getenv('MONGO_URI')
client = MongoClient(mongo)
db =client.get_database("Guide")

@app.route("/")
def test():
    guide_data = list(db['guides'].find({}))
    return render_template('index.html', guides = guide_data)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        db_users = db["users"]
        user = db_users.find_one({"pseudo" : request.form['utilisateur']})
        if user:
            if bcrypt.checkpw(request.form['mot_de_passe'].encode('utf-8'), user["password"]):
                session['role'] = user['role']
                session['user'] = user['pseudo']
            else:
                return render_template("login.html", erreur = "les mots de passes ne correspondent pas")
        return render_template('front/login.html', erreur = "les mots de passes ne correspondent pas")
    else:
        return render_template('front/login.html')

@app.route("/signup")
def signin():
    if request.method == 'POST':
        return render_template('signin.html', erreur = "le nom d'utilisateur existe déjà")
    else:
        if(request.form["mot_de_passe"] == request.form['verif_mot_de_passe']):
            utilisateur = request.form['utilisateur']
            mdp = request['mot_de_passe']
            avatar = request.form['avatar']

            mdp_crypte = mdp.encode("utf-8")
            salt = bcrypt.gensalt()
            mdp_hash = bcrypt.hashpw(mdp_crypte, salt)

            new_user = {
                "pseudo" : utilisateur,
                "password" : mdp_hash,
                "avatar" : avatar,
                "guides" : [],
                "role" : "user"
            }

            db["users"].insert_one(new_user)
            return redirect("/")
        else:
            return render_template('signin.html', erreur = "les mots de passe ne correspondent pas")
        
app.run(host = '0.0.0.0', port=81)