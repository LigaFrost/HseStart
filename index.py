import sqlite3
import vk_api
import random
from random import choice
from flask import Flask,flash, render_template, request, redirect, session, url_for, Markup
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPG'])
app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "ksjdfkosYFIOASDFHKASDFYHKASDJFHPFYHPKASDFH;JKsdlkjfhqouryu134y8998"
global auth_student

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
			#Students#

@app.route("/student")
@app.route("/student/")
def single():
    session['countyes']=0
    session['countno']=0
    if session['student']==auth_student[0] or session['student']!=-1:
        student=get_student(auth_student[0])
        dic={"id_s": student[0], "first_name":student[1], "last_name":student[3], "middle_name":student[2],"email":student[4], "date_of_birth":student[6], "city":student[5], "vk":student[7],"inst":student[8],  "password" :student[9], "image":student[10]}
        return render_template('HseStart.html', student=dic, url_for=url_for)
    else: return redirect('/signin')

@app.route('/')
def students():
    return render_template('HseStart_SignIn.html')

def get_students():
	studentsDB=sqlite3.connect("students_BI.db")
	cursor_s=studentsDB.cursor()
	cursor_s.execute("SELECT * FROM students ORDER BY id_s")
	students=cursor_s.fetchall()
	return students

def get_student(student_id):
	studentsDB=sqlite3.connect("students_BI.db")
	cursor_s=studentsDB.cursor()
	cursor_s.execute("SELECT * FROM students WHERE id_s=?", ([student_id]))
	student=cursor_s.fetchone()
	return student

def add_student(first_name, middle_name, last_name, e_mail, city, date_of_birth, vk_href, inst_href, password, image_href):
    studentsDB=sqlite3.connect("students_BI.db")
    cursor_s=studentsDB.cursor()
    cursor_s.execute("SELECT * FROM students ORDER BY id_s")
    students=cursor_s.fetchall()
    try:
        id_s=students[-1][0]+1
    except Exception: id_s=0
    e_mail=str(e_mail)
    password=str(password)

    cursor_s.execute(" INSERT INTO students VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id_s, first_name, middle_name, last_name, e_mail, city, date_of_birth, vk_href, inst_href, password, image_href))
    studentsDB.commit()

			#End students#

@app.route('/curators')
@app.route('/curators/')
def curators():
    session['countyes']=0
    session['countno']=0
    if session['student']!=-1:
        return render_template("HseStart_Curators.html", curators=curators)
    else: return redirect('/signin')

def get_curators(): 
        cursor_c=curatorsDB.cursore() 
        cursor_c.execute("SELECT * FROM curators ORDER BY id")
        curators=cursor_c.fetchall() 
        return curators

			#Contacts#

@app.route('/contacts')
@app.route('/contacts/')
def contacts():
    session['countyes']=0
    session['countno']=0
    return render_template("HseStart_Contacts.html")
            #End contacts#

            #Teachers#

@app.route('/teachers')
@app.route('/teachers/')
def teachers():
    session['countyes']=0
    session['countno']=0
    if session['student']!=-1:
        return render_template("HseStart_Teachers.html")
    else: return redirect('/signin')
    
			#Auth#

@app.route('/signin', methods=["GET","POST"])
@app.route('/signin/', methods=["GET","POST"])
def login():
    error = ''
    global auth_student
    #try:	
    if request.method == "POST":		
        email = str(request.form.get('email'))
        password =str(request.form.get('password'))
        studentsDB=sqlite3.connect("students_BI.db")
        cursor_s=studentsDB.cursor()
        if cursor_s.execute("SELECT * FROM students WHERE email=?",([email])) and cursor_s.execute("SELECT * FROM students WHERE password=?",([password])):
            auth_student=cursor_s.fetchone()
            session['student'] = auth_student[0]
            session['countyes']=0
            session['countno']=0
            return redirect("/student")

        elif attempted_email == "hsestart@hse.ru" and attempted_password == "hsestart2018":
                session['admin'] = True
                return redirect("/admin")
		
        else:
            flash ("Неверный Логин/Пароль, попробуйте снова!")
            session['student']=-1
            session['admin']==False
            return redirect("/signin")
                

    return render_template("HseStart_SignIn.html", error = error)

    #except Exception as e:
        #flash(e)
    #    return render_template("HseStart_SignIn.html", error = error)


@app.route('/signup', methods=['POST','GET'])
@app.route('/signup/', methods=['POST','GET'])
def signup():
    error = ''
    #try:    
    if request.method == "POST":
        dic={"first_name":request.form.get('first_name'), "last_name":request.form.get('last_name'), "middle_name":request.form.get('middle_name'),"email":request.form.get('email'), "date_of_birth":request.form.get('date_of_birth'), "city":request.form.get('city'), "vk":request.form.get('vk'),"inst":request.form.get('inst'),  "password" :request.form.get('password'), "image":request.files.get('image_href')}
        if 'image_href' not in request.files:
            flash('No file part')
            return redirect('/signin')
                    
        else:
            if 'file' not in request.files:
                dic["image"]=""
                file = request.files['image_href']
                
                if file.filename == '':
                        dic["image"]=""
                        
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    dic["image"]=filename
                    add_student(dic['first_name'], dic['middle_name'], dic['last_name'], dic['email'], dic['city'], dic['date_of_birth'], dic['vk'], dic['inst'], dic['password'], filename)
                    return redirect('/signin')
                    

    return render_template("HseStart_SignUp.html", error = error)

    #except Exception as e:
    #    flash(e)
    #    return render_template("HseStart_SignUp.html", error = error)

                #End Auth#

                #Quizz#

vk=vk_api.VkApi(token='ef546a6af000449719ceb18b81904ccad09311b9e1836b14d6af6b9a9048db17dbf37037505a57e8b587c')

members = vk.method('groups.getMembers?group_id=45231426&fields=sex,photo_max')['items']
def getUser(sex):
    u = random.choice(members)
    print ('sex')
    if u["photo_max"] == "https://vk.com/images/camera_200.png" or u["photo_max"] == "https://vk.com/images/deactivated_200.png"or u['sex']!=sex:
        return getUser(sex)
    return u

@app.route('/logout')
def logout():
    session['student']=-1
    return redirect('/signin')
@app.route('/quiz')
def index():
    message = ""
    if session['student']==auth_student[0]:
        if 'final' in session:
            if session['final']=='krasava':
                message='Правильно!'
            if session['final']=='notkrasava':
                message='Неверно, попробуйте снова!'
        if not 'countno'  in session:
            session['countno']=0
        if not 'countyes'  in session:
            session['countyes']=0
        sex=random.randint(1,2)
        peoples = [getUser(sex),getUser(sex),getUser(sex)]
        chosenID = random.choice(peoples)
        session['YouHaveToChose']=str(chosenID['id'])
        name=chosenID['first_name']+' '+chosenID['last_name']
        a=render_template('HseStart_Quiz.html',people=peoples[0],people1=peoples[1],people2=peoples[2],name=name,message=message,countyes=session['countyes'],countno=session['countno'])
        return a
    else: return redirect('/signin')

@app.route('/checker')
def check():
    chosen=request.args['id']
    if chosen==session['YouHaveToChose']:
        session['YouHaveToChose']='ohfsdjfdsjknfkjnfs'
        session['final']='krasava'
        session['countyes']+=1
        return redirect('/quiz')
    else:
        session['countno']+=1
        session['YouHaveToChose']='ohfsdjfdsjknfkjnfs'
        session['final']='notkrasava'
        return redirect('/quiz')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

                #End Quiz#


app.run(port=1602)
