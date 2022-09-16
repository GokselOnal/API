from flask import Flask
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///champions.db"


champ_put_args = reqparse.RequestParser()
champ_put_args.add_argument("name",  type=str)
champ_put_args.add_argument("class", type=str)
champ_put_args.add_argument("role",  type=str)
champ_put_args.add_argument("win%",  type=str)
champ_put_args.add_argument("pick%", type=str)
champ_put_args.add_argument("ban%",  type=str)


BASE = "/api/champions"

class Characters(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(20), nullable=False, unique=True)
    class_    = db.Column(db.String(20), nullable=False)
    role      = db.Column(db.String(20), nullable=False)
    win_rate  = db.Column(db.String(10))
    pick_rate = db.Column(db.String(10))
    ban_rate  = db.Column(db.String(10))


def info_champ(champ):
    return {"id"   : champ.id,
            "name" : champ.name,
            "class": champ.class_,
            "role" : champ.role,
            "win%" : champ.win_rate,
            "pick%": champ.pick_rate,
            "ban%" : champ.ban_rate}


@app.route(BASE)
def get_champs():
    champions = Characters.query.all()
    output = [info_champ(champ) for champ in champions]
    return {"champions": output}


@app.route(BASE + "/<int:id>")
def get_champ(id):
    champ = Characters.query.filter_by(id=id).first()
    if not champ:
        return {"message": "Could not find characters with that given id"}, 404
    return info_champ(champ)


@app.route(BASE + "/<string:name>")
def get_champ_by_name(name):
    champ = Characters.query.filter_by(name=name.title()).first()
    if not champ:
        return {"message": "Could not find characters with that given name"}, 404
    return info_champ(champ)


@app.route(BASE, methods=["POST"])
def add_champ():
    args = champ_put_args.parse_args()
    result = Characters.query.filter_by(name=args["name"]).first()
    if result:
        return {"message": "Character is already exist with given name"}, 409
    champ = Characters(name  =args["name"],
                       class_=args["class"],
                       role  =args["role"],
                       win_rate =args["win%"],
                       pick_rate=args["pick%"],
                       ban_rate =args["ban%"])
    db.session.add(champ)
    db.session.commit()
    return {"added": info_champ(champ)}, 201


@app.route(BASE + "/<int:id>", methods=["PUT"])
def update_champ(id):
    args = champ_put_args.parse_args()
    champ = Characters.query.filter_by(id=id).first()
    if not champ:
        return {"message": "Character doesn't exists with given id, cannot update"}, 404
    if champ:
        if args["name"] : champ.name = args["name"]
        if args["class"]: champ.class_ = args["class"]
        if args["role"] : champ.role = args["role"]
        if args["win%"] : champ.win_rate = args["win%"]
        if args["pick%"]: champ.pick_rate = args["pick%"]
        if args["ban%"] : champ.ban_rate = args["ban%"]
        db.session.commit()
    return {"updated": info_champ(champ)}


@app.route(BASE + "/<string:name>", methods=["PUT"])
def update_champ_by_name(name):
    args = champ_put_args.parse_args()
    champ = Characters.query.filter_by(name=name.title()).first()
    if not champ:
        return {"message": "Character doesn't exists with given name, cannot update"}, 404
    if champ:
        if args["name"] : champ.name = args["name"]
        if args["class"]: champ.class_ = args["class"]
        if args["role"] : champ.role = args["role"]
        if args["win%"] : champ.win_rate = args["win%"]
        if args["pick%"]: champ.pick_rate = args["pick%"]
        if args["ban%"] : champ.ban_rate = args["ban%"]
        db.session.commit()
    return {"updated": info_champ(champ)},


@app.route(BASE + "/<int:id>", methods=["DELETE"])
def delete_champ(id):
    champ = Characters.query.get(id)
    if not champ:
        return {"message": "Character doesn't exists with given id, cannot delete"}, 404
    db.session.delete(champ)
    db.session.commit()
    return {"deleted":  info_champ(champ)}


@app.route(BASE + "/<string:name>", methods=["DELETE"])
def delete_champ_by_name(name):
    champ = Characters.query.filter_by(name=name.title()).first()
    if not champ:
        return {"message": "Character doesn't exists with given name, cannot delete"}, 404
    db.session.delete(champ)
    db.session.commit()
    return {"deleted":  info_champ(champ)}


if __name__ == "__main__":
    app.run(debug=True)