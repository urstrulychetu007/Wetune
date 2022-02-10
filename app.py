# from mysql.dbapi2 import Cursor
from distutils.log import debug
from re import template
from flask import *
from flask.app import Flask
from flask_mail import Mail,Message
from random import randint
from flask.helpers import url_for
from flask.templating import render_template
import sqlite3
import os
import bcrypt
# import mysql

from werkzeug.utils import redirect





class Queries:
    query = ''
    def __init__(self):
        self.query = ''

    def getquery(self):
        return self.query

    def setquery(self,query):
        self.query =  query       


querys = Queries()
app = Flask(__name__)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='wetuneapp@gmail.com'
app.config['MAIL_PASSWORD']='chetan2512'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)
unid = randint(00000000000,99999999999)

mysql = sqlite3.connect('data.db',check_same_thread=False)

usr = 'chetan'



def addusertodb(usn):
    cursor = mysql.cursor()
    query = "insert into userslog values('{n}','{n1}')".format(n=usn,n1=ip())
    cursor.execute(query)
    mysql.commit()
    # mysql.close()



def validation(email,passw):
    cursor = mysql.cursor()
    users = cursor.execute('select mail,pass,username,verification from users')
    users = cursor.fetchall()
    if len(users)>0 :
        userdetails =  cursor.fetchall()
        for users in userdetails:
            if users[0] == email and bcrypt.checkpw(passw.encode('utf-8'),users[1].encode('utf-8')) :
                cursor.close()
                addusertodb(users[2])
                return users[2]
      
    # cursor.close()
    return '0'

def ip():
    import socket
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    return ipaddr


def check(user):

    cur =  mysql.cursor()
    query = "select wli from userslog where usn = '{n}' and wli = '{n1}'".format(n=user,n1=ip())
    cur.execute(query)
    howmany = cur.fetchall()
    if len(howmany) > 0:
        return True
    else :
        return False    
def checkuser():
    cur =  mysql.cursor()
    query = "select usn from userslog where  wli = '{n1}' limit 1".format(n1=ip())
    cur.execute(query)
    howmany = cur.fetchall()
    if len(howmany) > 0:
        return howmany[0][0]
    else :
        return ''
@app.route("/signin",methods=["POST","GET"])
def login():
        #    usr=checkuser()
           global usr
           if usr!= '':
                return redirect(url_for('welcome',user=usr))        
           else:
            if request.method == 'POST':
                mail = request.form['email']
                password = request.form['passw']
                check = validation(mail,password)
                if check!='0':
                    usr = check
                    return redirect(url_for('welcome',user=usr))
                else:   
                 return  """ <h1>Invalid attempt <br><a href = "/signin">Try Again..</a></h1> """
            else:           
             return render_template('login.html')



@app.route("/")
def init():
    return render_template('init.html')

@app.route("/signout:<user>")
def signout(user):
    cursor = mysql.cursor()
    query = "delete from userslog where wli = '{n}' and usn = '{n1}'".format(n=ip(),n1=user)
    cursor.execute(query)
    mysql.commit()
    return redirect(url_for('login'))

