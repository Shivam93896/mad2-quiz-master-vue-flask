from celery import shared_task
from datetime import datetime
from backend.models import db,User,Subject,Chapter,Quiz,Score,Question
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import csv
import os
from email import encoders
import smtplib
from jinja2 import Template



def mail_config(to_address,subject,email_message,attachment=None):
    smtp_server_host='localhost'
    smtp_server_port=1025
    sender_email='admin@gmail.com'

    msg= MIMEMultipart()
    msg['From']=sender_email
    msg['To'] = to_address
    msg['Subject']=subject
    msg.attach(MIMEText(email_message,'html'))

    if attachment:
        if os.path.exists(attachment):
            with open(attachment,'rb') as f:
                part=MIMEBase('text','csv')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',f'attachment',filename={os.path.basename})
                msg.attach(part)
        else:
            print('File dose not exist')        
    with smtplib.SMTP(smtp_server_host,smtp_server_port) as server:
        server.sendmail(sender_email,to_address,msg.as_string())          
    print('Email send successfully')  

@shared_task 
def daily_reminder():
    users=User.query.all()    
    quizzes=Quiz.query.all()
    for user in users: 
        if user.is_admin:
            continue
        unattempted_quizzes = []
        for quiz in quizzes:
            attempt=Score.query.filter_by(user_id=user.id,quiz_id=quiz.id).first() 
            if not attempt:
                unattempted_quizzes.append(quiz)
            if unattempted_quizzes:
                html_body=build_html_email(user.username,unattempted_quizzes)
                mail_config(
                    user.email,
                    'Reminder: Complete Your quizzes',
                    html_body
                )
def build_html_email(username,unattempted_quizzes) :
    html_body=f'<p> Hello {username},</p>'
    html_body+='<p>Here are the quizzs you have not attempted:</p>'               
    html_body+='<ul>'
    for quiz in unattempted_quizzes:
        html_body+=f'<li>{quiz.name}</li>'
    html_body+='</ul>'
    html_body+='<p>Please attempt the quizzes as soon as possible.</p>'
    return html_body    


@shared_task
def export_scores(user_id):
    try:
        reports_dir=os.path.join(os.getcwd(),'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        report_file=os.path.join(reports_dir, f'{user_id}_quiz_reports_{datetime.now().strftime("%Y-%m-%d")}.csv')    

        with open(report_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Quiz ID', 'Quiz Title', 'Obtained Marks', 'Total Marks', 'Completion Time'])

            quizzes = db.session.query(
                Quiz.id,
                Quiz.name,
                Score.score.label('obtained_marks'),
                Score.total_possible_score.label('total_marks'),
                Score.date.label('date')
            ).join(Score, Score.quiz_id == Quiz.id).filter(Score.user_id == user_id).all()

            for quiz in quizzes:
                quiz_id , quiz_title, obtained_marks, total_marks, completion_date = quiz
                writer.writerow([
                    quiz_id, quiz_title, obtained_marks, total_marks, completion_date.strftime('%Y-%m-%d') if completion_date else ''
                ])
        user=User.query.get(user_id)
        mail_config(
            user.email,
            'Your Quiz Report',
            'Please find the attached report of quiz attempts',
            attachment=report_file
        )        
    except Exception as e:
        print(e)    

def send_email(user, month, quiz_details, total_quizzes, avg_percentage):
    template_path='templates/report.html'
    with open(template_path, 'r') as template_file:
        template_file=template_file.read()
    template=Template(template_file)
    html_content=template.render(
        user=user,
        month=month,
        quiz_details=quiz_details,
        total_quizzes=total_quizzes,
        avg_percentage=avg_percentage
    )
    mail_config(
        user.email,
        f'Monthly Report for {user.username}',
        html_content
    )



@shared_task
def send_monthly_report():
    users=User.query.filter_by(is_admin=False).all()
    for user in users:
        month = datetime.now().strftime('%B')   
        quiz_details= Score.query.filter_by(user_id=user.id).all()
        total_quizzes= len(quiz_details)     
        if total_quizzes > 0 :
            avg_percentage = sum(score.percentage for score in quiz_details) / total_quizzes
        else:
            avg_percentage = 0
        send_email(user, month, quiz_details, total_quizzes)    