from bson import ObjectId
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()
app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key

uri = "mongodb+srv://Louis:O6eE8Gd2mz0OAzrR@cluster0.0a0qlbo.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

#mongo = os.getenv('MONGO_URI')
#client = MongoClient(mongo)
db =client.get_database("Guide")

@app.route("/")
def test():
    guide_data = list(db['guides'].find({}))
    return render_template('index.html', guides = guide_data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        db_users = db["users"]
        user = db_users.find_one({"pseudo" : request.form['utilisateur']})
        if user:
            if bcrypt.checkpw(request.form['mot_de_passe'].encode('utf-8'), user["password"]):
                session['role'] = user['role']
                session['user'] = user['pseudo']
                return redirect("/")
                
            else:
                return render_template('front/login.html', erreur = "les mots de passes ne correspondent pas")
        
    return render_template('front/login.html')

#@app.route("/signin", methods=["GET", "POST"])
#def signin():
    if request.method == 'POST':
        return render_template('signin.html', erreur = "le nom d'utilisateur existe déjà")
    else:
        if(request.form["mot_de_passe"] == request.form['verif_mot_de_passe']):
            utilisateur = request.form['utilisateur']
            mdp = request.form['mot_de_passe']
            avatar = request.form['avatar']

            mdp_crypte = mdp.encode("utf-8")
            salt = bcrypt.gensalt()
            mdp_hash = bcrypt.hashpw(mdp_crypte, salt)

            if len(utilisateur) < 3 or len(utilisateur) > 4:
                return redirect(url_for('login'))
            
            if len(mdp) < 10:
                return redirect(url_for('login'))

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


#@app.route("/signin", methods=["GET", "POST"])
#def signin():
    if request.method == "GET":
        return render_template("signin.html")

    if request.form["mot_de_passe"] != request.form["verif_mot_de_passe"]:
        return render_template(
            "signin.html",
            erreur="Les mots de passe ne correspondent pas"
        )
    print("ok")

    if request.method == "POST":
        utilisateur = request.form["utilisateur"]
        mdp = request.form["mot_de_passe"]
        avatar = request.form["avatar"]

        if db["users"].find_one({"pseudo": utilisateur}):
            return render_template(
                "signin.html",
                erreur="Le nom d'utilisateur existe déjà"
            )
        print("ok")

        if len(utilisateur) < 3 or len(utilisateur) > 20:
            return render_template(
                "signin.html",
                erreur="Le nom d'utilisateur doit contenir entre 3 et 20 caractères"
            )
        print("ok")

        if len(mdp) < 10:
            return render_template(
                "signin.html",
                erreur="Le mot de passe doit contenir au moins 10 caractères"
            )
        print("ok")

        mdp_hash = bcrypt.hashpw(
            mdp.encode("utf-8"),
            bcrypt.gensalt()
        )
        print("ok")

        new_user = {
            "pseudo": utilisateur,
            "password": mdp_hash,
            "avatar": avatar,
            "guides": [],
            "role": "user"
        }

        db["users"].insert_one(new_user)
        print("ok")
        return redirect("/")
    
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    
    if request.method == "POST":
        utilisateur = request.form.get("utilisateur", "").strip()
        mdp = request.form.get("mot_de_passe", "")
        verif_mdp = request.form.get("verif_mot_de_passe", "")
        avatar = request.form.get("avatar", "")
        
        if mdp != verif_mdp:
            return render_template("signin.html", erreur="Les mots de passe ne correspondent pas")
        
        if len(utilisateur) < 3 or len(utilisateur) > 20:
            return render_template("signin.html", erreur="Le nom d'utilisateur doit contenir entre 3 et 20 caractères")
        
        if db["users"].find_one({"pseudo": utilisateur}):
            return render_template("signin.html", erreur="Le nom d'utilisateur existe déjà")
        
        if len(mdp) < 10:
            return render_template("signin.html", erreur="Le mot de passe doit contenir au moins 10 caractères")
        
        mdp_hash = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())
        
        new_user = {
            "pseudo": utilisateur,
            "password": mdp_hash,
            "avatar": avatar,
            "guides": [],
            "role": "user"
        }
        
        db["users"].insert_one(new_user)
        return redirect("/")


app.route("/publish/add")
def add_guide():
    return render_template('publish.html', tags=TAGS)

@app.route("/publish/create", methods=['POST'])
def create_guide():
    titre = request.form['nom']
    description = request.form['description']
    image = request.files['image']
    tag = request.form.getlist['tag']
    auteur = session['user']
    
    if image:
        nom_fichier = secure_filename(image.filename)
        upload_path = os.path.join(app.static_folder, 'images/user', nom_fichier)
        image.save(upload_path)
        image_path = f"/static/images/user/{nom_fichier}"

    else :
        image_path = ""

    guides  = {
        "nom": titre,
        "description": description,
        "image": image_path,
        "tag": tag,
        "auteur": auteur,
        "likes": 0,
        "liked_by": []
    }
    db['guides'].insert_one(guides)
    return redirect(url_for('index'))

@app.route("/guide/<guide_id>")
def like_guide(guide_id):
    if 'util' in session:
        return(url_for('login'))
    
    user = session['util']
    guide = db['guides'].find_one({"_id": ObjectId(guide_id)})

    if not guide:
        return redirect(url_for('index'))
    
    if user in guide["liked_by", []]:
        db['guides'].update_one({"_id" : ObjectId(guide_id)},
                            {"$inc": {"likes": -1}, 
                             "$pull": {"liked_by": user}
                             })
    else:
        db['guides'].update_one({"_id" : ObjectId(guide_id)},
                            {"$inc": {"likes": 1}, 
                             "$push": {"liked_by": user}
                             })
        
result = db['guides'].update_many({"$or" : [
    {"tags" : {"$exists": False}},
    {"likes" : {"$exists": False}},
    {"liked_by" : {"$exists": False}}
]},
    {"$set": {"tags" : [],
              "likes" : 0,
              "liked_by" : []
             }  
    }
)
##########ADMIN##########

@app.route('/admin')
def admin():
    guide_data = list(db['guides'].find({}))
    users = list(db['users'].find({}))
    if 'util' in session and session['role'] == 'admin':
        return render_template('back/back_accuei.html', guides=guide_data, users=users)
    else:
        return render_template('index.html', erreur="Vous n'avez pas les droits d'accès", guides=guide_data, users=users)
    
@app.route('/admin/update_role/<user_id>')
def update_role(user_id):
    if 'util' in session and session['role'] == 'admin':
        new_role = request.form.get('role')

        db['dresseurs'].update_one({"_id": ObjectId(user_id)}, {"$set": {"role": new_role}})

    return redirect(url_for('admin'))

@app.route('/admin/delete_user/<user_id>')
def delete_user(user_id):
    if 'util' in session and session['role'] == 'admin':
        db['users'].delete_one({"_id": ObjectId(user_id)})
    return redirect(url_for('admin'))


app.run(host = '0.0.0.0', port=81)