from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message='Preencha este campo.')])
    email = StringField('E-mail', validators=[DataRequired(message='Preencha este campo.'), Email(message='Endereço de email inválido.')])
    senha = PasswordField('Senha', validators=[DataRequired(message='Preencha este campo.')])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(message='Preencha este campo.'), EqualTo('senha', message='Repita a senha corretamente.')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado.")

    def validate_senha(self, senha):
        senha=senha.data
        if len(senha) < 6 or len(senha) > 20:
            raise ValidationError("Senha deve conter de 6 à 20 caracteres.")


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(message='Preencha este campo.'), Email(message='Endereço de email inválido.')])
    senha = PasswordField('Senha', validators=[DataRequired(message='Preencha este campo.')])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

    def validate_senha(self, senha):
        senha=senha.data
        if len(senha) < 6 or len(senha) > 20:
            raise ValidationError("Senha deve conter de 6 à 20 caracteres.")

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message='Preencha este campo.')])
    email = StringField('E-mail', validators=[DataRequired(message='Preencha este campo.'),Email(message='Endereço de email inválido.')])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    ling_java = BooleanField('Java')
    ling_javascript = BooleanField('Javascript')
    ling_python = BooleanField('Python')
    ling_typescript = BooleanField('Typescript')
    ling_c = BooleanField('C#')
    ling_cc = BooleanField('C++')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Já existe usuário com este email.")

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(message='Preencha este campo'), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui: ', validators=[DataRequired(message='Preencha este campo')])
    botao_submit_criarpost = SubmitField('Criar Post')

    def validate_senha(self, titulo):
        titulo = titulo.data
        if len(titulo) < 2 or len(titulo) > 140:
            raise ValidationError("Título deve conter de 2 à 140 caracteres.")

class FormEditarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(message='Preencha este campo'), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui: ', validators=[DataRequired(message='Preencha este campo')])
    botao_submit_editarpost = SubmitField('Editar Post')

    def validate_titulo(self, titulo):
        titulo = titulo.data
        if len(titulo) < 2 or len(titulo) > 140:
            raise ValidationError("Título deve conter de 2 à 140 caracteres.")
