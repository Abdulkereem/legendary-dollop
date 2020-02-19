from flask import flash, request, redirect, render_template, session, abort, make_response, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
import random
import smtplib
import time

import pymysql
from datetime import datetime

db_name = "bank"
table = "user_reg"
table2 = "admin_reg"
Acc ="WT012020"

# creating database connection
def sql_conn():
    con = pymysql.connect(host="localhost", user="root", password="", database=db_name)
    return con


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin_signup.html')

@app.route('/admin_signup1',methods=['POST'])
def admin_signup1(): # admin sign up
    email = request.form.get('email')
    fname = request.form.get('fname')
    gender = request.form.get('gender')
    lname = request.form.get('lname')
    password = generate_password_hash(request.form.get('password'))
    contact = request.form.get('contact')


    conn = sql_conn()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO ' + table2 + ' VALUES (%s,%s, %s, %s, %s,%s, %s)',
                   ("", fname, lname, gender, email, contact, password))
    cursor.close()
    conn.commit()
    conn.close()

    flash("Account Created Successfully")
    return redirect('/')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup1',methods=['POST'])
def signup1(): # user sign up
    email = request.form.get('email')
    fname = request.form.get('fname')
    gender = request.form.get('gender')
    lname = request.form.get('lname')
    password = generate_password_hash(request.form.get('password'))
    contact = request.form.get('contact')

    date_format = "%Y-%m-%d"
    reg_date = datetime.today().strftime(date_format)

    conn = sql_conn()
    cursor = conn.cursor()

    cursor.execute('select * from '+ table+' where email=%s',(email))
    row = cursor.fetchone()
    if row:
        flash("Account with this email exists already")
        return redirect('/signup')


    else:


        cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)',
                       ("", fname, lname, gender, email, contact, password, reg_date,"", "","Active"))
        cursor.close()
        conn.commit()
        conn.close()

        flash("Account Created Successfully")
        return redirect('/')

@app.route('/login')
def login():
    return redirect("/")

@app.route('/login1',methods=['POST','GET'])
def login1():
    global role,email,password
    details = request.form
    email = details["inputEmail"]
    password = details["inputPassword"]
    role = details['option']
    if details['option'] =='Admin':

        if request.method == 'POST':
            if email and password:
                # check user exists
                conn = sql_conn()
                cursor = conn.cursor()
                sql = "SELECT * FROM admin_reg WHERE email=%s"
                sql_where = (email,)
                cursor.execute(sql, sql_where)
                row = cursor.fetchone()
                if row:

                    if check_password_hash(row[6], password):
                        session['email'] = row[4]
                        session["name"] = str(row[1])
                        #to get registeref users list
                        cursor.execute('Select * from user_reg')
                        Account = cursor.fetchall()

                        cursor.execute('SELECT COUNT(fname) from user_reg')
                        users = cursor.fetchone()
                        cursor.close()
                        conn.close()


                        return render_template('admin_profile.html',name=str(row[1]),Accounts=Account , users =users[0])
                    else:
                        flash('Enter valid credentials1')
                        return redirect('/')
                else:
                    flash('Enter valid credentials2')
                    return redirect('/')
            else:
                flash('Enter valid credentials3')
                return redirect('/')
        else:
            flash('Enter valid credentials4')
            return redirect('/')
    else:
        email = details["inputEmail"]
        password = details["inputPassword"]
        if request.method == 'POST':

            if email and password:
                # check user exists
                conn = sql_conn()
                cursor = conn.cursor()
                sql = "SELECT * FROM user_reg WHERE email=%s"
                sql_where = (email,)
                cursor.execute(sql, sql_where)
                row = cursor.fetchone()
                if row:
                    if row[10] != "Closed":
                        if check_password_hash(row[6], password):
                            session['email'] = row[4]
                            session["name"] = str(row[1])
                            cursor.execute('Select * from transactions where email=%s order by ID desc LIMIT 5', (email))
                            trans = cursor.fetchall()

                            cursor.execute('SELECT SUM(amount) from transactions where email=%s', (email))
                            Total = cursor.fetchone()

                            date_format = "%Y-%m-%d"
                            date = datetime.today().strftime(date_format)
                            cursor.execute('SELECT SUM(amount) from transactions where email=%s AND date=%s',
                                           (email, date))
                            date_total = cursor.fetchone()

                            cursor.execute('SELECT SUM(amount) from transactions where month(date)in (select max(month(date)) from transactions) and email=%s',(email))

                            month_total = cursor.fetchone()

                            cursor.close()
                            conn.close()
                            return render_template('user_profile.html', list = row,Acc = Acc+str(row[0]),transactions=trans,Total=Total,date_total=date_total,month_total=month_total)
                        else:
                            flash('Enter valid credentials')
                            return redirect('/')
                    else:
                        flash('your Account is closed, please reactivate it again')
                        return redirect('/')
                else:
                    flash('Enter valid credentials')
                    return redirect('/')
            else:
                flash('Enter valid credentials')
                return redirect('/')
        else:
            flash('Enter valid credentials')
            return redirect('/')

