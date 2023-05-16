from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarPost
from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


# Atribuindo a página ao link "home" à página inicial
@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

# Atribuindo a página ao link "usuarios" ao site
@app.route("/usuarios")
@login_required
def users():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

# Atribuindo a página ao link "contato" ao site
@app.route("/contato")
def contato():
    return render_template('contato.html')

# Atribuindo a página ao link "login" ao site com métodos de recepção e envio de dados
@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    # Validando login, exibindo mensagem de sucesso e redirecionando usuário para a página inicial
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login. E-mail ou senha incorretos.', 'alert-danger')

    # Validando criação de conta, exibindo mensagem de sucesso e redirecionando usuário para a página inicial
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        with app.app_context():
            # Criando usuário
            usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
            # Adicionando a sessão
            database.session.add(usuario)
            # Commit
            database.session.commit()
        flash(f'Conta criada para o email {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for(f'static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route("/post/criar", methods=["GET", "POST"])
@login_required
def criar_post():
    form= FormCriarPost()
    if form.validate_on_submit():
        with app.app_context():
            post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
            database.session.add(post)
            database.session.commit()
            flash('Post criado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    # adicionando o código no nome da imagem para não ter dois nomes igual no db
    cod = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arq = nome + cod + extensao
    caminho = os.path.join(app.root_path, 'static/fotos_perfil', nome_arq)
    # padronizando tamanho da imagem
    tamanho = (400, 400)
    imagem_redu = Image.open(imagem)
    imagem_redu.thumbnail(tamanho)
    # salvar a imagem
    imagem_redu.save(caminho)
    return nome_arq

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'ling_' in campo.name:
            if campo.data:
                #adicionar o texto do campo.label na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    foto_perfil = url_for(f'static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=["GET", "POST"])
@login_required
def exibir_post(post_id):
    with app.app_context():
        post = Post.query.get(post_id)
        if current_user == post.autor:
            form = FormEditarPost()
            if request.method == 'GET':
                form.titulo.data = post.titulo
                form.corpo.data = post.corpo
            elif form.validate_on_submit():
                post.titulo = form.titulo.data
                post.corpo = form.corpo.data
                database.session.commit()
                flash('Post atualizado com sucesso', 'alert-success')
                return redirect(url_for('home'))
        else:
            form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
