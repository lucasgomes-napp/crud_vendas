from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import sqlite3, time

app = Flask(__name__, template_folder='template')

def conexao_banco():
    conn = sqlite3.connect('crud_vendas/bd/vendas.db')
    return conn

@app.route("/")
def index():
    conn = conexao_banco()
    conn.row_factory = sqlite3.Row
    vendas = conn.execute('SELECT * FROM vendas')
    return render_template('index.html', vendas=vendas)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addData', methods=['POST', 'GET'])
def addData():
    if request.method == 'POST':
        valor = request.form['venda']
        status = request.form['status']
        quantidade = request.form['quantidade']
        estado = request.form['estado']
        con = conexao_banco()
        cur = con.cursor()
        cur.execute("INSERT INTO vendas(VALOR_VENDA, STATUS, QTD_VENDAS, ESTADO )values(?,?,?,?)", (valor,status,quantidade,estado))
        con.commit()
        return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    conn = conexao_banco()
    conn.execute(f'DELETE FROM vendas WHERE ID = {id}')
    conn.commit()
    return redirect(url_for('index'))

def import_csv():
    filename = r'crud_vendas\arquivo\data.csv'
    sales = pd.read_csv(filename)
    sales = sales.dropna().rename(columns={
        'i': 'ID',
        'c': 'ID_VENDAS',
        'd': 'DATA',
        'h': 'HORA',
        't': 'VALOR_VENDA',
        's': 'STATUS',
        'qtd_p': 'QTD_VENDAS',
        'e': 'ESTADO'})

    conn = sqlite3.connect(r'crud_vendas\bd\vendas.db')
    sales.to_sql(name='vendas', con=conn, index=False)


if __name__ == '__main__':
    #import_csv()
    app.run()