@app.route('/profile')
def profile():
    role_n = role
    if role_n:
        if role == 'Admin':
            email = session['email']

            conn = sql_conn()
            cursor = conn.cursor()
            sql = "SELECT * FROM admin_reg WHERE email=%s"
            sql_where = (email,)
            cursor.execute(sql, sql_where)
            row = cursor.fetchone()
            if row:
                # to get registered users list
                cursor.execute('Select * from user_reg')
                Account = cursor.fetchall()

                cursor.execute('SELECT COUNT(fname) from user_reg')
                users = cursor.fetchone()
                cursor.close()
                conn.close()

                return render_template('admin_profile.html',name=str(row[1]),Accounts=Account , users =users[0])

        else:
            email = session['email']
            conn = sql_conn()
            cursor = conn.cursor()
            sql = "SELECT * FROM user_reg WHERE email=%s"
            sql_where = (email,)
            cursor.execute(sql, sql_where)
            row = cursor.fetchone()
            if row:

                #for gettng last transactions detials of user
                cursor.execute('Select * from transactions where email=%s order by ID desc LIMIT 5',(email))
                trans = cursor.fetchall()

                cursor.execute('SELECT SUM(amount) from transactions where email=%s', (email))
                Total = cursor.fetchone()

                date_format = "%Y-%m-%d"
                date = datetime.today().strftime(date_format)
                cursor.execute('SELECT SUM(amount) from transactions where email=%s AND date=%s', (email,date))
                date_total = cursor.fetchone()

                cursor.execute(
                    'SELECT SUM(amount) from transactions where month(date)in (select max(month(date)) from transactions) and email=%s',
                    (email))

                month_total = cursor.fetchone()
                return render_template('user_profile.html',list = row,Acc = Acc+str(row[0]),transactions=trans,Total=Total,
                                       date_total=date_total,month_total=month_total)

    else:
        flash('session expired please Login again')
        return redirect('/')


@app.route('/profile_update')
def profile_update():
    role_n = role

    if role_n == 'Admin':
        email = session['email']
        conn = sql_conn()
        cursor = conn.cursor()
        sql = "SELECT * FROM admin_reg WHERE email=%s"
        sql_where = (email,)
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        if row:
            return render_template('profile_update.html', list=row)


    else:
        email =  session['email']
        conn = sql_conn()
        cursor = conn.cursor()
        sql = "SELECT * FROM user_reg WHERE email=%s"
        sql_where = (email,)
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        if row:

            return render_template('profile_update.html', list = row)


@app.route('/update',methods=['POST'])
def update():
    role_n = role
    if role_n == 'Admin':
        details = request.form
        fname = details['fname']
        gender = details['gender']
        lname = details['lname']
        contact = details['contact']
        id = details['regno']

        conn = sql_conn()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE admin_reg SET fname=%s,gender=%s,lname=%s,contact=%s WHERE ID = %s',
            (fname, gender, lname, contact, id))
        cursor.close()
        conn.commit()
        conn.close()
        return redirect('/profile')

    else:
        details = request.form
        fname = details['fname']
        gender = details['gender']
        lname = details['lname']
        contact = details['contact']
        id = details['regno']

        conn = sql_conn()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE user_reg SET fname=%s,gender=%s,lname=%s,contact=%s WHERE ID = %s',
            (fname, gender, lname, contact,id))
        cursor.close()
        conn.commit()
        conn.close()
        return redirect('/profile')

@app.route('/add_amount')
def add_amount():
 return render_template('addamount.html')

@app.route('/add',methods=['POST'])
def add():
    email =session['email']
    Amount = request.form.get('Amount')
    conn = sql_conn()
    cursor = conn.cursor()
    cursor.execute('Select * from user_reg where email=%s',(email))
    row = cursor.fetchone()
    Existing_balance = int(row[8])
    Total =  Existing_balance+int(Amount)

    cursor.execute(
        'UPDATE user_reg SET balance=%s Where email =%s',
        (Total,email))
    cursor.close()
    conn.commit()
    conn.close()
    flash('Rs :'+str(Amount)+' is added to your wallet.')
    return redirect('/profile')

@app.route('/tr_amount')
def tr_amount():
 return render_template('Transfer.html')


@app.route('/OTP',methods=['POST','GET'])
def OTP():
    global otpn,zero,Email,To_addrs,Amount
    if request.method == 'POST':
        zero = 0
        Email = session['email']
        To_addrs = request.form.get('wt_id')
        Amount = request.form.get('Amount')
        new = int(random.random()*1000000)

        otpn = int(round(new,6))
        sender = "2798ed05237b16"  # enter sender email address
        Password = "54be75888612d5"  # enter sender password
        to_addr = "test@localhost" # enter receiver email adderss
        smtp = smtplib.SMTP('smtp.mailtrap.io',587 ) # enter your smtp address and Port number
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender,Password)  # will login in to your email account

        subject = "Your OTP For Latest Transaction Attempt "
        body =  "OTP For Latest transaction "+str(otpn)+ " Generated at @ " +str(time.ctime())
        msg = f'subject : {subject}\n\n{body}'
        smtp.sendmail(sender,to_addr,msg)
        smtp.quit()
        return  render_template('OTP_verify.html',wt_id=To_addrs,Amount=Amount)
    else:
        Email = session['email']
        To_addr = To_addrs


        Amount = Amount
        return render_template('OTP_verify.html',wt_id=To_addr,Amount=Amount)
