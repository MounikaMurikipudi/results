from flask import Flask,request,redirect,render_template,url_for,flash,session
from flask_mysqldb import MySQL
from flask_session import Session
from otp import genotp
from cmail import sendmail
from tokenreset import token
import random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import io
from io import BytesIO
app=Flask(__name__)
app.secret_key='admin@123'
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='admin'
app.config['MYSQL_DB']='sonuresults'
Session(app)
mysql=MySQL(app)
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        name=request.form['name']
        emailid=request.form['emailid']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into contactus(name,emailid,message) values(%s,%s,%s)',[name,emailid,message])
        mysql.connection.commit()
    return render_template('myresult.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        user=request.form['AdminName']
        Email=request.form['email']
        password=request.form['password']
        ccode=request.form['Ccode']
        code='admin@123'
        cursor=mysql.connection.cursor()
        if code==code:
            cursor.execute('select user from a_register')
            data=cursor.fetchall()
            if (user,) in data:
                flash('user already exits')
                return render_template('register.html')
            cursor.execute('select email from a_register')
            e_data=cursor.fetchall()
            cursor.close()
            if (Email,) in e_data:
                flash('email already exit')
                return render_template('register.html')
            otp=genotp()
            subject='Thanks for registering to the application'
            body=f'Use this otp to registre{otp}'
            sendmail(Email,subject,body)
            return render_template('otp.html',otp=otp,user=user,Email=Email,password=password,ccode=ccode)
        else:
            flash('Invaild Secret code')
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('dash'))
    if request.method=='POST':
        AdminName=request.form['AdminName']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*)from a_register where user=%s and password=%s',[AdminName,password])
        count=cursor.fetchone()[0]
        if count==0:
            flash('Invalid user or password')
            return render_template('a_login.html')
        else:
            session['user']=AdminName             #session use to restrick homepage
            return redirect(url_for('dash'))    #linkhome restricked
    return render_template('a_login.html')
@app.route('/dash')
def dash():
    if session.get('user'):
        return render_template('dash.html')
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('index'))
    else:
        flash('already logged out')
        return redirect(url_for('index'))
        
@app.route('/otp/<otp>/<user>/<Email>/<password>/<ccode>',methods=['GET','POST'])
def otp(otp,user,Email,password,ccode):
    if request.method=='POST':
        uotp=request.form['otp']
        print(otp)
        print(uotp)
        if otp==uotp:
            cursor=mysql.connection.cursor()
            cursor.execute('insert into a_register values(%s,%s,%s,%s)',(user,Email,password,ccode))
            mysql.connection.commit()
            cursor.close()
            flash('Successfully Detail Register')
            return redirect(url_for('login'))
        else:
            flash('Worng otp')
            return render_template('otp.html',otp=otp,user=user,Email=Email,password=password,ccode=ccode)
@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    if session.get('user'):
        if request.method=='POST':
            studentid=request.form['studentid']
            studentname=request.form['studentname']
            section=request.form['section']
            mobile=request.form['mobile']
            Address=request.form['Address']
            Department=request.form['Department']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into addstu value(%s,%s,%s,%s,%s,%s)',(studentid,studentname,section,mobile,Address,Department))
            cursor.connection.commit()
            flash(f' added successfully')
            return redirect(url_for('dash'))
        return render_template('addstudent.html')
    else:
        return redirect(url_for('login'))
@app.route('/addsubject',methods=['GET','POST'])
def addsubject():
    if session.get('user'):
        if request.method=='POST':
            courseid=request.form['courseid']
            coursetitle=request.form['coursetitle']
            mmark=request.form['mmark']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into addsub value(%s,%s,%s)',(courseid,coursetitle,mmark))
            cursor.connection.commit()
            flash(f' added successfilly')
            return redirect(url_for('dash'))
        return render_template('addsubject.html')
    else:
        return redirect(url_for('login'))
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        user=request.form['id']
        cursor=mysql.connection.cursor()
        cursor.execute('select user from a_register')
        data=cursor.fetchall()
        if(user,)in data:
            cursor.execute('select email from a_register where user=%s',[user])
            data=cursor.fetchone()[0]
            print(data)
            cursor.close()
            subject='Reset Password for {email}'
            body=f'Reset the password using {request.host+url_for("createpassword",token=token(user,200))}'
            sendmail(data,subject,body)
            flash('Reset link sent to your mail')
            return redirect(url_for('login'))
        else:
            return 'Invalid user'
    return render_template('Forgot.html')
@app.route('/createpassword/<token>',methods=['GET','POST'])
def createpassword(token):
        try:
            s=Serializer(app.config['SECRET_KEY'])
            user=s.loads(token)['user']
            if request.method=='POST':
                npass=request.form['npassword']
                cpass=request.form['cpassword']
                if npass==cpass:
                    cursor=mysql.connection.cursor()
                    cursor.execute('update a_register set password=%s where user=%s',[npass,user])
                    mysql.connection.commit()
                    return 'Password reset Successfull'
                else:
                    return 'Password mismatch'
            return render_template('newpassword.html')
        except Exception as e:
            print(e)
            return 'Link Expired try again'
