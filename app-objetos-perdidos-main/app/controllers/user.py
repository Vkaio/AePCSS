from ..models.user import User
from ..db import db_session
from passlib.hash import sha256_crypt
from flask import flash, session, redirect, url_for

class UserController():
    @staticmethod
    def get_users():
        session_db = db_session()

        users = session_db.query(User).all()

        session_db.close()

        return users


    @staticmethod
    def get_user(id):
        session_db = db_session()

        user = session_db.query(User).filter_by(id=id).first()

        session_db.close()

        return user

    
    @staticmethod
    def get_user_by_email(email):
        session_db = db_session()

        user = session_db.query(User).filter_by(email=email).first()

        session_db.close()

        return user


    @staticmethod
    def login(request):
        email = request.form['email']
        password = request.form['password']

        user = UserController.get_user_by_email(email)

        if sha256_crypt.verify(password, user.password):
            session['logged_in'] = True
            session['username'] = user.name
            session['id'] = user.id

            return redirect(url_for('view_objects'))
        else:
            flash('usuário ou senha inválida!')
            return redirect(request.url)

    @staticmethod
    def logout():
        session.clear()


    @staticmethod
    def create(request):
        name = ''
        email = ''
        phone = ''
        password = ''

        if request.is_json:
            content = request.get_json()
            name = content['name']
            email = content['email']
            phone = content['phone']
            password = content['password']
        else:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']

        user = User(name=name, email=email, phone=phone, password=password)

        session_db = db_session()

        result = ''
        try: 
            session_db.add(user)
        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        if request.is_json:
            result = user.serialize()

        session_db.close()

        return result


    @staticmethod
    def update(id, request):
        name = ''
        email = ''
        phone = ''
        password = ''

        if request.is_json:
            content = request.get_json()
            name = content['name']
            email = content['email']
            phone = content['phone']
            password = content['password']
        else:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']

        session_db = db_session()

        result = ''
        try: 
            user = session_db.query(User).filter_by(id=id).update(
                {
                    'name': name,
                    'password': password,
                    'phone': phone,
                    'email': email,
                }, synchronize_session='fetch')

        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        if request.is_json:
            user = session_db.query(User).filter_by(id=id).first()
            result = user.serialize()

        session_db.close()

        return result


    @staticmethod
    def delete(id):
        session_db = db_session()

        result = ''
        try:
            user = session_db.query(User).filter_by(id=id).delete(
                synchronize_session='fetch')
        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        session_db.close()

        return result


    @staticmethod
    def fill_table():
        user = User(name='Admin', email='admin@admin.com', password=sha256_crypt.encrypt('123'))
        user2 = User(name='Tester', email='tester@admin.com', password=sha256_crypt.encrypt('123'))

        session_db = db_session()

        result = ''
        try: 
            session_db.add(user)
            session_db.add(user2)
        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        session_db.close()

        return result
    

