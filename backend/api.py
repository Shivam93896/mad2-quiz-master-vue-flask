from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_manager, get_jwt_identity, create_access_token,jwt_required, get_jwt
from backend.models import db,User,Subject,Chapter,Quiz,Question,Score
from datetime import datetime
from passlib.hash import bcrypt
from backend.task import*


class User_Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
     
        if not user:
            return {'message':'user does not exist'}, 401
  
        if user and bcrypt.verify(data['password'],user.password):
            access_token=create_access_token(identity=user.username, additional_claims={"user_id":user.id})

            if user.is_admin:
                return {'message':'Admin login successful',
                        'access_token':access_token,
                        'user_id':user.id,
                        'username':user.username },200
            else:
                return {'message':'User login successful',
                        'access_token':access_token,
                        'user_id':user.id,
                        'username':user.username },200
        else:
            return {'message':'Invalid username or password'}, 401    
        
class User_Signup(Resource):
    def post(self):
        data=request.get_json()    
        user=User.query.filter_by(username=data['username']).first()
        if user:
            return {'message':'User already exist'}, 400
        user=User(username=data['username'],
                  email=data['email'],
                  password=bcrypt.hash(data['password']),
                  dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
                  fullname=data['fullname'],
                  qualification=data['qualification'])
        db.session.add(user)
        db.session.commit()
        return {'message':'User signup successful'},200    


