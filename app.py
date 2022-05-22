from flask import jsonify, Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from models import setup_db, question, user, score, insertInDb, update, delete
import uuid
from flask_cors import CORS
import json
import random
from werkzeug.utils import secure_filename
import os
# from flask_jwt import JWT, jwt_required


app = Flask(__name__)
cors = CORS(app)
app.debug = True
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = setup_db(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vjfdxyrk:sEJAp9eqEXryY-IhhWF9Ncmfl5XJVf8_@tyke.db.elephantsql.com/vjfdxyrk'
# Models



# get 
@app.route('/')
def index():
    return 'Index Page'

@app.route('/user', methods=['GET'])
def getUsers():
    print('form: ', request)
    student = user.query.get({"id": request.form['id']})
    print('student: ', student)
    data = {
        "firstName": student.first_name,
        "userName": student.user_name,
        "isAdmin": student.is_admin,
        "lastName": student.last_name,
        "id": student.id 
    }
    # for usniqueUser in users: 
    #     data.append({
    #         "firstName": usniqueUser.first_name,
    #         "lastName": usniqueUser.last_name,
    #         "id": usniqueUser.id 
    #     })
    jsonStuennt = jsonify(data)
    print('jsonStuennt: ', jsonStuennt)
    
    return jsonStuennt

@app.route('/signIn', methods=['POST'])
def signIn():
    # print('form: ', request)
    print('------request: ', request)
    decodedData = json.loads(request.data.decode('UTF-8'))
    print('------decodedData: ', decodedData)
    userName = decodedData['userName']

    print('<<<<<<<------userName: ', userName)
    studentFromDb = user.query.filter(user.user_name == userName).first()
    print('<<<<<<<------student: ', studentFromDb)
    print('<<<<<<<------student.password: ', studentFromDb.password)
    print('<<<<<<<------request: ', request)
    print('<<<<<<<------request.json: ', request.json)
    
    if studentFromDb:

        # student = user.query.get({"id": student.strip('<')[0]})
        if decodedData['password'] == str(studentFromDb.password):
            token = random.randrange(99999999)
            try: 
                updateStudent = user.query.filter(user.user_name == userName).one_or_none()
                
                updateStudent.token = str(token)
                print('---updateStudent: ', updateStudent)
                print('---updateStudent.token: ', updateStudent.token)
                db.session.flush()
                db.session.commit()
            except Exception as e:
                
                db.session.rollback()
                print('error:', e)
            finally:
                print('----finally')
                
            print('student----->>>>: ', studentFromDb)
            data = {
                "token": studentFromDb.token,
                "firstName": studentFromDb.first_name,
                "userName": studentFromDb.user_name,
                "isAdmin": studentFromDb.is_admin,
                "lastName": studentFromDb.last_name,
                "token": token,
                "id": studentFromDb.id 
            }
            jsonStuennt = jsonify(data)
            print('jsonStuennt: ', jsonStuennt)
            db.session.close()
            return jsonStuennt
    return 'not authenticated'



@app.route('/user', methods=['POST'])
def createUser():
    print('creating user')
    decodedData = json.loads(request.data.decode('UTF-8'))
    print('request.data: ', request.data)
    print('------decoded request: ', decodedData)
    print('request.form[]', decodedData['firstName'])
    print('uuid.uuid4()', uuid.uuid4())
    # request.form['userName']
    user.query

    # stmt = (
    #     insert(user).values(user_name='majed12', password='123',id='2')
    # )
    admin = False 
    try:
        if decodedData['adminKey'] == '123':
            admin = True
    
    except:
        pass
    newUser = user(
        user_name=decodedData['userName'],
        password=decodedData['password'], 
        first_name=decodedData['firstName'], 
        last_name=decodedData['lastName'], 
        is_admin= admin,
        id=str(uuid.uuid4())
        )
    insertInDb(newUser)
    # print('stmt', stmt)
    return 'success'

@app.route('/question/<int:token>', methods=['POST'])
def createQuestion(token):
    print('token : -<<<', token)
    decodedData = json.loads(request.data.decode('UTF-8'))
    print('request.data: ', request.data)
    print('------decoded request: ', decodedData)
    try: 
        studentFromDb = user.query.filter(user.token == str(token)).first()
        print("studentFromDb: ", studentFromDb)

        if studentFromDb:
            print('logged')
            newQuestion = question(
            question=decodedData['question'],
            answerA= decodedData['answerA'], 
            answerB=decodedData['answerB'], 
            answerC=decodedData['answerC'], 
            answerD=decodedData['answerD'], 
            answerCorrect=decodedData['answerCorrect'], 
            picture_path=decodedData['picture_path'],
            hint=decodedData['hint'],
            id=str(uuid.uuid4())
            )
            insertInDb(newQuestion)

            return 'success'
        return 'failed'
    except Exception as e:
                
                print(e)
                return 'failed'

@app.route('/questions', methods=['GET'])
def getQuestions():
    # print('token : -<<<', token)
    try: 
        questionsFromDb = question.query.all()
        print("questionsFromDb: ", questionsFromDb)
    
        if questionsFromDb:
            readyQuestions = []
            for questionFromDb in questionsFromDb:
                print('questionFromDb: ', questionFromDb)
                data = {
                    "question": questionFromDb.question,
                    "hint": questionFromDb.hint,
                    "answerA": questionFromDb.answerA,
                    "answerB": questionFromDb.answerB,
                    "answerC": questionFromDb.answerC,
                    "answerD": questionFromDb.answerD,
                    "answerCorrect": questionFromDb.answerCorrect,
                    "image_url": questionFromDb.picture_path,
                    "id": questionFromDb.id 
                }
                readyQuestions.append(data)
                print('data: ', data)
            jsonQuestions = jsonify(readyQuestions)
            return (jsonQuestions)
        #     print('logged')
        #     return 'success'
        return 'failed'
    except Exception as e:
                
                print(e)
                return 'failed'




@app.route('/question/<int:token>', methods=['PATCH'])
def deleteQuestion(token):
    print('token : -<<<', token)
    decodedData = json.loads(request.data.decode('UTF-8'))
    print('request.data: ', request.data)
    print('------decoded request: ', decodedData)
    try: 
        studentFromDb = user.query.filter(user.token == str(token)).first()
        print("studentFromDb: ", studentFromDb)

        if studentFromDb:
            print('logged')
            questionFromDb = question.query.filter(question.id == str(decodedData['id'])).first()
            # questionFromDb = Movies.query.order_by(id).all()
            print('delete question: ', questionFromDb)
            delete(questionFromDb)
            # newQuestion = question(
            # question=decodedData['question'],
            # answerA= decodedData['answerA'], 
            # answerB=decodedData['answerB'], 
            # answerC=decodedData['answerC'], 
            # answerD=decodedData['answerD'], 
            # answerCorrect=decodedData['answerCorrect'], 
            # picture_path=decodedData['picture_path'],
            # hint=decodedData['hint'],
            # id=str(uuid.uuid4())
            # )
            # insertInDb(newQuestion)

            return 'success'
        return 'failed'
    except Exception as e:
                
                print(e)
                return 'failed'

@app.route('/scores', methods=['GET'])
def getScores():
    print('form: ', request)
    scores = score.query.all()
    print('scores: ', scores)
    data = []
    for usniqueScore in scores: 
        student = user.query.get({"id": usniqueScore.user_id})
        # print('student: ', student)
        data.append({
            "score": usniqueScore.user_score,
            "date": usniqueScore.date,
            "userId": usniqueScore.user_id,
            "userName": student.user_name,
            "id": usniqueScore.id 
        })
         
    jsonScores = jsonify(data)
    # print('user: ', users[0])
    
    return jsonScores    

@app.route('/score/<int:token>', methods=['POST'])
def createScore(token):
    print('token : -<<<', token)
    decodedData = json.loads(request.data.decode('UTF-8'))
    print('request.data: ', request.data)
    print('------decoded request: ', decodedData)
    try: 
        studentFromDb = user.query.filter(user.token == str(token)).first()
        print("studentFromDb: ", studentFromDb)

        if studentFromDb:
            print('logged')
            newScore = score(
                user_score= decodedData['score'],
                date= decodedData['date'],
                user_id= str(studentFromDb.id),
                id=str(uuid.uuid4())
            )
            insertInDb(newScore)

            return newScore.id
        return 'failed'
    except Exception as e:
                
                print(e)
                return 'error'