import sqlite3
import vk_api
import random
from random import choice
from flask import Flask,flash, render_template, request, redirect, session, url_for, Markup
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "ksjdfkosYFIOASDFHKASDFYHKASDJFHPFYHPKASDFH;JKsdlkjfhqouryu134y8998"


			#Students#
@app.route("/student")
def single():
	students=get_students()
	return render_template('HseStart.html')
@app.route('/')
def students():
	students=get_students()
	return render_template('HseStart_SignIn.html')

def get_students():
	studentsDB=sqlite3.connect("students_BI.db")
	cursor_s=studentsDB.cursor()
	cursor_s.execute("SELECT * FROM students ORDER BY id")
	students=cursor_s.fetchall()
	return students

def get_student(student_id):
	studentsDB=sqlite3.connect("students_BI.db")
	cursor_s.execute("SELECT * FROM students WHERE id=student_id")
	student=cursor_s.fetchone()
	return student

def add_student(first_name, middle_name, last_name, e_mail, city, date_of_birth, vk_href, inst_href, password, image_href):
    studentsDB=sqlite3.connect("students_BI.db")
    cursor_s.execute("SELECT * FROM students ORDER BY id")
    students=cursor_s.fetchall()
    id=students[-1][0]+1

    cursor_s.execute(""" INSERT INTO students
    						VALUES(id, first_name, middle_name, last_name, e_mail, city, date_of_birth, vk_href, inst_href, password, image_href)
    						""")
    studentsDB.commit()
'''
@app.route('/')
def studentpage():
        student=get_student(auth_student[0])
        render_template()
'''

			#End students#

@app.route('/curators')
@app.route('/curators/')
def curators():
                return render_template("HseStart_Curators.html", curators=curators)

def get_curators(): 
        cursor_c=curatorsDB.cursore() 
        cursor_c.execute("SELECT * FROM curators ORDER BY id")
        curators=cursor_c.fetchall() 
        return curators


                   



			#Contacts#

@app.route('/contacts')
@app.route('/contacts/')
def contacts():
	return render_template("HseStart_Contacts.html")


			#Auth#

@app.route('/signin', methods=["GET","POST"])
@app.route('/signin/', methods=["GET","POST"])
def login():
    error = ''
    try:	
        if request.method == "POST":		
                attempted_email = request.form['e-mail']
                attempted_password =(request.form['password'])
                if cursor.execute("SELECT * FROM students WHERE e_mail=?",([attempted_email])) and cursor.execute("SELECT * FROM students WHERE password=?",([attempted_password])):
                                student=cursor.fetchone()
                                global auth_student
                                auth_student=student
                                id_student=student[0]
                                session['student'] = id_student
                                return redirect("/quiz")

                elif attempted_email == "hsestart@hse.ru" and attempted_password == "hsestart2018":
                        session['admin'] = True
                        return redirect("/admin")
				
                else:
                        flash ("Неверный Логин/Пароль, попробуйте снова!")
                        session['student'] = None
                        session['admin']==False
                        return redirect("/signin")
                

        return render_template("HseStart_SignIn.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("HseStart_SignIn.html", error = error)


@app.route('/signup', methods=['POST','GET'])
@app.route('/signup/', methods=['POST','GET'])
def sign_up():
                first_name=request.form['first_name']
                last_name=request.form['last_name']
                middle_name=request.form['middle_name']
                email = request.form['email']
                date_of_birth=request.form['date_of_birth']
                city=request.form['city']
                vk=request.form['vk']
                inst=request.form['inst']
                password = request.form['password']
                image=request.files['image_href']
                if 'image' not in request.files:
                        flash('No file part')
                        return redirect('/signup')
                image = request.files['image']
                    
                if image.filename == '':
                        flash('No selected file')
                        return redirect("/signup")
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                    
                        add_student(first_name, middle_name, last_name, email, city, date_of_birth, vk, inst, password, image)
                        students=get_students()
                return render_template("HseStart_SignUp.html")


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
        session['student']=None
        return redirect('/signin')
@app.route('/quiz')
def index():
    message = ""
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


app.run(port=1601)