@app.route('/home:<user>')
def welcome(user):
    # return user
    if  user!= '' :
       cur = mysql.cursor()
    #    cur = cur.cursor()
       cur.execute("select name,imageurl,rating,lang from movies m,movieInfo mi where m.mvid = mi.mvid order by rating desc limit 25")
       movieslist = cur.fetchall()
       cur.execute("select name from Genre,movieInfo where Genre.gen_id = movieInfo.gen_id group by name having count(Genre.gen_id)>3  limit 17")
       movieslist1 = cur.fetchall()
       list = [['Jathi Ratnalu','https://mcmscache.epapr.in/post_images/website_197/post_21391449/6049e8108d749.jpg','7.6','telugu','Srikanth and his friends Sekhar and Ravi head to the city in pursuit of some izzat. Once there, they realise that maybe they were better off back home in Jogipet.'],['Kanulu Kanulanu Dochayante','https://snagfilms-a.akamaihd.net/38c1e2aa-64c1-41c3-8b5e-674247d490c8/images/2021/04/12/1618210151242_kkd_1920x1080_16x9Images.jpg','7.7','telugu','Two wily online scammers mend their fraudulent ways after meeting the girls of their dreams — until a deceitful discovery throws their world for a loop'],['Sye Raa Narasimha Reddy','https://static.toiimg.com/photo/70752873.jpeg','7.4','telugu','Gwalior Fort, during the Indian Rebellion of 1857. In a moment of despair, Lakshmibai, Rani of Jhansi, encourages her men by telling them the heroic story of Uyyalawada Narasimha Reddy, a brave telugu chieftain who took up arms in 1846 to protest against the numerous arbitrariness and crimes perpetrated by the leaders and military forces of the East India Company.'],['Baahubali: The Conclusion','https://www.teahub.io/photos/full/300-3006582_bahubali-2-hd-posters.jpg','8.2','telugu','When Mahendra, the son of Bāhubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom'],['Mahanati','https://static.toiimg.com/thumb/msid-64794688,imgsize-128030,width-800,height-600,resizemode-75/64794688.jpg','8.5','telugu',"Mahanati depicts the life and career of one of telugu cinema's greatest and most iconic starlets, the first Indian female super star, Savitri"]]

    #    cur.execute("select name,imageurl from movies where yor='2019' order by yor ")
    #    movieslist2 = cur.fetchall()
       cur.execute("select ac_name,ac_url from actor,movies where actor.acid != 'AC0001' and movies.acid = actor.acid   group by ac_name,ac_url having count(movies.acid)>3")
       movieslist3 = cur.fetchall()
       cur.execute("select acs_name,acs_url from actress,movies where acsid != 'AS0001' and acs_id = acsid   group by acs_name,acs_url having count(acs_id)>3 ")
       movieslist4 = cur.fetchall()       
       return render_template('home.html',lists=list,top15list=movieslist,user=user,genrelist=movieslist1,actormvlist=movieslist3,actressmvlist=movieslist4,i=0)    
    else:
     return  redirect(url_for('login'))


@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == 'POST' :
        email = request.form['email']
        mobile = request.form['Mobile']
        username = request.form['username']
        password = request.form['passw']
        confrmpass = request.form['confrmpass']
        if password==confrmpass:
                # userdetails = email+'\n'+password+'\n'+mobile+'\n'+username
                chipertext = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
                cur = mysql.cursor()
                uid = 'U'+str(unid)
                cur.execute(f'Insert into users values("{username}","{uid}","{email}","{chipertext}","{mobile}","false")')
                mysql.commit()
                msg=Message(subject='OTP',sender='wetuneapp@gmail.com',recipients=[email])
                mesage = "stream-wetune app verify your mail to register the user so please enter the below otp given in the website to confirm your registration and have fun with us "+  str(otp)
                msg.body=mesage
                mail.send(msg)
                return render_template('verify.html',uname=username)
        else:
            return "Invalid credentials"        
    else :
        return render_template('register.html')    



@app.route('/validate<name>',methods=['POST'])
def validate(name):
    user_otp=request.form['otp']
    if otp==int(user_otp):
        cur = mysql.cursor()
        cur.execute("update users set verification = 'true' where username = '{uname}' ".format(uname=name))
        mysql.commit()
        return """<h3>Email varification succesfull</h3><br><a href="/signin">Go to home page...<a> """
    return "<h3>Please Try Again</h3>"

@app.route("/home:<user>/year:<yor>")
def mvbyyear(yor,user):
    
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select name,imageurl from movies where yor='{n}' order by name".format(n=yor)
       cur.execute(query)
       list = cur.fetchall()
       query = "select name,imageurl from movies where yor='{n}' and lang = 'telugu' order by name".format(n=yor)
       cur.execute(query)
       Tlist = cur.fetchall() 
       query = "select name,imageurl from movies where yor='{n}' and lang='kannada' order by name".format(n=yor)
       cur.execute(query)
       Klist = cur.fetchall()
       query = "select name,imageurl from movies,movieInfo where yor='{n}' and movieInfo.mvid = movies.mvid  order by rating desc".format(n=yor)
       cur.execute(query)
       Rlist = cur.fetchall()
       return render_template('yor.html',yofr=yor,lists = list,tlist = Tlist,klist = Klist,rlist=Rlist,user=user)


