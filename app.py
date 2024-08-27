from flask import Flask, render_template,request,redirect,jsonify,url_for,session,json,send_from_directory,flash
from pymongo import MongoClient
from flask_pymongo import PyMongo
import os
from flask_login import logout_user
# from mongoengine import connect, StringField, IntField
from werkzeug.utils import secure_filename
from functools import wraps
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from bson.objectid import ObjectId
from flask_mail import Mail,Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

UPLOAD_FOLDER = 'static/upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['SECRET_KEY']='the random string'
app.config['MONGO_URI']='mongodb://localhost:27017/services'
client = MongoClient('localhost', 27017)
client = MongoClient(app.config['MONGO_URI'])
mongo=PyMongo(app)
db = client['services']
home = db['Home']
company = db['about_company']
blog = db['blog']
portfo = db['portfolio']
contactt = db['contact']
media = db['Media']
admin_admin = db['admins']
partner = db['Partner']
ourstory = db['ourstory']
whatwedo = db['whatwedo']
ourteam = db['ourteam']
video = db['Video']
about_post = db['about_post']
portfo_other = db['portfo_other']
blog_content = db['blog_content']



def mailSend(to, cc , subject , message):
    msg = MIMEMultipart()

    print("verferffesfe")
    bcc=[]
    

    bcc.append("")

    newTo=[]
    for i in to:
        if(i!=None and i!='None'):
           newTo.append(i) 

    newcc=[]
    for i in cc:
        if(i!=None and i!='None'):
           newcc.append(i) 
    
    
    # setup the parameters of the msg
    password = "mzvfilwjlsumwyxv"
    msg['From'] = "shubham.singh@fourbrick.com"
    msg['To'] = ", ".join(newTo)
    msg['Cc'] = ", ".join(newcc)
    msg['Bcc'] = ", ".join(bcc)
    msg['Subject'] = subject
    
    # add in the msg body
    msg.attach(MIMEText(message, 'html'))
    
    email_content = msg.as_string()

    
    all_email  =  newcc + newTo + bcc
    
    #create server
    server = smtplib.SMTP("smtp.gmail.com:587")
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    
# Login Credentials for sending the mail
    # server.login(msg['From'], password)
    
    
    # send the msg via the server.
    print(msg.as_string())

    server.sendmail(msg['From'], all_email, email_content)

    server.quit()
    return "mail has been sended"



@app.route('/',methods=['GET'])
def indexhtml():
    data = home.find()
    data1 =  partner.find()
    data2 = ourstory.find()
    data3 = whatwedo.find()
    data4 = video.find()
    data5 = ourteam.find()
    datacont = contactt.find()
    datamedia = media.find()
    # print("jhsasuhasj",data,data1,data2,data3,data5,datacont)
    return render_template('index.html',data=list(data),data1=list(data1),data2=list(data2),data3=list(data3),data4=list(data4),datacont=list(datacont),data5=list(data5),datamedia=list(datamedia))   #-----[cursor object ko list mein store karne k liye]




@app.route('/enquiry', methods=['GET', 'POST'])
def index2():
    print("call")
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        data = {'name': name, 'email': email, 'Message': message}
        print(data)
        mongo.db.enquiry.insert_one(data)
        e = 'shubham.singh@fourbrick.com'
        msg = message +" " +"" +email
        subject = 'User enquiry '
        print(mailSend([e],[],subject,msg))
        return '''
        <script>
            alert('Mail has been sent successfully');
            window.location.href = 'contact1'; 
        </script>'''
    return render_template('contact1.html')




@app.route("/about",methods=['GET'])
def abouthtml():
    data = company.find()
    data1 = about_post.find()
    data5 = ourteam.find()
    datacont = contactt.find()
    datamedia = media.find()
    return render_template('about1.html',data=list(data), data1=list(data1),datacont=list(datacont),data5=list(data5),datamedia=list(datamedia))

@app.route("/portfolio1",methods=['GET'])
def porthtml():
    data = portfo.find()
    data1 = portfo_other.find() 
    datacont = contactt.find()
    datamedia = media.find()
    return render_template('portfolio1.html',data=list(data),data1=list(data1),datacont=list(datacont),datamedia=list(datamedia))

