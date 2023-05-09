from flask import render_template, request, url_for, redirect, flash
from app import app, db, login_manager
from models import User, Tcc, Curso
from flask_login import login_user, logout_user, current_user

@app.route('/')
def index():
    users = User.query.all()
    tccs = Tcc.query.all()
    cursos = Curso.query.all()
    return render_template('index.html', users=users, tccs=tccs, cursos=cursos)

#                                  TCC


@app.route('/tcc/cadastro', methods=['GET', 'POST'])
def tcccadastro():
    if not current_user.is_authenticated:
        proxima = 'tcccadastro'
        return redirect(url_for('login', proxima=proxima, a='aa', b='bb', c='cc'))
    users = User.query.all()
    cursos = Curso.query.all()
    
    if request.method == 'POST':
        if request.form['autor'] == request.form['orientador']:
            print('O autor não pode ser o orientador')
            return
        
        titulo = request.form['titulo']
        autor = request.form['autor']
        orientador = request.form['orientador']
        curso = request.form['curso']
        tcc = Tcc(titulo, autor, orientador, curso)
        print('cheguei add')
        db.session.add(tcc)
        db.session.commit()
        print('passe commit')
        return redirect(url_for('index'))  
    return render_template('tcc/tcccadastro.html', users=users, cursos=cursos)


@app.route('/tcc/delete/<int:id>', methods=['GET', 'POST']) 
def tccdelete (id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    tcc = Tcc.query.get(id)
    db.session.delete(tcc)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tcc/atualizar/<int:id>', methods=['GET', 'POST']) 
def tccatualizar (id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    tcc = Tcc.query.get(id)
    users = User.query.all()
    cursos = Curso.query.all()
    
    if request.method == 'POST':
        tcc.titulo = request.form['titulo']
        tcc.autor = request.form['autor']
        tcc.orientador = request.form['orientador']
        tcc.curso = request.form['curso']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('tcc/tccatualiza.html', tcc=tcc, users=users, cursos=cursos)


#                            ----__CURSO__---

@app.route('/curso/cadastro', methods=['GET', 'POST'])
def cursocadastro():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome'] 
        graduacao = request.form['graduacao']
        
        curso = Curso(nome, graduacao)
        
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for('index'))
        
        
    return render_template('curso/cursocadastro.html')

#                            ----__USER__----


@app.route('/user/cadastro', methods=['GET', 'POST'])
def cadastro():
    
    # verificar se os campos estão vazios ou se o user já existe
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, email, password)
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('user/cadastro.html')




@app.route('/user/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        proxima = request.form['proxima']
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.password == password:
            flash('Verifique a senha e email')
            return redirect(url_for('login'))
          
        flash('login feito com sucesso')
        login_user(user)
        print(proxima)
        print('proxima acima')
        return redirect(url_for(proxima))
        
    return render_template('user/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))