@app.route("/home:<user>/Accto:<cate>")
def cat(cate,user):
    
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       if cate  == 'actor':
            query = "select ac_name,ac_url from {n} where ac_name !='' order by ac_name".format(n=cate)
       elif cate == 'actress':
            query = "select acs_name,acs_url from {n} where acs_name != '' order by acs_name".format(n=cate)
       elif cate == 'Genre':
           query = "select name from Genre where name != '' order by name"          
       cur.execute(query)
       list = cur.fetchall() 
       return render_template('gallery.html',yofr=cate,lists = list,user=user)
   

@app.route("/home:<user>/genre:<genre>")
def mvbygen(genre,user):
    if  user!= '':
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid order by movies.name".format(n=genre)
       cur.execute(query)
       list = cur.fetchall()
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid and lang = 'telugu' order by movies.name".format(n=genre)
       cur.execute(query)
       Tlist = cur.fetchall()
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid and lang = 'kannada' order by movies.name".format(n=genre)
       cur.execute(query)
       Klist = cur.fetchall()
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid order by movieInfo.rating desc".format(n=genre)
       cur.execute(query)
       Rlist = cur.fetchall() 
       return render_template('yor.html',yofr=genre,lists = list,tlist = Tlist,klist = Klist,rlist=Rlist,user=user)
    else:
     return  redirect(url_for('login'))


@app.route("/home:<user>/actress:<acs>")
def mvbyacs(acs,user):
    if  user!= '':
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select name,imageurl from movies,actress where acs_name='{n}' and acs_id = acsid order by name".format(n=acs)
       cur.execute(query)
       list = cur.fetchall() 
       query = "select name,imageurl from movies,actress where acs_name='{n}' and acs_id = acsid and lang = 'telugu' order by name".format(n=acs)
       cur.execute(query)
       Tlist = cur.fetchall() 
       query = "select name,imageurl from movies,actress where acs_name='{n}' and acs_id = acsid  and lang = 'kannada' order by name".format(n=acs)
       cur.execute(query)
       Klist = cur.fetchall() 
       query = "select name,imageurl from movies,actress,movieInfo where acs_name='{n}' and acs_id = acsid and movies.mvid = movieInfo.mvid order by movieInfo.rating desc".format(n=acs)
       cur.execute(query)
       Rlist = cur.fetchall() 
       return render_template('yor.html',yofr=acs,lists = list,tlist = Tlist,klist = Klist,rlist=Rlist,user=user)

    else:
     return  redirect(url_for('login'))

@app.route("/home:<user>/actor:<ac>")
def mvbyac(ac,user):
    if  user!= '':
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select name,imageurl from movies,actor where ac_name='{n}' and actor.acid = movies.acid order by name".format(n=ac)
       cur.execute(query)
       list = cur.fetchall() 
       query = "select name,imageurl from movies,actor where ac_name='{n}' and actor.acid = movies.acid and lang = 'telugu' order by name".format(n=ac)
       cur.execute(query)
       Tlist = cur.fetchall() 
       query = "select name,imageurl from movies,actor where ac_name='{n}' and actor.acid = movies.acid and lang = 'kannada' order by name".format(n=ac)
       cur.execute(query)
       Klist = cur.fetchall() 
       query = "select name,imageurl from movies,actor,movieInfo where ac_name='{n}' and actor.acid = movies.acid and movieInfo.mvid = movies.mvid  order by movieInfo.rating desc".format(n=ac)
       cur.execute(query)
       Rlist = cur.fetchall() 
       return render_template('yor.html',yofr=ac,lists = list,tlist = Tlist,klist = Klist,rlist=Rlist,user=user)
    else:
     return  redirect(url_for('login'))