@app.route("/contact1",methods=['GET'])
def contacthtml():
    datacont = contactt.find()
    datamedia = media.find()
    return render_template('contact1.html',datacont=list(datacont),datamedia=list(datamedia))

@app.route("/blog1",methods=['GET'])
def bloghtml():
    data = blog.find()
    data1 = blog_content.find()
    datacont = contactt.find()
    datamedia = media.find()
    return render_template('blog1.html', data=list(data),data1=list(data1),datacont=list(datacont),datamedia=list(datamedia))    


@app.route('/login',methods=['GET'])
def loginhtml():
    return render_template('login.html')






@app.route('/home',methods=['POST','GET'])
# @login_required
def home1():
    if request.method == 'POST':
        img=None
        if request.files.get('image'):
            img = request.files.get('image')
            path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
            img.save(path)
        back_img=None
        if request.files.get('back_img'):
            back_img= request.files.get('back_img')
            path = os.path.join(app.config['UPLOAD_FOLDER'],back_img.filename)
            back_img.save(path)
            # print(back_img)

        title = request.form.get('title')
        # description = request.form.get('description')
        
        data = {
           'img': img.filename if img else None,
           'back_img': back_img.filename if back_img else None,
           'title':title,
        #    'description':description
        }
        home.insert_one(data)
        return redirect('/home')

    data = home.find()
    return render_template("home.html",data=data)







@app.route('/about_company', methods=['POST','GET'])
# @login_required
def about_company():
    if request.method == 'POST':
        # img=None
        # if request.files.get('image'):
        #     img = request.files.get('image')
        #     path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
        #     img.save(path)
        #     print(img)
       
        title = request.form.get('title')
        description = request.form.get('description')
        
        data = {
        #    'img': img.filename if img else None,
           'title':title,
           'description':description
        }
        company.insert_one(data)
        return redirect('/about_company')
    data =  company.find()
    return render_template("about_company.html",data=data)

    






@app.route('/blog', methods=['GET', 'POST'])
# @login_required
def choose():
    if request.method=='POST':
        # img=None
        # if request.files.get('image'):
        #     img = request.files.get('image')
        #     path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
        #     img.save(path)
        #     print(img)
        title = request.form.get('title')
        description = request.form.get('description')
        
        data = {
        #    'img': img.filename if img else None,
           'title':title,
           'description':description
        }
        blog.insert_one(data)
        
        
        return redirect('/blog')
    data =  blog.find()
    return render_template("blog.html",data=data)


@app.route('/portfolio', methods=['GET', 'POST'])
# @login_required
def portfolio():
    if request.method=='POST':
        # img=None
        # if request.files.get("image"):
        #     img = request.files.get('image')
        #     path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
        #     img.save(path)
        #     print(img)
        
        
        title = request.form.get('title')
        description = request.form.get('description')
        
        data = {
        #    'img': img.filename if img else None,
            'title':title,
            'description':description
        }
        portfo.insert_one(data)
        
        
        return redirect('/portfolio')
    data =  portfo.find()
    return render_template("portfolio.html",data=data)




@app.route('/contact', methods=['GET', 'POST'])
# @login_required
def contact():
    if request.method=='POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        datacont = {
           "email": email,
           "phone": phone
        }
        contactt.insert_one(datacont)
        
        
        return redirect('/contact')
    datacont =  contactt.find()
    return render_template("contact.html",datacont=datacont)


@app.route('/media',methods=['GET','POST'])
# @login_required
def media1():
    if request.method == 'POST':
        link1 = request.form.get('link1')
        link2 = request.form.get('link2')
        link3 = request.form.get('link3')
        link4 = request.form.get('link4')

        datamedia = {
            "link1": link1,
            "link2": link2,
            "link3": link3,
            "link4": link4
        }
        media.insert_one(datamedia)
        return redirect('/media')
    datamedia = media.find()
    return render_template("socialmedia.html",datamedia=datamedia)


       

# --------------------------update Api------------------------------------home

