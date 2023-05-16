from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario
import pip
#
# with app.app_context():
#       database.create_all()
#
# with app.app_context():
#     usuario = Usuario(username='David', email='davidvn@gmail.com', senha='101303')
#     database.session.add(usuario)
#     database.session.commit()
#
# with app.app_context():
#     usuarios = Usuario.query.all()
#     print(usuarios)
#     primeiro_usuario = Usuario.query.first()
#     print(primeiro_usuario.email)
#
# with app.app_context():
#     database.drop_all()
#     database.create_all()
# with app.app_context():
#      usuario = Usuario.query.first()
#      print(usuario.cursos)
#
#
# with app.app_context():
#      post = Post.query.first()
#      print(post.titulo)
#      print(post.corpo)
# with app.app_context():
#     comentario = Comentario.query.first()
#     print(comentario.corpo)
# with app.app_context():
#     usuario = Usuario(username='teste', email='teste@gmail.com', senha='12345678')
#     database.session.add(usuario)
#     database.session.commit()
# with app.app_context():
#     meu_post = Post(titulo='post_teste', corpo='Esse é um teste', id_usuario=2)
#     database.session.add(meu_post)
#     database.session.commit()
