from flask import Flask, render_template, redirect, request, session, url_for
import datetime
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory, abort
import mysql.connector
import uuid
import cv2
import pytesseract
from PIL import Image
import pyotp

import requests

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'abcdef'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    database="pm"
)

@app.route('/',methods=['POST','GET'])
def index():

    return render_template('index.html')


@app.route('/rto_log',methods=['POST','GET'])
def rto_log():

    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM pm_rto where username=%s && password=%s",(username,password))
        account = mycursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'rto'
            msg="success"  
        else:
            msg="fail"

    return render_template('rto_log.html', msg=msg)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_veh',methods=['POST','GET'])
def add_veh():

    msg=""
    
    if request.method=='POST':
        veh_no=request.form['veh_no']
        reg_mobile=request.form['reg_mobile']
        reg_name=request.form['reg_name']
        reg_address=request.form['reg_address']
        veh_type=request.form['veh_type']
        veh_name=request.form['veh_name']
        veh_color=request.form['veh_color']
        fuel_type=request.form['fuel_type']
        chassis_no=request.form['chassis_no']
        seats=request.form['seats']
        username=request.form['username']
        password=request.form['password']
        now = datetime.datetime.now()
        reg_join=now.strftime("%d-%m-%Y")
        if 'image' in request.files:
            image = request.files['image']

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = 'D:/PickmeSafe/static/vehicle/' + filename
                image.save(image_path)

                mycursor = mydb.cursor()
                mycursor.execute("SELECT count(*) FROM pm_vehicle where veh_no=%s",(veh_no, ))
                cnt = mycursor.fetchone()[0]
                if cnt==0:
                    mycursor.execute("SELECT max(id)+1 FROM pm_vehicle")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    sql = "INSERT INTO pm_vehicle(id, veh_no, reg_mobile, reg_name, reg_address, veh_type, veh_name, veh_color, fuel_type, chassis_no, seats, reg_join, image, images, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (maxid, veh_no, reg_mobile, reg_name, reg_address, veh_type, veh_name, veh_color, fuel_type, chassis_no, seats, reg_join, filename, doc_filename, username, password)
            
                    mycursor.execute(sql, val)
                    mydb.commit()

                    msg="success"
                else:
                    msg="fail"

    return render_template('add_veh.html', msg=msg)



pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


@app.route('/num_search', methods=['POST','GET'])
def num_search():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a hod to access the page.", 'danger')
        return redirect(url_for('user_log'))
   
    
    license_plate=""
    st=""
    mess=""
    name=""
    mobile=""
    user=""
    dname=""
    dmobile=""
    oname=""
    omobile=""
    veh_no=""
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'image' not in request.files:
            return 'No file part'
        
        doc_file = request.files['image']
        if doc_file:
            doc_filename = secure_filename(doc_file.filename)
            doc_file.save('D:/PickmeSafe/static/vehicle/' + doc_filename)
            doc_path = 'D:/PickmeSafe/static/vehicle/' + doc_filename

            img = cv2.imread(doc_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 30, 150)

            # Find contours in the edged image
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Loop over the contours to find the license plate contour
            for contour in contours:
                if cv2.contourArea(contour) > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    roi = gray[y:y + h, x:x + w]
                    
                    # Perform OCR on the license plate region
                    license_plate = pytesseract.image_to_string(roi, config='--psm 6')  # Adjust OCR configuration if needed
                    break
            
    plate = request.args.get('plate')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_vehicle WHERE veh_no = %s", (plate,))
    data = cursor.fetchone()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_driver WHERE veh_no = %s", (plate,))
    dat = cursor.fetchone()
    cursor.close()

    

    act=request.args.get("act")
    if act=="message":
        veh_id=request.args.get("veh_id")
        now = datetime.datetime.now()
        reg_join=now.strftime("%d-%m-%Y")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM pm_vehicle WHERE id = %s", (veh_id,))
        aa = cursor.fetchone()
        veh_no=aa[1]
        oname=aa[3]
        omobile=aa[2]
        oaddress=aa[4]
        veh_type=aa[5]
        veh_name=aa[6]
        owner_username=aa[15]


        cursor.execute("SELECT * FROM pm_driver WHERE veh_no = %s", (veh_no,))
        cc = cursor.fetchone()
        dname=cc[5]
        dmobile=cc[3]
        daddress=cc[2]

        username = session.get('username')
        cursor.execute("SELECT * FROM pm_user WHERE username = %s", (username,))
        bb = cursor.fetchone()
        mobile=bb[6]
        name=bb[5]
        user=bb[1]
        umobile=bb[3]
        uaddress=bb[2]

        mess = f"Hi I'm {user},I have journey at {veh_no} owner is {oname}-{omobile}"

        st="1"
        cursor.close()

        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM pm_travel")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO pm_travel(id, veh_no, oname, omobile, oaddress, veh_type, veh_name, dname, dmobile, daddress, gmobile, gname, user, umobile, uaddress, username, reg_join, status, owner_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, veh_no, oname, omobile, oaddress, veh_type, veh_name, dname, dmobile, daddress, mobile, name, user, umobile, uaddress, username, reg_join, '1', owner_username)   
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"

        
    

    return render_template('num_search.html', license_plate=license_plate, data=data, dat=dat, name=name, mobile=mobile, st=st, mess=mess, user=user, veh_no=veh_no, dname=dname, dmobile=dmobile, oname=oname, omobile=omobile)