@app.route('/update/<id>', methods=['POST','GET'])
# @login_required
def update1(id):
    
    if request.method == "POST":
        user = home.find_one({"_id": ObjectId(id)})
        # print(user)
        if user:
            
            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']
            
            bg_img = request.files.get('bg_image')
            if bg_img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],bg_img.filename)
                bg_img.save(path)
                bg_img_name = bg_img.filename
            else:
                bg_img_name = user['back_img']

            home.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "back_img":bg_img_name,
                        "img": img_name,
                        "title": request.form["title"],
                        # "description": request.form["description"],
                    }
                },
            )
            return redirect('/home')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/home')   
    
        
@app.route('/delete_home/<id>',)
# @login_required
def delete1(id):
    print(id)
    if id is not None:
        home.delete_one({"_id": ObjectId(id)})
        return redirect('/home')
    return jsonify({"message": "ID is required"})

# --------------------------------------------------about_company

@app.route('/update_company/<id>', methods=['POST','GET'])
# @login_required
def update2(id):
    
    if request.method == "POST":
        user = company.find_one({"_id": ObjectId(id)})
        # print(user)
        if user:
        #     img_name = None
            
        #     img = request.files.get('image')
            
        #     if img:
               
        #         path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
        #         img.save(path)
        #         img_name = img.filename
        #     else:
        #         # print('not update')
        #         img_name = user['img']

            
            
            
            company.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        # "img": img_name,
                        "title": request.form["title"],
                        "description": request.form["description"],
                    }
                },
            )
            return redirect('/about_company')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/about_company')   
    


@app.route('/delete_company/<id>',)
# @login_required
def delete2(id):
    print(id)
    if id is not None:
        company.delete_one({"_id": ObjectId(id)})
        return redirect('/about_company')
    return jsonify({"message": "ID is required"})


# -------------------------------------------------------blog


@app.route('/update_blog/<id>', methods=['POST','GET'])
# @login_required
def update3(id):
    if request.method == "POST":
        user = blog.find_one({"_id": ObjectId(id)})
        if user:
            img_name = None
            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']

            blog.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "img": img_name,
                        "title": request.form["title"],
                        "description": request.form["description"],
                    }
                },
            )
            return redirect('/blog')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/blog')

@app.route('/delete_blog/<id>',)
# @login_required
def delete3(id):
    print(id)
    if id is not None:
        blog.delete_one({"_id": ObjectId(id)})
        return redirect('/blog')
    return jsonify({"message": "ID is required"})

# ---------------------------------------------------portfolio

@app.route('/update_portfo/<id>', methods=['POST','GET'])
# @login_required
def update4(id):
    if request.method == "POST":
        user = portfo.find_one({"_id": ObjectId(id)})
        if user:
        #     img_name = None

        #     img = request.files.get('image')
        #     if img:
        #         path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
        #         img.save(path)
        #         img_name = img.filename
        #     else:
        #         img_name = user['img']

            portfo.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                    #    "img": img_name,
                       "title": request.form["title"],
                       "description": request.form["description"]
                    }
                },
            )
            return redirect('/portfolio')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/portfolio')


@app.route('/delete_portfo/<id>',)
# @login_required
def delete4(id):
    print(id)
    if id is not None:
        portfo.delete_one({"_id": ObjectId(id)})
        return redirect('/portfolio')
    return jsonify({"message": "ID is required"})


# -----------------------------------------------------contact

@app.route('/update_contactt/<id>', methods=['POST','GET'])
# @login_required
def update5(id):
    if request.method == "POST":
        user = contactt.find_one({"_id": ObjectId(id)})
        if user:
            contactt.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "email": request.form["email"],
                        "phone": request.form["phone"],
                    }
                },
            )
            return redirect('/contact')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/contact')



@app.route('/delete_contactt/<id>',)
# @login_required
def delete5(id):
    print(id)
    if id is not None:
        contactt.delete_one({"_id": ObjectId(id)})
        return redirect('/contact')
    return jsonify({"message": "ID is required"})

#-------------------------------------------------media

@app.route('/update_media/<id>', methods=['POST','GET'])
# @login_required
def updatemedia(id):
    if request.method == 'POST':
        user = media.find_one({'_id': ObjectId(id)})
        if user:
            media.update_one(
                {"_id": ObjectId(id)},
                {
                   "$set":{
                       "link1": request.form['link1'],
                       "link2": request.form['link2'],
                       "link3": request.form['link3'],
                       'link4': request.form['link4'],  
                   } 
                }

            )
            return redirect('/media')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/media')