@app.route("/home:<user>/captain:<ac>")
def mvbydir(ac,user):
    if  user!= '':
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select name,imageurl from movies,Director,movieInfo where dir_name='{n}' and Director.dir_id = movieInfo.dir_id and movieInfo.mvid = movies.mvid order by name".format(n=ac)
       cur.execute(query)
       list = cur.fetchall() 
       return render_template('yor.html',yofr=ac,lists = list,user=user)
    else:
     return  redirect(url_for('login'))    

@app.route("/home:<user>/genre:<genre>")
def mvbygenr(genre,user):
    if  user!= '':
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid order by movies.name".format(n=genre)
       cur.execute(query)
       list = cur.fetchall()
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid and lang = 'telugu' order by movies.name".format(n=genre)
       cur.execute(query)
       Tlist = cur.fetchall()
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid and lang = 'kannada' order by movies.name".format(n=genre)
       cur.execute(query)
       Klist = cur.fetchall()
       query = "select movies.name,imageurl from movies,Genre,movieInfo where Genre.name='{n}' and movieInfo.gen_id = Genre.gen_id and movieInfo.mvid = movies.mvid order by movieInfo.rating desc".format(n=genre)
       cur.execute(query)
       Rlist = cur.fetchall() 
       return render_template('yor.html',yofr=genre,lists = list,tlist = Tlist,klist = Klist,rlist=Rlist,user=user)
    else:
      return  redirect(url_for('login')) 


def getcast(hero,heroine,Director,extra):
    temp=[]
    temp.append(hero)
    temp.append(heroine)
    other  = extra.split(", ")
    if len(other) == 1 :
        other = extra.split(",")
    for i in range(len(other)):
        temp.append(other[i])
    temp.append(Director)
    return temp    

def getimages(casts):
    cur = mysql.cursor()
    # cur=cur.cursor()
    temp=[]
    for i in range(len(casts)):
         t=[]
         query = "select ac_url from actor where ac_name = '{n}'".format(n=casts[i])
         cur.execute(query)
         t=cur.fetchall()
         if len(t) == 0 :
              query = "select acs_url from actress where acs_name = '{n}'".format(n=casts[i])
              cur.execute(query)
              t=cur.fetchall()
              if len(t) == 0 :
                  temp.append('https://st.depositphotos.com/2101611/4338/v/600/depositphotos_43381243-stock-illustration-male-avatar-profile-picture.jpg')
              else :
                  temp.append(t[0][0])

         else :
             temp.append(t[0][0])

    # temp.append('https://st.depositphotos.com/2101611/4338/v/600/depositphotos_43381243-stock-illustration-male-avatar-profile-picture.jpg')
    return temp     
                     

def getrelated(casts,mv):
    # temp = [[]]
    cur = mysql.cursor()
    # cur=cur.cursor()
    # lists = []
    query = "select name,imageurl from movies,actor where movies.acid = actor.acid and ac_name = '{n}' and name != '{m}'".format(n=casts[0],m=mv)
    cur.execute(query)
    temp = cur.fetchall()
    # temp = temp+lists
    # cur=cur.cursor()
    query = "select name,imageurl from movies,actress where movies.acs_id = actress.acsid and acs_name = '{n}' and name != '{m}'".format(n=casts[1],m=mv)
    cur.execute(query)
    lists = cur.fetchall()
    if len(lists) !=0 :
     temp = temp+lists
    query = "select name,imageurl from movies,movieInfo,Director where movies.mvid = movieInfo.mvid and dir_name = '{n}' and name != '{m}' and movieInfo.dir_id = Director.dir_id".format(n=casts[len(casts)-1],m=mv)
    cur.execute(query)
    lists = cur.fetchall()
    if len(lists) !=0 :
     temp = temp+lists 
    return temp