@app.route('/transfer',methods=['POST'])
def transfer():
    OTP_number = int(request.form.get('OTP'))
    if otpn == OTP_number:
    #For getting sender details
        conn = sql_conn()
        cursor = conn.cursor()
        cursor.execute('Select * from user_reg where email=%s', (Email))
        row = cursor.fetchone()
        Balance = row[8]
        if int(Balance) != zero:
            name = row[1]
            updated_bal = int(Balance)-int(Amount)
            cursor.execute('UPDATE user_reg SET balance=%s Where email =%s',(updated_bal,email))
            conn.commit()

            #For getting Receiver details
            cursor.execute('Select * from user_reg where ID=%s', (To_addrs))
            row = cursor.fetchone()
            try:# using try block for to check of code executes or not
                to_name =row[1]
                To_Balance = row[8]
                to_updated_bal = int(To_Balance)+int(Amount)
                cursor.execute('UPDATE user_reg SET balance=%s Where ID =%s', (to_updated_bal, To_addrs))
                conn.commit()
                cursor.close()
                conn.close()

                #for recording transactions
                conn = sql_conn()
                cursor = conn.cursor()
                date_format = "%Y-%m-%d"
                trans_date = datetime.today().strftime(date_format)
                cursor.execute('INSERT INTO transactions VALUES (%s,%s, %s, %s, %s,%s)',
                               ("",name,to_name,trans_date,Amount,email))
                conn.commit()
                cursor.close()
                conn.close()


                flash('Rs :' + str(Amount) + ' is successfully Transfered to  '+ to_name)
                return redirect('/profile')
            except Exception as e:
                flash('Please Enter Correct Wallet Id.')
                return redirect('/tr_amount')
        else:
            flash('You do not have sufficient balance to transfer ')
            return redirect('/profile')
    else:

        flash(f'Please enter correct OTP Number ')

        return redirect('/OTP')

@app.route('/acc_status',methods=['POST'])
def acc_status():
    global new, ac_id, change

    detials = request.form.to_dict()

    for i in detials:
        ac_id = str(i)
        change = detials[ac_id]
    if change == "Activate":
        conn = sql_conn()
        cursor = conn.cursor()

        cursor.execute('UPDATE user_reg SET status=%s,closed_date="" Where ID =%s', (change,ac_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Account Activated successfully")
        return redirect('/profile')
    else:
        conn = sql_conn()
        cursor = conn.cursor()
        date_format = "%Y-%m-%d"
        closed_date = datetime.today().strftime(date_format)
        cursor.execute('UPDATE user_reg SET status=%s,closed_date=%s Where ID =%s', ("Closed",closed_date, ac_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Account Closed successfully")
        return redirect('/profile')


@app.route('/password_chg')
def password_chg():
    return render_template('change_password.html')

@app.route('/password_change',methods=['POST'])
def password_change():
    role_n = role
    if role_n == 'Admin':
        password = generate_password_hash(request.form.get('password'))
        conn = sql_conn()
        cursor = conn.cursor()
        cursor.execute('UPDATE admin_reg SET password=%s', (password))
        conn.commit()
        cursor.close()
        conn.close()
        flash("password changed successfully")
        return redirect('/profile')
    else:
        password = generate_password_hash(request.form.get('password'))
        conn = sql_conn()
        cursor = conn.cursor()
        cursor.execute('UPDATE user_reg SET password=%s',(password))
        conn.commit()
        cursor.close()
        conn.close()
        flash("password changed successfully")
        return redirect('/profile')

@app.route('/transaction_list')
def transaction_list():
    email = session['email']
    conn = sql_conn()
    cursor = conn.cursor()
    cursor.execute('Select * from transactions where email=%s', (email))
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    if row:

        return render_template('total_trans.html',transactions = row,Acc = Acc+str(row[0][0]),list=row[0][1])
    else:
        flash('No transactions were made')
        return redirect('/profile')

otpTable=['9101','1089','0000']  # you have to create and save the otp anytime you send it to the user
                                  #the table will contain two column the pin and the counter column
                                  # whenevr user enter wrong otp the counter column should increase till it each 3
                                  # the you flag it  
                                  # otpTable list represent otp Column          
counter = 0  # this represent the counter column

@app.route('/otptest',methods=['GET','POST'])
def otptest():

    if request.method == 'POST':
        print(counter)
  
        pin = request.form['otp']

        if pin in otpTable:
            return 'otp valid'

        if not pin in otpTable:  #if the otp is not valid the counter column should increase 
            counter=+1
            if counter == 3:  #if the counter table is upto 3 the it should flag
                return 'you have enter incorrect pin 3 times'

            flash('incorrect otp enterd you have'+str(3-counter))  # here you should give the response
            return redirect(request.url)

            """
            this is just an alogrithm you implement it perfectly

            """




    return render_template('otp.html')




@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
    return redirect('/')