@app.route('/delete_media/<id>')
# @login_required
def deletemedia(id):
    if id is not None:
        media.delete_one({"_id": ObjectId(id)})
        return redirect('/media')
    return jsonify({"message":"ID is required"})





#-----------------------Sub_menu-------------------#




#--------------------Home-sub-menu----------------#

 #---------(home)partner-------------#


@app.route('/partner', methods=['GET', 'POST'])
# @login_required
def partner1():
    if request.method == 'POST':
        logo=None
        if request.files.get('logo'):
            logo = request.files.get('logo')
            path = os.path.join(app.config['UPLOAD_FOLDER'],logo.filename)
            logo.save(path)
        
        link = request.form.get('link')
        
        data1 = {
           'logo': logo.filename if logo else None,
           'link': link
        }
        partner.insert_one(data1)
        return redirect('/partner')
    data1 =  partner.find()
    return render_template("partner.html",data1=data1)



@app.route('/update_partner/<id>', methods=['POST','GET'])
# @login_required
def update6(id):

    if request.method == "POST":
        user = partner.find_one({"_id": ObjectId(id)})
        print(user)
        if user:
            logo = request.files.get('logo')
            if logo:
                path = os.path.join(app.config['UPLOAD_FOLDER'],logo.filename)
                logo.save(path)
                logo_name  = logo.filename
                print(logo_name)
            else:
                logo_name = user['logo']

            partner.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                       'logo': logo_name,
                       'link': request.form["link"]
                    }
                },
            )
            return redirect('/partner')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/partner')


@app.route('/delete_partner/<id>',)
# @login_required
def delete6(id):
    print(id)
    if id is not None:
        partner.delete_one({"_id": ObjectId(id)})
        return redirect('/partner')
    return jsonify({"message": "ID is required"})


#-----------(home)ourstory-----------#

@app.route('/add_ourstory', methods=['GET', 'POST'])
# @login_required
def ourstory1():
    if request.method=='POST':
        img=None
        if request.files.get("image"):
            img = request.files.get('image')
            path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
            img.save(path)
            # print(img)
        
        
        title = request.form.get('title')
        description = request.form.get('description')
        
        data2 = {
           'img': img.filename if img else None,
            'title':title,
            'description':description
        }
        ourstory.insert_one(data2)
        
        
        return redirect('/add_ourstory')
    data2 =  ourstory.find()
    return render_template("ourstory.html",data2=data2)


@app.route('/update_ourstory/<id>', methods=['POST','GET'])
# @login_required
def update7(id):
    if request.method == "POST":
        user = ourstory.find_one({"_id": ObjectId(id)})
        if user:
            img_name = None

            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']

            ourstory.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                       "img": img_name,
                       "title": request.form["title"],
                       "description": request.form["description"]
                    }
                },
            )
            return redirect('/add_ourstory')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/ourstory')

@app.route('/delete_ourstory/<id>',)
# @login_required
def delete7(id):
    print(id)
    if id is not None:
        ourstory.delete_one({"_id": ObjectId(id)})
        return redirect('/add_ourstory')
    return jsonify({"message": "ID is required"})


#------------(home)whatwedo-----------#

@app.route('/add_whatwedo', methods=['GET', 'POST'])
# @login_required
def whatwedo1():
    if request.method=='POST':
        img=None
        if request.files.get("image"):
            img = request.files.get('image')
            path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
            img.save(path)
            # print(img)
        
        
        title = request.form.get('title')
        description = request.form.get('description')
        
        data3 = {
           'img': img.filename if img else None,
            'title':title,
            'description':description
        }
        whatwedo.insert_one(data3)
        
        
        return redirect('/add_whatwedo')
    data3 =  whatwedo.find()
    return render_template("whatwedo.html",data3=data3)


@app.route('/update_whatwedo/<id>', methods=['POST','GET'])
# @login_required
def update8(id):
    if request.method == "POST":
        user = whatwedo.find_one({"_id": ObjectId(id)})
        if user:
            img_name = None

            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']

            whatwedo.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                       "img": img_name,
                       "title": request.form["title"],
                       "description": request.form["description"]
                    }
                },
            )
            return redirect('/add_whatwedo')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/add_whatwedo')

