from flask import Flask, render_template, request, redirect
from models import db, Produto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    estoque_minimo = int(request.form['estoque_minimo'])

    novo_produto = Produto(
        nome=nome,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo
    )

    db.session.add(novo_produto)
    db.session.commit()

    return redirect('/')

@app.route('/deletar/<int:id>')
def deletar(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)