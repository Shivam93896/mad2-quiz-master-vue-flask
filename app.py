from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime 
from passlib.hash import bcrypt 
from backend.models import db,User
from backend.api import (User_Login, AddSubject,User_Signup,AddChapter,AddQuiz,AddQuestion, Export_Details, Username,
                         StartQuiz,Admin_Summary,Admin_User,User_Result)
from backend.config import cache
from backend.worker import*
from backend.task import*

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.LocalConfig')
    db.init_app(app)
    cache.init_app(app)
    return app

def admin():
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin=User(username='admin',
                    email='admin@gmail.com',
                    password=bcrypt.hash('admin123'),
                    dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
                    fullname = 'Admin' ,is_admin=True,
                    qualification='BS')
        db.session.add(admin)
        db.session.commit()



app = create_app()
api = Api(app)
CORS(app)
jwt = JWTManager(app)
with app.app_context():
    celery=celery_init_app(app)
    celery.conf.beat_schedule=CeleryConfig.beat_schedule
    db.create_all()
    admin()   

@app.get('/')
def index():
    return 'Hello world Shivam Kumar'   

@app.get('/test')
@cache.cached(timeout=10)
def test():
    return {'Time':str(datetime.now())}



api.add_resource(User_Login,'/login')
api.add_resource(User_Signup,'/signup')
api.add_resource(AddSubject, '/add_subject/get','/add_subject/post', '/edit_subject/<int:sub_id>','/delete_subject/<int:sub_id>')
api.add_resource(AddChapter, '/add_chapter/get','/add_chapter/<int:sub_id>','/edit_chapter/<int:chap_id>','/delete_chapter/<int:chap_id>')
api.add_resource(AddQuiz, '/add_quiz','/edit_quiz/<int:quiz_id>','/delete_quiz/<int:quiz_id>', '/get_quiz')
api.add_resource(AddQuestion, '/add_question/<int:quiz_id>','/edit_question/<int:question_id>','/delete_question/<int:question_id>','/get_questions/<int:quiz_id>')
api.add_resource(Export_Details, '/export_details')
api.add_resource(Username, '/username')
api.add_resource(StartQuiz, '/start_quiz/<int:quiz_id>')
api.add_resource(Admin_Summary, '/admin_summary')
api.add_resource(Admin_User, '/admin_user')
api.add_resource(User_Result, '/user_result')


if __name__=='__main__':
    app.run(debug=True)
 