@app.route('/delete_whatwedo/<id>',)
# @login_required
def delete8(id):
    print(id)
    if id is not None:
        whatwedo.delete_one({"_id": ObjectId(id)})
        return redirect('/add_whatwedo')
    return jsonify({"message": "ID is required"})

#---------------(home)video-----------#

@app.route('/add_video', methods=['GET', 'POST'])
# @login_required
def video1():
    if request.method=='POST':
        vid=None
        if request.files.get("video"):
            vid = request.files.get('video')
            path = os.path.join(app.config['UPLOAD_FOLDER'],vid.filename)
            vid.save(path)
            # print(vid)
        
        
        title = request.form.get('title')
        link = request.form.get('link')
        
        data4 = {
           'vid': vid.filename if vid else None,
            'title':title,
            'link':link
        }
        video.insert_one(data4)
        
        
        return redirect('/add_video')
    data4 =  video.find()
    return render_template("video.html",data4=data4)


@app.route('/update_video/<id>', methods=['POST','GET'])
# @login_required
def update9(id):
    if request.method == "POST":
        user = video.find_one({"_id": ObjectId(id)})
        if user:
            vid_name = None

            vid = request.files.get('video')
            if vid:
                path = os.path.join(app.config['UPLOAD_FOLDER'],vid.filename)
                vid.save(path)
                vid_name = vid.filename
            else:
                vid_name = user['vid']

            video.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                       "vid": vid_name,
                       "title": request.form["title"],
                       "link": request.form["link"]
                    }
                },
            )
            return redirect('/add_video')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/add_video')

@app.route('/delete_video/<id>',)
# @login_required
def delete9(id):
    print(id)
    if id is not None:
        video.delete_one({"_id": ObjectId(id)})
        return redirect('/add_video')
    return jsonify({"message": "ID is required"})

#------------(home)ourteam-----------#

@app.route('/add_ourteam', methods=['GET', 'POST'])
# @login_required
def ourteam1():
    if request.method=='POST':
        img=None
        if request.files.get("image"):
            img = request.files.get('image')
            path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
            img.save(path)
            # print(img)
        
        
        title = request.form.get('title')
        description = request.form.get('description')
        
        data5 = {
           'img': img.filename if img else None,
            'title':title,
            'description':description
        }
        ourteam.insert_one(data5)
        
        
        return redirect('/add_ourteam')
    data5 =  ourteam.find()
    return render_template("ourteam.html",data5=data5)


@app.route('/update_ourteam/<id>', methods=['POST','GET'])
# @login_required
def update10(id):
    if request.method == "POST":
        user = ourteam.find_one({"_id": ObjectId(id)})
        if user:
            img_name = None

            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']

            ourteam.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                       "img": img_name,
                       "title": request.form["title"],
                       "description": request.form["description"]
                    }
                },
            )
            return redirect('/add_ourteam')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/add_ourteam')

@app.route('/delete_ourteam/<id>',)
# @login_required
def delete10(id):
    print(id)
    if id is not None:
        ourteam.delete_one({"_id": ObjectId(id)})
        return redirect('/add_ourteam')
    return jsonify({"message": "ID is required"})


#--------------------------About-sub-menu-------------------#

@app.route('/about_post', methods=['GET','POST'])
# @login_required
def about_post1():
    if request.method=='POST':
        img1 = request.files.get('image')
        path = os.path.join(app.config['UPLOAD_FOLDER'],img1.filename)
        img1.save(path)

        title = request.form.get('title')
        description = request.form.get('description')

        
        data1 = {
           'img1': img1.filename,
           'title': title,
           'description':description

        }
        about_post.insert_one(data1)
        
        
        return redirect('/about_post')
    data1 =  about_post.find()
    return render_template("about_post.html",data1=data1)




@app.route('/update_about_post/<id>', methods=['POST','GET'])
# @login_required
def update11(id):
    if request.method == "POST":
        user = about_post.find_one({"_id": ObjectId(id)})
        if user:
            img_name1 = None
            img1 = request.files.get('image')
            if img1:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img1.filename)
                img1.save(path)
                img_name1 = img1.filename
            else:
                img_name1  = user['img1']

            title = request.form.get('title')
            description = request.form.get('description')
            


            

            about_post.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "img1": img_name1,
                        'title':title,
                        'description':description

                    }
                },
            )
            return redirect('/about_post')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/about_post')



