from flask import Flask, render_template
import pandas as pd
import sqlite3

app = Flask(__name__, template_folder='template')

def get_db_connection():
    conn = sqlite3.connect('bd/vendas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    vendas = conn.execute('SELECT * FROM vendas')
    return render_template('index.html', vendas=vendas)

def import_csv():
    filename = 'arquivo\data.csv'
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

    conn = sqlite3.connect(r'bd\vendas.db')
    sales.to_sql(name='vendas', con=conn, index=False)


if __name__ == '__main__':
    #import_csv()
    app.run(debug=True)