"""bibliotecas importadas"""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

"""configuração banco de dados sqlite"""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agenda.sqlite3"

db = SQLAlchemy(app)

#comando para funcionamento do create_all
app.app_context().push()

"""estrutura banco de dados"""
class agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    contato = db.Column(db.Integer)
    descricao = db.Column(db.String(100))
    data_hora = db.Column(db.String(30))
    valor = db.Column(db.Integer)

    def __init__(self, nome, contato, descricao, data_hora, valor):
        self.nome = nome
        self.contato = contato
        self.descricao = descricao
        self.data_hora = data_hora
        self.valor = valor

"""rotas para as páginas"""
@app.route('/')
def principal():
    return render_template("index.html")

@app.route('/area_do_profissional', methods=["GET", "POST"])
def agendamento():
    return render_template("area_do_profissional.html", agenda=agenda.query.all())

@app.route('/inserir_cadastro', methods=["GET", "POST"])
def cria_cadastro():
    nome = request.form.get('nome')
    contato = request.form.get('contato')
    descricao = request.form.get('descricao')
    data_hora = request.form.get('data_hora')
    valor = request.form.get('valor')

    if request.method == "POST":
        ag = agenda(nome, contato, descricao, data_hora, valor)
        db.session.add(ag)
        db.session.commit()
        return redirect(url_for('agendamento'))   
    return render_template("inserir_cadastro.html")

@app.route('/<int:id>/atualizar_cadastro', methods=["GET", "POST"])
def atualizar_cadastro(id):
    atualiza = agenda.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form["nome"]
        contato = request.form["contato"]
        descricao = request.form["descricao"]
        data_hora = request.form["data_hora"]
        valor = request.form["valor"]

        agenda.query.filter_by(id=id).update({"nome":nome, "contato":contato, "descricao":descricao, "data_hora":data_hora, "valor":valor})
        db.session.commit()
        return redirect(url_for('agendamento'))
    return render_template("atualizar_cadastro.html", atualiza=atualiza)

@app.route('/<int:id>/excluir_cadastro', methods=["GET", "POST"])
def excluir_cadastro(id):
    atualiza = agenda.query.filter_by(id=id).first()
    db.session.delete(atualiza)
    db.session.commit()
    return redirect(url_for('agendamento'))
    return render_template("excluir_cadastro.html")


#with site.app_context():
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)