@app.route("/home:<user>/movie:<mv>")
def openmv(mv,user):
    if  user!= '':
       cur = mysql.cursor()
    #    cur = cur.cursor()  
       query = "select imageurl,yor,a.ac_name,ac.acs_name,dir_name,rating,mi.casting,g.name,mi.movieurl from movies,actor a,actress ac,Director d,Genre g,movieInfo mi where movies.name='{n}'  and movies.acid = a.acid and movies.acs_id = ac.acsid and movies.mvid=mi.mvid and g.gen_id=mi.gen_id and mi.dir_id=d.dir_id;".format(n=mv)
       cur.execute(query)
       list = cur.fetchall() 
       casts = getcast(list[0][2],list[0][3],list[0][4],list[0][6])
       cimg = getimages(casts)
       query = "select songname from songs,songsinfo,movies where songid=s_id and songsinfo.mvid = movies.mvid and movies.name='{n}'".format(n=mv)
       cur.execute(query)
       songs = cur.fetchall()
       rel = getrelated(casts,mv)
    #    query = ""
       return render_template('movie.html',user=user,moviename=mv,lists = list,totalcast = casts,images=cimg,length = len(casts),song = songs,related=rel)
    else:
     return  redirect(url_for('login'))


@app.route("/playsong:<songname>")
def playson(songname):
    # if user!='':
        cur = mysql.cursor()
        # cur = cur.cursor()
        query = "select songurl,singers,imageurl from songs,songsinfo,movies where songname = '{n}' and songid = s_id and songsinfo.mvid = movies.mvid".format(n=songname)
        cur.execute(query)
        list=cur.fetchall()   
        return render_template('playsong.html',movieimage = list[0][2],songurl = list[0][0],singers = list[0][1],songname=songname)
    # else:
    #     return redirect(url_for('login'))


@app.route("/playmovie:<name>")
def playmv(name):
    # if user!='':
        cur = mysql.cursor()
        # cur = cur.cursor() 
        query="select movieurl,imageurl from movieInfo,movies where movies.mvid=movieInfo.mvid and movies.name = '{n}'".format(n=name)
        cur.execute(query)
        url=cur.fetchall()
        img = url[0][1]
        url = url[0][0]  
        return render_template('playmovie.html',murl=url,image=img,moviename=name)
    # else:
    #     return redirect(url_for('login'))    


@app.route('/Admins',methods=['POST','GET'])
def admin():
    if request.method == 'POST' :
        queries = request.form['queries']
        querys.setquery(queries)
        return redirect(url_for('execute'))
    return render_template('admin.html')


@app.route('/exe')
def execute():

    arrays = querys.getquery().split(';')
    for iq in arrays:
        db = mysql.cursor()
        cursor = db.cursor()
        cursor.execute(iq)
        db.commit()
        db.close()
    return render_template('executed.html',queries = arrays)    


def getDirectors():
    # temp = []
    db = mysql.cursor()
    Cursor = db.cursor()
    Cursor.execute('select * from Director')
    temp = Cursor.fetchall()
    return temp


@app.route('/displaytables<table>')
def tables(table):
    cursor = mysql.cursor()
    query = 'select * from {n}'.format(n=table)
    cursor.execute(query)
    query = cursor.fetchall()
    return render_template('dt.html',tables=table,queries=query)

@app.route('/home:<user>/search:<inputs>')
def search(inputs,user):
    cursor = mysql.cursor()
    query = 'select ac_name,ac_url from actor'
    cursor.execute(query)
    actors = cursor.fetchall()
    query = 'select acs_name,acs_url from actress'
    cursor.execute(query)
    actress = cursor.fetchall()
    query = 'select name,imageurl from movies'
    cursor.execute(query)
    movies = cursor.fetchall()
    query = 'select songname,imageurl from songs,movies,songsinfo where songid = s_id and songsinfo.mvid = movies.mvid'
    cursor.execute(query)
    songs = cursor.fetchall()   
    query = 'select name from Genre'
    cursor.execute(query)
    genres = cursor.fetchall() 
    dirs = 'select dir_name from Director'
    cursor.execute(dirs)
    dirs = cursor.fetchall()
    return render_template('serch.html',user=user,ins=inputs,hero=actors,heroine=actress,cinema=movies,music=songs,types=genres,captains=dirs)