@app.route('/addsemresult',methods=['GET','POST'])
def addsemresult():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT studentid from addstu')
        data=cursor.fetchall()
        cursor.execute('SELECT COURSEID FROM addsub')
        cdata=cursor.fetchall()
        if request.method=='POST':
            id1=request.form['id']
            course=request.form['course']
            semt=request.form['semt']
            smarks=request.form['smarks']
            section=request.form['section']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into semresults value(%s,%s,%s,%s,%s)',(id1,course,semt,smarks,section))
            cursor.connection.commit()
            flash(f'added successfilly')
            return redirect(url_for('dash'))
        return render_template('addsemresult.html',data=data,cdata=cdata)
    else:
        return redirect(url_for('login'))
@app.route('/addinternalresult',methods=['GET','POST'])
def addinternalresult():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT studentid from addstu')
        data=cursor.fetchall()
        cursor.execute('SELECT COURSEID FROM addsub')
        cdata=cursor.fetchall()
        if request.method=='POST':
            id1=request.form['id']
            course=request.form['course']
            int1=request.form['int1']
            int2=request.form['int2']
            imarks1=request.form['imarks1']
            imarks2=request.form['imarks2']
            section=request.form['section']
            cursor=mysql.connection.cursor()
            cursor.execute('insert into internalresults value(%s,%s,%s,%s,%s,%s,%s)',(id1,course,int1,int2,imarks1,imarks2,section))
            cursor.connection.commit()
            flash(f'added successfilly')
            return redirect(url_for('dash'))
        return render_template('addinternalresult.html',data=data,cdata=cdata)
    else:
        return redirect(url_for('login'))
@app.route('/studentrecord')
def studentrecord():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from addstu')
        students_data=cursor.fetchall()
        print(students_data)
        cursor.close()
        return render_template('studentrecord.html',data=students_data)
    else:
        return redirect(url_for('login'))
@app.route('/updaterecords/<studentido>',methods=['GET','POST'])
def updaterecords(studentido):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select studentid,studentname,section,mobile,Address,Department from addstu where studentid=%s',[studentido])
        data=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
           studentid=request.form['studentid']
           studentname=request.form['studentname']
           section=request.form['section']
           mobile=request.form['mobile']
           Address=request.form['Address']
           Department=request.form['Department']
           cursor=mysql.connection.cursor()
           cursor.execute('update addstu set studentid=%s,studentname=%s,section=%s,mobile=%s,Address=%s,Department=%s where studentid=%s',[studentid,studentname,section,mobile,Address,Department,studentido])
           mysql.connection.commit()
           cursor.close()
           flash('Records updated successfully')
           return redirect(url_for('studentrecord'))
        return render_template('update.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/deleterecords/<stdid>')
def deleterecords(stdid):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from addstu where studentid=%s',[stdid])
    mysql.connection.commit()
    cursor.close()
    flash('Records deleted successfully')
    return redirect(url_for('studentrecord'))
@app.route('/subjectrecord')
def subjectrecord():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from addsub')
        data=cursor.fetchall()
        print(data)
        cursor.close()
        return render_template('subjectrecord.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/subupdate/<courseido>',methods=['GET','POST'])
def subupdate(courseido):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select courseid,coursetitle,maxmarks from addsub where courseid=%s',[courseido])
        data=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
           courseid=request.form['courseid']
           coursetitle=request.form['coursetitle']
           maxmarks=request.form['mmarks']
           cursor=mysql.connection.cursor()
           cursor.execute('update addsub set courseid=%s,coursetitle=%s,maxmarks=%s where courseid=%s',[courseid,coursetitle,maxmarks,courseido])
           mysql.connection.commit()
           cursor.close()
           flash('Records updated successfully')
           return redirect(url_for('subjectrecord'))
        return render_template('subupdate.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/delete/<courseid>')
def delete(courseid):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from addsub where courseid=%s',[courseid])
    mysql.connection.commit()
    cursor.close()
    flash('Records deleted successfully')
    return redirect(url_for('subjectrecord'))

@app.route('/editsemresult',methods=['GET','POST'])
def editsemresult():
    if session.get('user'):
        if request.method=='POST':
            search=request.form['search']
            cursor=mysql.connection.cursor()
            cursor.execute('select a.courseid,a.studentid,a.semister,a.semmarks,i.Internal1,i.internalmarks1,i.Internal2,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid')
            data=cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return render_template('showsem.html',data=data)
        return render_template('showsem.html')
    else:
        return redirect(url_for('login'))
@app.route('/deletes/<courseid>/<studentid>')
def deletes(courseid,studentid):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from semresults where courseid=%s and studentid=%s',[courseid,studentid])
    cursor.execute('delete from internalresults where courseid=%s and studentid=%s',[courseid,studentid])
    mysql.connection.commit()
    cursor.close()
    flash('Records deleted successfully')
    return redirect(url_for('dash'))
