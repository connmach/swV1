import  json 
import logging
from flask import Flask, render_template, redirect, url_for, request, session
import pymysql
import os
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/login')
def authentication():

   return render_template('index.html')

@app.route('/')
def index():
    error = None
    return render_template('index.html')
@app.route('/courses')
def courses():
    error = None
    return render_template('Courses _ Catalog.html')
@app.route('/course/python')
def coursePython():
    error = None
    return render_template('python1.html')
@app.route('/course/cs001', methods = ['POST', 'GET'])
def courseA():
    error = None
    return render_template('cs001.html')

@app.route('/course/testcs_page')
def courseB():
    error = None
    return render_template('testcs_page.html')



@app.route('/course/tutorial/functions', methods = ['POST', 'GET'])
def tutorial():
    pass
    return render_template('Tut001.html')

@app.route('/blog/art001')
def article():
    error = None
    return render_template('art001.html')


@app.route('/blog')
def articles():
    error = None
    return render_template('blog.html')

@app.route('/engine/qnRepo/<qno>/', methods = ['POST', 'GET'])
def qnRepo_old(qno):

   app.logger.info('**************************************************Processing default request input' + qno)

   row= retrieveQn(qno)


   print(row);

   resultObj=("success");
   errorObj = None
   error = None
   msg=None
   status="200";
   app.logger.info('**************************************************Processing ++ row request' + str(row[0])  )
   print(row[0])
   list(row)
   print(list(row))
   topicDesc=str(row[1])
   instruction=str(row[2])
   exercise=str(row[3])
   section=str(row[4])
   out= json.dumps({'status': 'OK', 'topicDesc':topicDesc,'instruction': instruction,'exercise': exercise,'section': section})
   return out;


@app.route('/engine/eval/python/', methods = ['POST', 'GET'])
def evalEngine():
   temp=request.form['ans'];
   empId=request.form['EmpId']
   qno=request.form['QNo']

'''
      //create folder in the server with employee id
     //write the content to file in the server answer.py
     // write the content to the database
     // time out of the session
     // invoke the shell script
     // if there is success file update the learning history
//  else if error file then update accordingly and return the error result to db and return. also give a tip to the student

     // write the result to the databsae
     // make the question complete
     // on error show the error in console.
     // on success move to the next question.
     // status success/failure
    // updation of learnin history and user history
    // update course/ section completion
    // update the score and remaining acitivities
     // update the question
  // initiate the docker container

 
   ans="*"
   print(ans);
   key= empId +"_" + qno;
   qaassoc_obj =();
   resultObj=("success");
   errorObj = None
   error = None
   msg=None
   dbStatus=insertIntoQA_Assoc(key,empId,qno,temp,out)
   return json.dumps({'status': 'OK', 'testStatus': out, 'pass':temp, 'empId':empId, 'key':key, 'DbStatus':dbStatus});
'''
def connect():
    MYSQL_HOST= 'socialwings.mysql.pythonanywhere-services.com'
    MYSQL_USER= 'socialwings'
    MYSQL_PASSWORD='Tech@1234'
    MYSQL_DB='socialwings$sw_ilp'

    conn=MySQLdb.connect (MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB)

    return conn;



def insertIntoQA_Assoc(key,empId,qno,temp,out):
    status="*"
    try:

        conn=connect();
        cur=conn.cursor()
        print("Connected to SQLite")


        cur.execute("INSERT INTO qa_assoc(qa_id,empid,question,answer,stauts) VALUES(%s,%s,%s,%s,%s)",(key,empId,qno,temp,out))
        conn.commit();
        status="commit "
        print("inserted into qa_assoc")
        status="inserted row"
        status = status + " 2.success"

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        status = status + "error"
    finally:
        if (conn):
            conn.close()
            print("The Sqlite connection is closed")

    return status;


def retrieveQn(qno):
    status="*"
    try:
 #       query="select * from assignments where id=%s;"

   #A_assignments
        query="select * from A_assignments where assngNo=%s;"
        conn = connect()
        cur=conn.cursor()
        cur.execute(query, [qno])
        rv = cur.fetchall()
  #      app.logger.info('**************************************************Preparing connection request')
        print("Connected to SQLite")
        print("retrieve question from repo" )
        app.logger.info('*****-----------------------------------Processing default request')
        print(rv)
        return rv[0];


    except sqlite3.Error as error:
        app.logger.info("******Failed to read data from sqlite table", error)
        status = status + "error"


    finally:
        if (conn):
            conn.close()
            app.logger.info("The Sqlite connection is closed****")

    return null;



## digi


def digi_connect():
    MYSQL_HOST= '46.101.210.184'
    MYSQL_USER= 'root'
    MYSQL_PASSWORD='root'
    MYSQL_DB='EDUWINGS_DB'
    PORT=3307
    conn=pymysql.connect(
    host = MYSQL_HOST,
    user = MYSQL_USER,
    passwd = MYSQL_PASSWORD,
    db = MYSQL_DB,
    port = PORT)

    return conn;






### check if the question is lesser than current question
## then retrieve the answer
def digi_retrieveQn(qno):
    status="*"
    try:
 #       query="select * from assignments where id=%s;"

   #A_assignments
        query="select * from Tasks where TaskId=%s;"
        conn = digi_connect()
        cur=conn.cursor()
        cur.execute(query, [qno])
        rv = cur.fetchall()
  #      app.logger.info('**************************************************Preparing connection request')
        print("Connected to SQLite")
        print("retrieve question from repo" )
        app.logger.info('*****-----------------------------------Processing default request')
        print(rv)
        return rv[0];


    except sqlite3.Error as error:
        app.logger.info("******Failed to read data from sqlite table", error)
        status = status + "error"


    finally:
        if (conn):
            conn.close()
            app.logger.info("The Sqlite connection is closed****")

    return null;
@app.route('/engine/python/qnRepo/<qno>/', methods = ['POST', 'GET'])
def qnRepo_new(qno):

   app.logger.info('**************************************************Processing  digi request input' + qno)

   row= digi_retrieveQn(qno)


   print(row);

   resultObj=("success");
   errorObj = None
   error = None
   msg=None
   status="200";
   app.logger.info('**************************************************Processing ++ row request frm digi Tasks Table' + str(row[0])  )
   print(row[0])
   list(row)
   print(list(row))

   TaskId 	=str(row[0])
   TaskName 	=str(row[1])
   TaskDesc 	=str(row[2])
   TaskOwnerId  	=str(row[3])
   instruction 	=str(row[4])
   exercise	=str(row[5])
   answer	=str(row[6])
   taskType	=str(row[7])
   marks	=str(row[8])
   linkedQuestion	=str(row[9])
   authorId	=str(row[10])
   reviewerId  	=str(row[11])
   courseId  	=str(row[12])
   app.logger.info("finished processing")
   return json.dumps({'status': 'OK', 'topicDesc':TaskDesc,'instruction': instruction,'exercise': exercise,'section': 'Python Basics'})

if __name__ == "__main__":
    print("enter the port")
 #   inport=input()
    port = int(os.environ.get("PORT",  8098))
    app.run(debug=False,host='0.0.0.0',port=port)
