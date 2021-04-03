from flask import Flask, render_template, url_for, request, redirect, send_from_directory, session, flash
from functools import wraps
from .db import init_db
from .models.object import Object
from .controllers.object import ObjectController
from .controllers.user import UserController
from flask import jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER='/var/www/uploads'
    )

    from . import database
    database.init_app(app)

    def is_logged_in(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('Nao autorizado, faça o login', 'perigo')
                return redirect(url_for('login'))
        return wrap


    @app.route('/')
    def hello():
        init_db()

        UserController.fill_table()
        ObjectController.fill_table()

        return redirect(url_for('view_objects'))

    @app.route('/users/view', methods=['GET'])
    @is_logged_in
    def profile():
        objs = ObjectController.get_objects_of_user(session['id'])

        return render_template('profile/index.html', objs=objs)


    @app.route('/objects/create', methods=['GET', 'POST'])
    @is_logged_in
    def create_object():
        if request.method == 'GET':
            return render_template('registerObject/index.html')

        else:
            ObjectController.create(request)

            return redirect(url_for('view_objects'))


    @app.route('/objects/view', methods=['GET'])
    def view_objects():
        objs = ObjectController.get_objects()

        return render_template('showCase/index.html', objs=objs)

    @app.route('/objects/view/<id>', methods=['GET'])
    def view_object(id):
        obj = ObjectController.get_object(id)
        user = UserController.get_user(obj.user_id)

        return render_template('objectDetails/index.html', obj=obj, user=user)


    @app.route('/objects/update/<id>', methods=['GET', 'POST'])
    @is_logged_in
    def update_object(id):
        obj = ObjectController.get_object(id)

        if session['id'] == obj.user_id:
            if request.method == 'GET':

                return render_template('registerObject/index.html', obj=obj)

            else:
                obj = ObjectController.update(id, request)

                return redirect(url_for('profile'))

        else:
            return redirect(url_for('profile'))


    @app.route('/objects/delete/<id>', methods=['GET'])
    @is_logged_in
    def delete_object(id):
        obj = ObjectController.get_object(id)

        if session['id'] == obj.user_id:
            obj = ObjectController.delete(id)

        return redirect(url_for('profile'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            UserController.login(request)

            return redirect(url_for('view_objects'))

        return render_template('login/index.html')


    @app.route('/logout')
    @is_logged_in
    def logout():
        UserController.logout()

        return redirect(url_for('view_objects'))


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            UserController.create()
#            name = request.form['name']
#            email = request.form['email']
#            phone = request.form['phone']
#            password = request.form['password']


#            cuser = User(name=name, email=email, phone=phone, password=password)

#            session_db = db_session()

#            try:
#                session_db.add(user)
#            except:
#                session_db.rollback()
#            else:
#                session_db.commit()
#
#            session_db.close()

#        return render_template('signUp/index.html', form=form)

        return render_template('signUp/index.html')

    def mascaraDeTelefone(telefone):
        textoAtual = telefone.value
        textoAjustado = telefone.value
        if(textoAtual.length == 11):
            parte1 = textoAtual.slice(0,1)
            parte2 = textoAtual.slice(2,6)
            parte3 = textoAtual.slice(7,10)
            textoAjustado = '(' + parte1 + ')' + parte2 + '-' + parte3

        telefone.value = textoAjustado


    @app.route('/objects', methods=['GET', 'POST'])
    def json_objects_get_or_create():
        if request.method == 'POST':
            return ObjectController.create(request)

        objs = ObjectController.get_objects()
        return jsonify(eqtls=[obj.serialize() for obj in objs])


    @app.route('/objects/<int:id>', methods=['PUT', 'DELETE'])
    def json_object_get_or_update_or_delete(id):
        if request.method == 'DELETE':
            result = ObjectController.delete(id)

            return jsonify(status='success')

        else:
            return ObjectController.update(id, request)


    @app.route('/db_test')
    @is_logged_in
    def db_test():
        database.init_db()

        return 'Banco de dados inicializado com sucesso!'

    @app.route('/uploads/<filename>')
    def upload(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


    return app