@app.route('/editinternalresult',methods=['GET','POST'])
def editinternalresult():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select i.courseid,i.studentid,i.Internal1,i.internalmarks1,i.Internal2,i.internalmarks2 from addstu as s inner join internalresults as i on s.studentid=i.studentid')
        data=cursor.fetchall()
        if request.method=='POST':
            search=request.form['search']
            cursor=mysql.connection.cursor()
            cursor.execute('select a.courseid,a.studentid,a.semister,a.semmarks,i.Internal1,i.internalmarks1,i.Internal2,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s',[search])
            data=cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            return render_template('showinternal.html',data=data)
        return render_template('showinternal.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/deleted/<courseid>/<studentid>')
def deleted(courseid,studentid):
    cursor=mysql.connection.cursor()
    cursor.execute('delete from internalresults where courseid=%s and studentid=%s',[courseid,studentid])
    mysql.connection.commit()
    cursor.close()
    flash('Records deleted successfully')
    return redirect(url_for('dash'))

@app.route('/viewcontactus')
def contactusview():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from contactus order by date desc')
        data=cursor.fetchall()
        return render_template('viewcontactus.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/sem/<semt>',methods=['GET','POST'])
def sem(semt):
    g_total=None
    if request.method=='POST':
        search=request.form['search']
        cursor=mysql.connection.cursor()
        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,semt])
        data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,semt])
        marks_data=cursor.fetchall()
        final_data=[i[0]+i[1]+i[2] for i in marks_data]
        real_data=[j+(final_data[i],) for i,j in enumerate(data)]
        g_total=sum(final_data)
        mysql.connection.commit()
        cursor.close()
        return render_template('sem1.html',real_data=real_data,g_total=g_total)
    return render_template('sem1.html')




@app.route('/report',methods=['GET','POST'])
def report():
    if request.method=='POST':
        search=request.form['search']
        cursor=mysql.connection.cursor()
        
        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem1'])
        sem1_data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem1'])
        sem1_marks_data=cursor.fetchall()
        sem1_final_data=[i[0]+i[1]+i[2] for i in sem1_marks_data]
        sem1_real_data=[j+(sem1_final_data[i],) for i,j in enumerate(sem1_data)]
        sem1_g_total=sum(sem1_final_data)

        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem2'])
        sem2_data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem2'])
        sem2_marks_data=cursor.fetchall()
        sem2_final_data=[i[0]+i[1]+i[2] for i in sem2_marks_data]
        sem2_real_data=[j+(sem2_final_data[i],) for i,j in enumerate(sem2_data)]
        sem2_g_total=sum(sem2_final_data)

        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem3'])
        sem3_data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem3'])
        sem3_marks_data=cursor.fetchall()
        sem3_final_data=[i[0]+i[1]+i[2] for i in sem3_marks_data]
        sem3_real_data=[j+(sem3_final_data[i],) for i,j in enumerate(sem3_data)]
        sem3_g_total=sum(sem3_final_data)

        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem4'])
        sem4_data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem4'])
        sem4_marks_data=cursor.fetchall()
        sem4_final_data=[i[0]+i[1]+i[2] for i in sem4_marks_data]
        sem4_real_data=[j+(sem4_final_data[i],) for i,j in enumerate(sem4_data)]
        sem4_g_total=sum(sem4_final_data)

        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem5'])
        sem5_data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem5'])
        sem5_marks_data=cursor.fetchall()
        sem5_final_data=[i[0]+i[1]+i[2] for i in sem5_marks_data]
        sem5_real_data=[j+(sem5_final_data[i],) for i,j in enumerate(sem5_data)]
        sem5_g_total=sum(sem5_final_data)

        cursor.execute('select a.studentid,a.courseid,a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem6'])
        sem6_data=cursor.fetchall()
        cursor.execute('select a.semmarks,i.internalmarks1,i.internalmarks2 from addstu as s inner join semresults as a on s.studentid=a.studentid  inner join internalresults as i on s.studentid=i.studentid and i.courseid=a.courseid where s.studentid=%s and a.semister=%s',[search,'sem6'])
        sem6_marks_data=cursor.fetchall()
        sem6_final_data=[i[0]+i[1]+i[2] for i in sem6_marks_data]
        sem6_real_data=[j+(sem6_final_data[i],) for i,j in enumerate(sem6_data)]
        sem6_g_total=sum(sem6_final_data)

        g_total=sem1_g_total+sem2_g_total+sem3_g_total+sem3_g_total+sem4_g_total+sem5_g_total+sem6_g_total
        
        mysql.connection.commit()
        cursor.close()
        return render_template('report.html',std=search,sem1_g_total=sem1_g_total,sem2_g_total=sem2_g_total,sem3_g_total=sem3_g_total,sem4_g_total=sem4_g_total,sem5_g_total=sem5_g_total,sem6_g_total=sem6_g_total,g_total=g_total)
    
    
    return render_template('report.html')

app.run(use_reloader=True,debug=True)
    
