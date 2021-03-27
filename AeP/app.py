from flask import Flask, render_template, logging, redirect, url_for, flash, session
from dados import Objetos
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '94829090'
app.config['MYSQL_DB'] = 'aepapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#Objetos = Objetos()

@app.route('/')
def index():
    return render_template('PgInicial.html', objetos = Objetos)

@app.route('/IEEECS_UnB_AeP')
def info():
    return render_template('info.html')


@app.route('/objetos')
def objetos():

    cur = mysql.connection.cursor()


    result = cur.execute("SELECT * FROM objetos")

    objetos = cur.fetchall()

    if result > 0:
        return render_template('objetos.html', objetos=objetos)
    else:
        msg = 'Objeto nao encontrado'
        return render_template('objetos.html', msg=msg)

    cur.close()


@app.route('/objetos/<string:id>')
def objetos(id):

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM objetos WHERE id = %s", [id])

    objetos = cur.fetchone()

    return render_template('objetos.html', objetos=objetos)


class RegisterForm(Form):
    name = StringField('Nome', [validators.Length(min=1, max=50)])
    username = StringField('Usuario', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Senha', [
        validators.DataRequired(),
        validators.EqualTo('Confirme', message='Senha ou Usuario invalidos')
    ])
    confirm = PasswordField('Confirme a senha')


@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))


        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()

        cur.close()

        flash('Voce realizou o cadastro com sucesso', 'sucesso')

        return redirect(url_for('login'))
    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password_candidate = request.form['password']


        cur = mysql.connection.cursor()


        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:

            data = cur.fetchone()
            password = data['password']


            if sha256_crypt.verify(password_candidate, password):

                session['logged_in'] = True
                session['username'] = username

                flash('Voce esta logado', 'sucesso')
                return redirect(url_for('dashboard'))
            else:
                error = 'Login invalido'
                return render_template('login.html', error=error)

            cur.close()
        else:
            error = 'Usuario nao encontrado'
            return render_template('login.html', error=error)

    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Nao autorizado, faça o login', 'perigo')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Voce saiu da sessao', 'sucesso')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur = mysql.connection.cursor()


    result = cur.execute("SELECT * FROM objetos WHERE author = %s", [session['username']])

    objetos = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', objetos=objetos)
    else:
        msg = 'Objeto nao encontrado'
        return render_template('dashboard.html', msg=msg)

    cur.close()


class ObjetosForm(Form):
    title = StringField('Titulo', [validators.Length(min=1, max=200)])
    desc = TextAreaField('Descricao', [validators.Length(min=30)])


@app.route('/add_objetos', methods=['GET', 'POST'])
@is_logged_in
def add_objetos():
    form = ObjetosForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        desc = form.desc.data


        cur = mysql.connection.cursor()


        cur.execute("INSERT INTO objetos(title, desc, author) VALUES(%s, %s, %s)",(title, desc, session['username']))


        mysql.connection.commit()


        cur.close()

        flash('Objeto adcionado', 'sucesso')

        return redirect(url_for('dashboard'))

    return render_template('add_objetos.html', form=form)



@app.route('/edit_objeto/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_objeto(id):

    cur = mysql.connection.cursor()


    result = cur.execute("SELECT * FROM objetos WHERE id = %s", [id])

    objetos = cur.fetchone()
    cur.close()

    form = ObjetoForm(request.form)


    form.title.data = objeto['title']
    form.desc.data = objeto['desc']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        desc = request.form['desc']


        cur = mysql.connection.cursor()
        app.logger.info(title)

        cur.execute ("UPDATE objetos SET title=%s, desc=%s WHERE id=%s",(title, desc, id))

        mysql.connection.commit()


        cur.close()

        flash('Objeto editado', 'sucesso')

        return redirect(url_for('dashboard'))

    return render_template('edit_objeto.html', form=form)


@app.route('/delete_objeto/<string:id>', methods=['POST'])
@is_logged_in
def delete_objeto(id):

    cur = mysql.connection.cursor()


    cur.execute("DELETE FROM objetos WHERE id = %s", [id])


    mysql.connection.commit()


    cur.close()

    flash('Objeto deletado', 'sucesso')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='CSTrainee2021'
    app.run(debug=True)
