from app import db, login_manager

from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __str__(self):
        return self.username


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    graduacao = db.Column(db.String(40), unique=True)
    
    def __init__(self, nome, graduacao):
        self.nome = nome
        self.graduacao = graduacao
    
    def __str__(self):
        return self.nome
    
    
class Tcc(db.Model):
    __tablename__ = 'tcc'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, unique=True, nullable=False)
    
    autor = db.Column(db.Integer, db.ForeignKey('user.id'))
    orientador = db.Column(db.Integer, db.ForeignKey('user.id'))
    curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    
    def __init__(self, titulo, autor, orientador, curso):
        self.titulo = titulo
        self.autor = autor
        self.orientador = orientador
        self.curso = curso
    
    def __str__(self):
        return self.titulo
    

    
    
    