@app.route('/delete_about_post/<id>',)
# @login_required
def delete11(id):
    print(id)
    if id is not None:
        about_post.delete_one({"_id": ObjectId(id)})
        return redirect('/about_post')
    return jsonify({"message": "ID is required"})




@app.route('/about_honors', methods=['GET','POST'])
@app.route('/about_honors/<typer>/<id>', methods=['GET','POST'])
def about_honors1(typer=None,id=None):
    if request.method =='POST':
        image = request.files.get('image')
        path = os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
        image.save(path)

        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        description = request.form.get('description')

        
        dictData = {
           'image': image.filename,
           'title': title,
           'subtitle': subtitle,
           'description':description}
        if (id!=None):
            update = {
                '_id':ObjectId(id)
            }
            allData = mongo.db.honours.update_one(
                update,{'$set':dictData},False)
        else:
            allData = mongo.db.honours.insert_one(dictData)
        return redirect('/about_honors')
    if request.method == 'GET':
        if(typer == 'del'):
            delete = {
                '_id':ObjectId(id)
            }
            deldictData = {
                'deleteStatus':1
            }
            allData = mongo.db.honours.update_one(
                delete,{'$set':deldictData},False)
            return redirect('/about_honors')
        allData = mongo.db.honours.find({"deleteStatus":{'$ne':1}})
        return render_template("about_honors.html",allData=list(allData))




# @app.route('/update_about_post/<id>', methods=['POST','GET'])
# # @login_required
# def update11(id):
#     if request.method == "POST":
#         user = about_post.find_one({"_id": ObjectId(id)})
#         if user:
#             img_name1 = None
#             img1 = request.files.get('image')
#             if img1:
#                 path = os.path.join(app.config['UPLOAD_FOLDER'],img1.filename)
#                 img1.save(path)
#                 img_name1 = img1.filename
#             else:
#                 img_name1  = user['img1']

#             title = request.form.get('title')
#             description = request.form.get('description')


            


            

#             about_post.update_one(
#                 {"_id": ObjectId(id)},
#                 {
#                     "$set": {
#                         "img1": img_name1,
#                         'title':title,
#                         'description':description

#                     }
#                 },
#             )
#             return redirect('/about_post')
#         else:
#             return jsonify({'error':'user not found'})
#     return redirect('/about_post')



# @app.route('/delete_about_post/<id>',)
# # @login_required
# def delete11(id):
#     print(id)
#     if id is not None:
#         about_post.delete_one({"_id": ObjectId(id)})
#         return redirect('/about_post')
#     return jsonify({"message": "ID is required"})


  
#----------------------------portfolio-sub-menu--------------#
@app.route('/portfolio_other', methods=['GET','POST'])
# @login_required
def portfolio1():
    if request.method=='POST':
        img=None
        if request.files.get("image"):
            img = request.files.get('image')
            path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
            img.save(path)
            # print(img)
        
        
        title = request.form.get('title')
        description = request.form.get('description')
        
        data1 = {
           'img': img.filename if img else None,
            'title':title,
            'description':description
        }
        portfo_other.insert_one(data1)
        
        
        return redirect('/portfolio_other')
    data1 =  portfo_other.find()
    return render_template("port_other.html",data1=data1)



@app.route('/update_portfo_other/<id>', methods=['POST','GET'])
# @login_required
def update12(id):
    if request.method == "POST":
        user = portfo_other.find_one({"_id": ObjectId(id)})
        if user:
            img_name = None

            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']

            portfo_other.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                       "img": img_name,
                       "title": request.form["title"],
                       "description": request.form["description"]
                    }
                },
            )
            return redirect('/portfolio_other')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/portfolio_other')


@app.route('/delete_portfo_other/<id>',)
# @login_required
def delete12(id):
    print(id)
    if id is not None:
        portfo_other.delete_one({"_id": ObjectId(id)})
        return redirect('/portfolio_other')
    return jsonify({"message": "ID is required"})



