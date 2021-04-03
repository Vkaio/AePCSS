from ..models.object import Object
from ..db import db_session
from werkzeug.utils import secure_filename
from flask import flash, redirect, session
import os

UPLOAD_FOLDER='/var/www/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ObjectController():
    @staticmethod
    def get_objects():
        session_db = db_session()

        objects = session_db.query(Object).all()

        session_db.close()

        return objects


    @staticmethod
    def get_object(id):
        session_db = db_session()

        obj = session_db.query(Object).filter_by(id=id).first()

        session_db.close()

        return obj

    
    @staticmethod
    def get_objects_of_user(id):
        session_db = db_session()

        objs = session_db.query(Object).filter_by(user_id=id).all()

        session_db.close()

        return objs


    @staticmethod
    def create(request):
        name = ''
        description = ''
        reward = ''
        image_path = ''
        user_id = ''

        if request.is_json:
            content = request.get_json()
            name = content['name']
            description = content['description']
            reward = content['reward']
        else:
            name = request.form['name']
            description = request.form['description']
            reward = request.form['reward']
            user_id = session['id']

        if 'object_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            file = request.files['object_image']

            if file.filename == '':
                image_path = '#'

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_path = filename

        obj = Object(name=name, description=description, reward=reward, image_path=image_path, user_id=int(user_id))

        session_db = db_session()

        result = ''
        try: 
            session_db.add(obj)
        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        if request.is_json:
            result = obj.serialize()

        session_db.close()

        return result


    @staticmethod
    def update(id, request):
        name = ''
        description = ''
        reward = ''
        image_path = ''

        old_obj = ObjectController.get_object(id)

        if request.is_json:
            content = request.get_json()
            name = content['name']
            description = content['description']
            reward = content['reward']
        else:
            name = request.form['name']
            description = request.form['description']
            reward = request.form['reward']

        if 'object_image' not in request.files:
            image_path = old_obj.image_path

        else:
            file = request.files['object_image']

            if file.filename == '':
                image_path = old_obj.image_path

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                if filename != old_obj.image_path:
                    # os.remove(os.path.join(UPLOAD_FOLDER, old_obj.image_path))
                    file.save(os.path.join(UPLOAD_FOLDER, filename))

                image_path = filename

        session_db = db_session()

        result = ''
        try: 
            obj = session_db.query(Object).filter_by(id=id).update(
                {
                    'name': name,
                    'description': description,
                    'reward': reward,
                    'image_path': image_path,
                }, synchronize_session='fetch')

        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        if request.is_json:
            obj = session_db.query(Object).filter_by(id=id).first()
            result = obj.serialize()

        session_db.close()

        return result


    @staticmethod
    def delete(id):

        image_path = ObjectController.get_object(id).image_path

        session_db = db_session()

        result = ''

        try:
            obj = session_db.query(Object).filter_by(id=id).delete(
                synchronize_session='fetch')
        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            os.remove(os.path.join(UPLOAD_FOLDER, image_path))

            result = 'success'

        session_db.close()

        return result


    @staticmethod
    def fill_table():
        obj1 = Object(name='Mi Band 3', description='Relógio pulseira preta', reward='Um muito obrigado!', image_path='#', user_id=1)
        obj2 = Object(name='Rolex', description='Relógio suiço de R$ 20.000', reward='', image_path='#', user_id=1)

        session_db = db_session()

        result = ''
        try: 
            session_db.add(obj1)
            session_db.add(obj2)
        except:
            session_db.rollback()
            result = 'failure'
        else:
            session_db.commit()
            result = 'success'

        session_db.close()

        return result
