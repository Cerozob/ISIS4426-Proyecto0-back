import os
from tokenize import String
import traceback
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from passlib.hash import pbkdf2_sha512
from sqlalchemy import ForeignKey

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)
ma = Marshmallow(app)


# ["Conferencia", "Seminario", "Congreso", "Curso"]


class Categoria(db.Model):
    __tablename__ = "categorias"
    nombre = db.Column(
                    db.String(15),
                    primary_key=True,
                    nullable=False)
    eventos = db.relationship('Evento')


# ["Presencial", "Virtual"]


class Modalidad (db.Model):
    __tablename__ = "modalidades"
    nombre = db.Column(
                    db.String(10),
                    primary_key=True,
                    nullable=False)
    eventos = db.relationship('Evento')


class Evento(db.Model):
    __tablename__ = "eventos"
    id = db.Column(
                    db.Integer,
                    primary_key=True)
    nombre = db.Column(db.String(80))
    categoria = db.Column(db.String(15), ForeignKey("categorias.nombre")) # agregar constraint
    lugar = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    fechaInicio = db.Column(db.DateTime)
    fechaFin = db.Column(db.DateTime)
    modalidad = db.Column(db.String(10), ForeignKey("modalidades.nombre")) # agregar constraint
    owner = db.Column(db.String, ForeignKey("usuarios.username"))


class User(db.Model):
    __tablename__ = "usuarios"
    username = db.Column(
                        db.String(80),
                        primary_key=True)
    email = db.Column(db.String(80))
    passwordHash = db.Column(
                            db.String(512),
                            nullable=False)
    eventos = db.relationship('Evento')

    @property
    def passwordHash(self):
        raise AttributeError("read-only")

    @passwordHash.setter
    def hashPassword(self, password: str):
        self.passwordHash = pbkdf2_sha512.encrypt(password.encode('utf-8'))

    def checkPassword(self, password):
        return pbkdf2_sha512.verify(password, self.passwordHash)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "email")


class EventoSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "categoria", "lugar", "direccion", "fechaInicio", "fechaFin", "modalidad")


class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ["nombre"]


class ModalidadSchema(ma.Schema):
    class Meta:
        fields = ["nombre"]

def createAllTables():
    try:
        db.create_all()
    except:
        print("Error creando tablas")
        print(f"traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    app.run(debug=True)