class AddSubject(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401
            
        subjects = Subject.query.all()
        sub_json = []
        for subject in subjects:
            chapters = Chapter.query.filter_by(subject_id=subject.id).all()
            chapter_json = []
            for chapter in chapters:
                chapter_json.append({
                    'id':chapter.id,
                    'name':chapter.name,
                    'description':chapter.description
                    })
            sub_json.append({
                'id':subject.id,
                'name':subject.name,
                'description':subject.description,
                'chapters':chapter_json
            })    
        return sub_json, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return {'message':'only admin can access'} , 401
        data = request.get_json()
        subject=Subject(name=data['name'],description=data['description'])
        db.session.add(subject)
        db.session.commit()
        return {'message':'Subject added successfully'},200
                
    @jwt_required()   
    def put(self, sub_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401   
        data = request.get_json()
        subject=Subject.query.filter_by(id=sub_id).first()
        if not subject:
            return {'message':'Subject does not exist'}, 404
        subject.name=data['name']
        subject.description=data['description']
        db.session.commit()
        return {'message':'Subject update successfully'},200
    
    @jwt_required()   
    def delete(self, sub_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401   
        subject=Subject.query.filter_by(id= sub_id).first()
        if not subject:
            return {'message':'Subject does not exist'}, 404
        
        db.session.delete(subject)
        db.session.commit()
        return {'message':'Subject deleted successfully'},200
    
class AddChapter(Resource):
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()    
        if current_user != 'admin':
           return {'message':'only admin can access'},401
        chapters = Chapter.query.all()
        char_json = []
        for chapter in chapters:  
            char_json.append({
            'id':chapter.id,
            'name':chapter.name,
            'description':chapter.description
            })  
        return char_json, 200      

    @jwt_required()
    def post(self,sub_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return {'message':'only admin can access'} , 401
        data = request.get_json()
        subject_id=Subject.query.filter_by(id=sub_id).first()
        chapter=Chapter(name=data['name'],
                        description=data['description'],
                        subject_id=subject_id.id)
        db.session.add(chapter)
        db.session.commit()
        return {'message':'Chapter added successfully'},200
    
    @jwt_required()   
    def put(self, chap_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401   
        data = request.get_json()
        chapter=Chapter.query.filter_by(id=chap_id).first()
        if not chapter:
            return {'message':'Chapter does not exist'}, 404
        chapter.name=data['name']
        chapter.description=data['description']
        db.session.commit()
        return {'message':'Chapter update successfully'},200
    
    @jwt_required()   
    def delete(self, chap_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401   
        chapter=Chapter.query.filter_by(id=chap_id).first()
        if not chapter:
            return {'message':'Chapter does not exist'}, 404
        
        db.session.delete(chapter)
        db.session.commit()
        return {'message':'Chapter deleted successfully'},200

class AddQuiz(Resource):
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()    
       
        quizzes = Quiz.query.all()
        quiz_json = []
        updated = False

        for quiz in quizzes: 
            attempts=None
            if quiz.single_attempt:
                attempts=Score.query.filter_by(quiz_id=quiz.id).count() 
                if attempts is not None and attempts > 0:
                    quiz.is_active=False
                    updated = True

            quiz_json.append({
                'id':quiz.id,
                'name':quiz.name,
                'description':quiz.description,
                'chapter_id':quiz.chapter_id,
                'is_active':quiz.is_active,
                'date':quiz.date.strftime('%Y-%m-%d'),
                'duration':quiz.duration.strftime('%H:%M:%S'),
                'single_attempt':quiz.single_attempt,
                'chapter':quiz.chapter.name,
                'subject':quiz.chapter.subject.name
            }) 
        if updated:
            db.session.commit()    

        return quiz_json, 200        
          
    @jwt_required()
    def post(self):
        current_user=get_jwt_identity()    
        if current_user != 'admin':
           return {'message':'only admin can access'},401 
        data=request.get_json()
        
        chapter=Chapter.query.filter_by(id=data['chapter_id']).first()
        quiz=Quiz(name=data['name'],
                  description=data['description'],
                  chapter_id=chapter.id,
                  date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                  duration=datetime.strptime(data['duration'], '%H:%M:%S').time(),
                  single_attempt = str(data.get('single_attempt', 'false')).lower() == 'true',
                  is_active = str(data.get('is_active', 'true')).lower() == 'true')
        db.session.add(quiz)
        db.session.commit()
        return {'message':'Quiz added succesfully'} ,200
    
    @jwt_required()
    def put(self,quiz_id):
        current_user=get_jwt_identity()    
        if current_user != 'admin':
           return {'message':'only admin can access'},401 
        data = request.get_json()
        quiz=Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message':'Chapter does not exist'}, 404
        quiz.name=data['name']
        quiz.description=data['description']
        quiz.chapter_id=data['chapter_id']
        quiz.date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        quiz.duration=datetime.strptime(data['duration'], '%H:%M:%S').time()
        quiz.single_attempt = str(data.get('single_attempt', 'false')).lower() == 'true'
        db.session.commit()
        return {'message':'Quiz updated succesfully'} ,200

    @jwt_required()   
    def delete(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401   
        quiz=Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message':'Quiz does not exist'}, 404
        
        db.session.delete(quiz)
        db.session.commit()
        return {'message':'Quiz deleted successfully'},200
    

class AddQuestion(Resource):
    @jwt_required()
    def get(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401  
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        question_json = []
        for question in questions:
            question_json.append({
                'id':question.id,
                'question_tag':question.question_tag,
                'question_state':question.question_state,
                'option1':question.option1,
                'option2':question.option2,
                'option3':question.option3,
                'option4':question.option4,
                'correct_option':question.correct_option
            }) 
        return question_json, 200    

    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401 
        data=request.get_json()
        chapter_id = Quiz.query.filter_by(id=quiz_id).first().chapter_id
        question=Question(chapter_id=chapter_id,
                          question_tag=data['question_tag'],
                          question_state=data['question_state'],
                          option1=data['option1'],
                          option2=data['option2'],
                          option3=data['option3'],
                          option4=data['option4'],
                          correct_option=data['correct_option'],
                          quiz_id=quiz_id)        
        db.session.add(question)
        db.session.commit()
        return {'message':'Question added succesfully'} ,200
      

    @jwt_required()
    def put(self, question_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401 
        data=request.get_json() 
        question=Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message':'Question does not exist'}, 404
        question.question_tag=data['question_tag']
        question.question_state=data['question_state']
        question.option1=data['option1']
        question.option2=data['option2']
        question.option3=data['option3']
        question.option4=data['option4']
        question.correct_option=data['correct_option']
        db.session.commit()
        return {'message':'Question updated succesfully'} ,200
    
    @jwt_required()   
    def delete(self, question_id):
        current_user = get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'},401   
        question=Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message':'Question does not exist'}, 404
        
        db.session.delete(question)
        db.session.commit()
        return {'message':'Question deleted successfully'},200

      
class Export_Details(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user == 'admin':
           return {'message':'only user can access'},401 
        claims= get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id) 
        if not user:
            return {'message':'User does not exist'}, 404
        export_scores.apply_async(args=[user_id])
        return {'message':'Export started successfully'}, 200 
    
class Username(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return {'message':'User does not exist'}, 404
        return {'fullname':user.fullname}, 200
        
class StartQuiz(Resource):

    @jwt_required()
    def get(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            return {'message':'only user can access'},401
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message':'User does not exist'}, 404
        
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message':'Quiz does not exist'}, 404
        
        if quiz.single_attempt:
            existing_score = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()
            if existing_score:
                return {'message':'You have already attempted this quiz'}, 400
        
        # return {'message':'Quiz is available for attempt', 'quiz_id': quiz.id}, 200


        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        time_limit = quiz.duration.hour * 3600 + quiz.duration.minute * 60 + quiz.duration.second
        quiz_data = {
            'quiz_id': quiz.id,
            'quiz_name': quiz.name,
            'time_limit': time_limit,
            'questions': [{
                "id": question.id,
                "question_tag": question.question_tag,
                "question_state": question.question_state,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "correct_option": question.correct_option,
                "correct_answer": getattr(question, question.correct_option)
            }for question in questions]
        }
        return quiz_data, 200
    
        
    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user == 'admin':
            return {'message':'only user can access'},401
        
        claims=get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message':'User does not exist'}, 404
        
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message':'Quiz does not exist'}, 404
        
        if quiz.single_attempt:
            existing_score = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()
            if existing_score:
                return {'message':'You have already attempted this quiz'}, 400
        
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.filter_by(id=chapter.subject_id).first()
        questions=Question.query.filter_by(quiz_id=quiz_id).all()
        data=request.get_json()
        score=0
        total_possible_score=len(questions)
        option_map = {'a': 'option1', 'b': 'option2', 'c': 'option3', 'd': 'option4'}

        for question in questions:
            user_answer_option = data.get('correct_option',{}).get(str(question.id))
            user_answer_option = user_answer_option.strip().lower() if user_answer_option else None
            mapped_user_answer = option_map.get(user_answer_option)   
            correct_option = question.correct_option.strip().lower() if question.correct_option else None
            if mapped_user_answer == correct_option:
                score += 1
        percentage = (score / total_possible_score) * 100
        timestamp = datetime.now().date()
        new_score=Score(user_id=user_id,
                        quiz_id=quiz_id,
                        subject_id=subject.id,
                        chapter_id=chapter.id,
                        score = score,
                        total_possible_score= total_possible_score,
                        date=timestamp,
                        percentage=round(percentage,2))       
        db.session.add(new_score)
        db.session.commit()
        
        return{'message':'Quiz completed successfully',
               "score":score,
               "total_possible_score":total_possible_score,
               "precent":percentage },200
    

class User_Result(Resource):
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()
        if current_user == 'admin':
            return {'message':'only user can access'},401
        claims=get_jwt()
        user_id = claims['user_id']
        user=User.query.get(user_id)
        if not user:
            return {'message':'User does not exist'}, 404
        scores=Score.query.filter_by(user_id=user_id).all()
        result=[]
        for score in scores:
            result.append({
                "subject_name":score.subject.name,
                "chapter_name":score.chapter.name,
                "quiz_name":score.quiz.name,
                "score":score.score,
                "percentage":score.percentage,
                "total_possible_score":score.total_possible_score,
                "date":score.date.strftime('%Y-%m-%d %H:%M:%S')


            })
        return result,200

class Admin_Summary(Resource):
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()
        print("currebt_user" , current_user)
        if current_user != 'admin':
           return {'message':'only admin can access'}, 401
        subject_attempts = db.session.query(
            Subject.name,
            db.func.count(Score.user_id)).join(Quiz, Score.quiz_id==Quiz.id).join(Chapter,Quiz.chapter_id==Chapter.id).join(Subject,Chapter.subject_id==Subject.id).group_by(Subject.name).all()
        
        pie_labels=[]
        pie_values=[]
        for subject,count in subject_attempts:
            if count>0:
                pie_labels.append(subject)
                pie_values.append(count)

        topscore = db.session.query(
            Subject.name,
            db.func.max(Score.score)).join(Quiz, Score.quiz_id==Quiz.id).join(Chapter, Quiz.chapter_id==Chapter.id).join(Subject, Chapter.subject_id==Subject.id).group_by(Subject.name).all()
            
        bar_labels = []
        bar_values = []
        for subject, max_score in topscore:
            if max_score is not None:
                bar_labels.append(subject)
                bar_values.append(max_score)  
        return {
            'pie_labels': pie_labels,
            'pie_values': pie_values,
            'bar_labels': bar_labels,
            'bar_values': bar_values
        }, 200      

class Admin_User(Resource):
    @jwt_required()
    def get(self):
        current_user=get_jwt_identity()
        if current_user != 'admin':
           return {'message':'only admin can access'}, 401
        users = User.query.filter_by(is_admin=False).all()
        user_json = []
        for user in users:
            user_json.append({
                'id':user.id,
                'name':user.fullname,
                'email':user.email,
                'username':user.username,
                'qualification':user.qualification,
            })
        return user_json, 200
