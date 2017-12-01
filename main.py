from flask import Flask, request, redirect, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'empdata'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM user''')
    rv = cur.fetchall()
    for row in rv :
        print(row)
    return str(rv[0])

@app.route('/addaction', methods=['GET', 'POST'])
def addaction():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO user (userId, userName, password) VALUES (%s, %s, %s)''', (request.form['userId'], request.form['username'], request.form['password']))
        mysql.connection.commit()
        return redirect('/list')

@app.route('/editaction', methods=['GET', 'POST'])
def editaction():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE user SET userName=%s, password=%s WHERE userId=%s''', (request.form['username'], request.form['password'], request.form['userId']))
        mysql.connection.commit()
        return redirect('/list')

@app.route('/edit/<id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM user WHERE userId=%s''', [id])
    data = cur.fetchall()
    mysql.connection.commit()
    return render_template('editform.html', data=data)

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM user WHERE userId=%s''', [id])
    mysql.connection.commit()
    return redirect('/list')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/list')
def list():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM user''')
    data = cur.fetchall()
    return render_template('list.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)