@app.route('/user_log', methods=['POST','GET'])
def user_log():

    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pm_user WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"
            
        else:
            msg="fail"

    return render_template('user_log.html', msg=msg)


@app.route('/user_reg', methods=['POST','GET'])
def user_reg():

    msg=""

    if request.method=='POST':       
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        gu_name=request.form['gu_name']        
        gu_mobile=request.form['gu_mobile']
        profile=request.form['profile']
        username=request.form['username']
        password=request.form['password']
        

        now = datetime.datetime.now()
        date_join=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM pm_user where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM pm_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO pm_user(id, name, address, mobile, email, gu_name,  gu_mobile, profile, username, password, date_join) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s)"
            val = (maxid, name, address, mobile, email, gu_name,  gu_mobile, profile, username, password, date_join)
            
            
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
        else:
            msg="fail"

    return render_template('user_reg.html', msg=msg)



@app.route('/distance',methods=['POST','GET'])
def distance():

   
        return render_template('distance.html')


@app.route('/get_otp',methods=['POST','GET'])
def get_otp():
    if 'username' not in session or session.get('user_type') != 'owner':
        print("Please log in as a hod to access the page.", 'danger')
        return redirect(url_for('owner_log'))
    mess=""
    reg_mobile=""
    name=""
    st=""
    msg=""
    if request.method == 'POST':
        veh_no = request.form['veh_no']
        
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM pm_vehicle WHERE veh_no = %s", (veh_no,))
        data = cursor.fetchone()
        reg_mobile=data[2]
        cursor.close() 
        if reg_mobile:
            otp = generate_otp()
            mess=f"Your OTP is: {otp}"
            st="1"
            msg="success"
            session['veh_no'] = veh_no
        else:
            msg="fail"
        
    return render_template('get_otp.html', mess=mess, reg_mobile=reg_mobile, st=st, name=name, msg=msg)

def generate_otp():
    return pyotp.TOTP(pyotp.random_base32()).now()


@app.route('/owner_log', methods=['POST','GET'])
def owner_log():

    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM pm_vehicle WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'owner'
            msg="success"
            
        else:
            msg="fail"

    return render_template('owner_log.html', msg=msg)


@app.route('/owner_reg', methods=['POST','GET'])
def owner_reg():

    msg=""

    if request.method=='POST':       
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        

        now = datetime.datetime.now()
        date_join=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM pm_owner where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM pm_owner")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO pm_owner(id, name, address, mobile, email, username, password, date_join) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
            val = (maxid, name, address, mobile, email, username, password, date_join)
            
            
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
        else:
            msg="fail"

    return render_template('owner_reg.html', msg=msg)



@app.route('/add_driver', methods=['POST','GET'])
def add_driver():
    if 'username' not in session or session.get('user_type') != 'owner':
        print("Please log in as a hod to access the page.", 'danger')
        return redirect(url_for('owner_log'))

    msg=""
    veh_no = session.get('veh_no')
    owner_username = session.get('username')
    if request.method=='POST':       
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        

        now = datetime.datetime.now()
        date_join=now.strftime("%d-%m-%Y")
        if 'profile' in request.files:
            profile = request.files['profile']

            if profile and allowed_file(profile.filename):
                filename = secure_filename(profile.filename)
                profile_path = 'D:/PickmeSafe/static/driver/' + filename
                profile.save(profile_path)

                mycursor = mydb.cursor()
                mycursor.execute("SELECT count(*) FROM pm_driver where username=%s",(username, ))
                cnt = mycursor.fetchone()[0]
                if cnt==0:
                    mycursor.execute("SELECT max(id)+1 FROM pm_driver")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    sql = "INSERT INTO pm_driver(id, name, address, mobile, email, username, password, profile, date_join, veh_no, owner_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                    val = (maxid, name, address, mobile, email, username, password, filename, date_join, veh_no, owner_username)
            
            
                    mycursor.execute(sql, val)
                    mydb.commit()

                    msg="success"
                else:
                    msg="fail"

    return render_template('add_driver.html', msg=msg, veh_no=veh_no)


