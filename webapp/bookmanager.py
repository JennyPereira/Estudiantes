import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "sqlite.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Estudiante(db.Model):
    """
    """
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))
    #nombre = db.Column(db.String(30), unique=False, nullable=False)

    #apellido = db.Column(db.String(30), unique=False, nullable=False) 

    def __repr__(self):
        return "<Title: {}>".format(self.nombre)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        est = Estudiante(nombre=request.form.get("nombre"), apellido=request.form.get("apellido"))
        db.session.add(est)
        db.session.commit()
    
    ests = Estudiante.query.all()
    return render_template("home.html", ests=ests)
    # return render_template("home.html")
   
@app.route("/update", methods=["POST"])
def update():
    idEstudiante = request.form.get("id")
    nuevoNombre = request.form.get("nuevoNombre")
    nuevoApellido = request.form.get("nuevoApellido")
    est = Estudiante.query.get(idEstudiante)
    est.nombre = nuevoNombre
    est.apellido = nuevoApellido
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idEstudiante = request.form.get("id")
    est = Estudiante.query.get(idEstudiante)
    db.session.delete(est)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)