def getuid(user):
    # list =[['Dhummu dholi','https://archive.org/download/darbar_202106/%5BiSongs.info%5D%2001%20-%20Dhummu%20Dholi.mp3','https://moviestore.online/wp-content/uploads/2020/08/53be5688916d21740f8e89f05ac695c7.jpg','1'],['Dhummu dholi','https://archive.org/download/darbar_202106/%5BiSongs.info%5D%2001%20-%20Dhummu%20Dholi.mp3','https://moviestore.online/wp-content/uploads/2020/08/53be5688916d21740f8e89f05ac695c7.jpg','1'],['Dhummu dholi','https://archive.org/download/darbar_202106/%5BiSongs.info%5D%2001%20-%20Dhummu%20Dholi.mp3','https://moviestore.online/wp-content/uploads/2020/08/53be5688916d21740f8e89f05ac695c7.jpg','1'],['Dhummu dholi','https://archive.org/download/darbar_202106/%5BiSongs.info%5D%2001%20-%20Dhummu%20Dholi.mp3','https://moviestore.online/wp-content/uploads/2020/08/53be5688916d21740f8e89f05ac695c7.jpg','1']]
    cursor = mysql.cursor()
    query = "select uid from users where username = '{n}'".format(n=user)
    cursor.execute(query)
    list = cursor.fetchall()
    
    return list[0][0] 

@app.route('/home:<user>/<wl>')
def addwl(user,wl):
    userid = getuid(user)
    query = "Select mvid from movies where name = '{n}'".format(n=wl)
    Cursor = mysql.cursor()
    Cursor.execute(query)
    mvname = Cursor.fetchall()
    query = "Insert into watch_later values('{n}','{n1}')".format(n=userid,n1=mvname[0][0])
    Cursor.execute(query)
    mysql.commit()
    return redirect(url_for('watchl',user=user))


@app.route('/home:<user>/watchlater')
def watchl(user):
    if  user!= '':
        cursor = mysql.cursor()
        query = "select m.imageurl,mi.movieurl from movieInfo mi,movies m,watch_later wl,users u where mi.mvid=m.mvid and wl.mvid=mi.mvid and wl.userid = u.uid and u.username = '{n}'".format(n=user)
        cursor.execute(query)
        list = cursor.fetchall()
        return render_template('watchlater.html',user=user,wl=list,j=0)
    return  redirect(url_for('login'))     

@app.route("/home:<user>/playlist:<pname>")
def playplist(pname,user):
    # plist = getplist()
    if pname == 'init':
        cursor = mysql.cursor()
        query ="select plimg,name,p_id from playlist_name".format(n=getuid(user))
        cursor.execute(query)
        playlistdetails = cursor.fetchall()
        return render_template('playlist.html',user=user,pld = playlistdetails)
    else :
            cursor = mysql.cursor()
            query ="select plimg,name,p_id from playlist_name where  name like '%{n2}%'".format(n=getuid(user),n2=pname)
            cursor.execute(query)
            playlistdetails = cursor.fetchall()
            query = "select songname,singers,songurl,imageurl,p_id from playlist,songs,songsinfo,movies where p_id = '{n}' and songid = playlist.s_id and  songsinfo.s_id = songid and movies.mvid = songsinfo.mvid ".format(n=playlistdetails[0][3])
            cursor.execute(query)
            playlistsongs = cursor.fetchall()
            i = []
            for i in playlistdetails:
              if i[0] != playlistdetails[0][0]:
                query = "select songname,singers,songurl,imageurl,p_id from playlist,songs,songsinfo,movies where p_id = '{n}' and songid = playlist.s_id and  songsinfo.s_id = songid and movies.mvid = songsinfo.mvid ".format(n=i[3])
                cursor.execute(query)
                songs = cursor.fetchall()
                playlistsongs = playlistsongs+songs        
            return render_template('playlistplay.html',user=user,pld = playlistdetails,pls = playlistsongs)

if __name__ == '__main__':
    app.run(debug=True)

    # https://www.teahub.io/photos/full/197-1977278_prabhas-baahubali-movie-wallpapers-ultra-hd-bahubali-2.jpg
    # https://www.filmibeat.com/ph-big/2017/04/baahubali-2-conclusion-imax-poster_149206102400.jpg