#--------------blog-sub-menu--------#

@app.route('/blog_content', methods=['GET', 'POST'])
# @login_required
def blog_content1():
    if request.method=='POST':
        img = request.files.get('image')
        print(img)
        path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
        img.save(path)
        title = request.form.get('title')
        description = request.form.get('description')
        
        data = {
           'img': img.filename,
           'title':title,
           'description':description
        }
        blog_content.insert_one(data)
        
        
        return redirect('/blog_content')
    data =  blog_content.find()
    return render_template("blog_content.html",data=data)



@app.route('/update_blog_content/<id>', methods=['POST','GET'])
# @login_required
def update13(id):
    if request.method == "POST":
        user = blog_content.find_one({"_id": ObjectId(id)})
        if user:
            img_name = None
            img = request.files.get('image')
            if img:
                path = os.path.join(app.config['UPLOAD_FOLDER'],img.filename)
                img.save(path)
                img_name = img.filename
            else:
                img_name = user['img']
            blog_content.update_one(
                {"_id": ObjectId(id)},
                {
                    "$set": {
                        "img": img_name,
                        "title": request.form["title"],
                        "description": request.form["description"],
                    }
                },
            )
            return redirect('/blog_content')
        else:
            return jsonify({'error':'user not found'})
    return redirect('/blog_content')


@app.route('/delete_blog_content/<id>',)
# @login_required
def delete13(id):
    print(id)
    if id is not None:
        blog_content.delete_one({"_id": ObjectId(id)})
        return redirect('/blog_content')
    return jsonify({"message": "ID is required"})

















# ---------------------------------------------------login api
# login_manager = LoginManager(app)

# class User(UserMixin):
#     def __init__(self, id, is_active=True):
#         self.id = id
#         def is_active(self):
#             return True  
# if not admin_admin.find_one():
#     admin_username = 'vishal@gmail.com'
#     admin_password = 'Vishal@1'
#     admin_admin.insert_one({'username': admin_username, 'password': admin_password})
# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)
 
# login_manager.login_view = 'login'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" not in session:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            dictData={
                "username":username,
                "password":password, 
            }

            # Check if the username and password match
            admin = mongo.db.admins.find(dictData)
            admin=list(admin)
            # print(f'jhjcjgu{admin}')
            print(admin)
            # store the username in the session
            if(admin):
                session['username'] = ['username']
                return redirect('/home')
            else:
                return render_template('login.html',msg="invalid")
        return render_template('login.html')
    else:
        return redirect("/home")
    #     if admin:
            
    #         user = User(admin['_id'])
        
    #         login_user(user)

    #         return redirect("/home") #redirect('/add')
    #         # return jsonify({'message':'you have been successfully login'})######render_template('index.html')
    #     else:
    #         return jsonify({'message': 'Invalid username or password!'})
    # # return jsonify({'message': 'yes'})
    # return render_template('login.html')

# --------------------------------------------------logout

@app.route('/logout')
# @login_required
def logout():
    if "username" in session:
        del session["username"]
        return redirect('/')
    else:
        return redirect("/login")

# -------------------------------------------------forgot

@app.route('/forgot/', methods=['GET', 'POST'])
# @login_required
def forgot():
    # if 'admin' in session:
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_password = request.form.get('new_password')
        # print('mlkkhtyrtxfdxdszfd::::::', username, new_password)
        admin = mongo.db.admins.find_one({'username': username})
        
        
        print(admin)
        if admin:
            if password == new_password:
            # '_id':
                mongo.db.admins.update_one({'_id': admin['_id']}, {
                                       '$set': {'password': new_password}})

            # admin_password = new_password
            # new_password.update(admin_password)
            # with open('config.json', 'w') as c:
            #     json.dump({'params': params}, c)
            # return jsonify({'message':'Password updated successfully!'})

                # flash ('Password updated successfully!4645.kkghf')
                return 'Password updated successfully!'
            return redirect('/login')
        else:
            return jsonify({ 'message':'your email is not match'})
            # return "your email is not match"
    # return jsonify({'message': 'yes'})
    return render_template('forgot.html')

# ``````````````````````````````````````````````````````````````````````````````````````````````````



if __name__=="__main__":
    app.run(debug=True,port=6969)