@app.route('/veh_details',methods=['POST','GET'])
def veh_details():
    
    

    veh_no = session.get('veh_no')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_vehicle WHERE veh_no = %s", (veh_no,))
    data1 = cursor.fetchone()
    cursor.close()

    return render_template('veh_details.html', data1=data1, veh_no=veh_no)


@app.route('/view_driver',methods=['POST','GET'])
def view_driver():
    if 'username' not in session or session.get('user_type') != 'owner':
        print("Please log in as a hod to access the page.", 'danger')
        return redirect(url_for('owner_log'))

    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_driver WHERE owner_username = %s", (username,))
    data1 = cursor.fetchall()
    cursor.close()


    act=request.args.get("act")

    if act=="ok":
        did=request.args.get("did")
        cursor = mydb.cursor()
        cursor.execute("delete * from pm_driver where id=%s",(did,))
        mydb.commit()
        print("successfully accepted")

    return render_template('view_driver.html', pm_driver=data1)



@app.route('/view_status', methods=['GET', 'POST'])
def view_status():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('user_log'))

    
    username=session.get('username')
    mess=""
    st=""
    mobile=""
    name=""
    user=""
    latitude=""
    longitude=""
    tt=""
    mess1=""
    source=""
    destination=""

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_travel where user = %s",(username,))
    data3 = cursor.fetchall()
    cursor.close()

    act=request.args.get("act")
    if act=="me":
        tid=request.args.get("tid")
        cursor = mydb.cursor()
        cursor.execute("update pm_travel set status=2 where id=%s",(tid, ))
        mydb.commit()
        cursor.execute("SELECT * FROM pm_travel where id = %s",(tid,))
        dd = cursor.fetchone()
        mobile=dd[10]
        name=dd[11]
        user=dd[12]
        source=dd[20]
        destination=dd[21]
        mess1 = f"Hi I'm {user}, Reach the {destination} from {source} safely."

        tt="2"
        cursor.close()
        


    if request.method=='POST':
        tid=request.form['tid']
        latitude=request.form['latitude']
        longitude=request.form['longitude']
        cursor = mydb.cursor()
        cursor.execute("update pm_travel set latitude=%s, longitude=%s where id=%s",(latitude, longitude, tid))
        mydb.commit()
        cursor.execute("SELECT * FROM pm_travel WHERE id = %s", (tid,))
        bb = cursor.fetchone()
        mobile=bb[10]
        name=bb[11]
        user=bb[12]

        mess = f"Hi I'm {user},Emergency This is my location {latitude},{longitude}"

        st="1"
        cursor.close()

        

    return render_template('view_status.html', pm_travel=data3, mobile=mobile, name=name, user=user, mess=mess, st=st, latitude=latitude, longitude=longitude, tt=tt , mess1=mess1, source=source, destination=destination)



@app.route('/location', methods=['GET', 'POST'])
def location():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('user_log'))


    if request.method=='POST':
        tid=request.form['tid']
        source=request.form['source']
        destination=request.form['destination']
        cursor = mydb.cursor()
        cursor.execute("update pm_travel set source=%s, destination=%s where id=%s",(source, destination, tid))
        mydb.commit()
        cursor.close()

        

    return redirect(url_for('view_status'))



@app.route('/report',methods=['POST','GET'])
def report():

    if 'username' not in session or session.get('user_type') != 'owner':
        print("Please log in as a hod to access the page.", 'danger')
        return redirect(url_for('owner_log'))

    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_travel WHERE owner_username = %s", (username,))
    aa = cursor.fetchall()
    cursor.close()

    return render_template('report.html', pm_travel=aa)



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('user_log'))

    rid=request.args.get("rid")
    msg=""

    if request.method=='POST':

        feedback=request.form['feedback']
        cursor = mydb.cursor()
        cursor.execute("update pm_travel set feedback=%s where id=%s",(feedback, rid))
        mydb.commit()
        cursor.close()
        msg="success"

    return render_template('feedback.html', msg=msg)


@app.route('/over_report', methods=['GET', 'POST'])
def over_report():

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pm_travel")
    aa = cursor.fetchall()
    cursor.close()

    return render_template('over_report.html', pm_travel=aa)

@app.route('/logout')
def logout():
    session.clear()
    print("Logged out successfully", 'success')
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
