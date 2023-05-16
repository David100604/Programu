from comunidadeimpressionadora import app, database

# @app.before_first_request
# def create_tables():
#     with app.app_context():
#         database.create_all()

# Colocando o site pra rodar e aplicar edições por meio de código automaticamente
if __name__ == '__main__':
    app.run(debug=True)