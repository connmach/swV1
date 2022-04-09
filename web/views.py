import  json 
import logging
from flask_github import GitHub
from flask import Flask, render_template, redirect, url_for, request, session
from flask import jsonify
#import pymysql
import requests
from web import app 
import os
import config
import utils.Utils as Utils
from authlib.client import OAuth2Session
from flask_oauth import OAuth
import google.oauth2.credentials
import googleapiclient.discovery
import pathlib

project_dir = pathlib.Path(__file__).resolve().parent.parent
web_dir = project_dir/'core'
template_dir = project_dir/'templates'
static_dir = project_dir/'static'
config_file = project_dir/'config.py'
#app = Flask(
#    __name__,
#    template_folder=template_dir,
#    static_folder=static_dir ) 

	
github = GitHub(app)


ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE ='openid email profile'

AUTH_REDIRECT_URI =  "https://www.socialblocks.in/course/google/auth"
 
CLIENT_ID = "314250832461-3kged24hlf981rrg1ki4csebj5imbukl.apps.googleusercontent.com"
CLIENT_SECRET = "i5EJyqio3EOXHRYuoGUHu5l1"
AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'

#facebook
SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '831034017556271'
FACEBOOK_APP_SECRET = '59baa3c81f16e5b5c4dbbb57530f2171' 




oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

 
@app.route('/course/fb/login')
def fblogin():
 pass  
#  return facebook.authorize(callback=url_for('facebook_authorized',
  #      next=request.args.get('next') or request.referrer or None,
  #      _external=True))


@app.route('/course/fb/auth')
 
def facebook_auth_redirect(): 
 
    session['userid']= "test"
    session['user_info'] ="test"
    session['myCourses']='{"A01","A03" }' 

    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    session['LH']= result
    out=session['LH']
    resDict=json.loads(out)
    app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))

    app.logger.info('*****Login:LH history from session****** status{0} result{1}'.format( status, result))

 
    session['Badge'] = "ninjaBeginner"
    session['LHHours'] ="30"
    session['Score'] = "2.0"
    session['LearningTrack'] = "Foundation"

#recent courses
    session['recentCourses']  =["cs001","cs003"]



    return redirect(url_for('homePage',userId=user_info['given_name']))





@app.route('/login_old')
def authentication():

   return render_template('index.html')

@app.route('/course/google/login') 
def googlelogin():
    gses  = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)
  
    uri, state = gses.authorization_url(AUTHORIZATION_URL)
    session[AUTH_STATE_KEY] = state
    app.logger.info('*******Auth state {0} {1}'.format(str(session[AUTH_STATE_KEY]),state))
    session.permanent = True

    return  redirect(uri, code=302)

@app.after_request
def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

def is_logged_in():
    return True if AUTH_TOKEN_KEY in session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens =  session[AUTH_TOKEN_KEY]
    
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)
def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()

@app.route('/course/google/auth')
def google_auth_redirect():
    req_state = request.args.get('state', default=None, type=None)
    app.logger.info('*******Auth state {0} '.format(req_state))
    session[AUTH_STATE_KEY]=req_state
   # if req_state !=  session[AUTH_STATE_KEY]:
   #      response =  make_response('Invalid state parameter', 401)
   #      return response
    
    gses = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state= session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = gses.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=request.url)

    session[AUTH_TOKEN_KEY] = oauth2_tokens
    user_info = get_user_info()
    session['userid']=user_info['given_name']
    session['user_info'] =user_info
    session['myCourses']='{"A01","A03" }' 

    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    session['LH']= result
    out=session['LH']
    resDict=json.loads(out)
    app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))

    app.logger.info('*****Login:LH history from session****** status{0} result{1}'.format( status, result))
    session['Badge'] = "ninjaBeginner"
    session['LHHours'] ="30"
    session['Score'] = "2.0"
    session['LearningTrack'] = "Foundation"
    session['recentCourses']  =["cs001","cs003"]
    return redirect(url_for('homePage',userId=user_info['given_name']))

@app.route('/course/google/logout')
 
def glogout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)

@app.route('/common/flappyExpectedOutput')
def expectedOutput():

        page=config.expectedOutput        
        return render_template(page) 

 
@app.route('/common/flappyOutput')
def Output():

        page=config.output        
        return render_template(page) 

 
@app.route('/videoProctoring')
def videoProctoring():

   return render_template('/courseHome/common/videoProctoring.html')



@app.route('/connect-console')
def console():
    app.logger.info(" *****Console *** ")

@app.route('/feedback/<cid>/<userId>/<taskId>/<taskType>/<actionMsg>/', methods = ['POST', 'GET'])
def getResult(cid,userId,taskId,taskType,actionMsg):
#
    action= actionMsg
    app.logger.info('******* feedback process'+ cid+" "+userId+" "+action+" "+taskId )

    data = {"courseId": cid, "taskId":taskId, "taskType":taskType ,"userId": "guest","action":action}

    try:
       response=requests.post(config.gradingURL,json= data ) 
       jsonResponse = response.json()
       app.logger.info(f"******json response {action} {taskType} received"+ response.json())
       json_data =  response.json()  

 

       return render_template('/courseHome/feedback/feedback.html',TaskAction=action,TaskType=taskType ,extends_base="False",TestStatus="Success" ,execData=json.loads(json_data))  

    except  requests.exceptions.RequestException as error:
        app.logger.info("******Moduel  retrieval request failed", error)
        page=config.page500          
        return render_template(page), 500    


  
    app.logger.info('******* request- TaskDetails URL:-{0} data- {1}'.format(config.questionRepoURL, json.dumps(data)))
    pno=2
    fno=2
    TotalTC=4
    out="Hello World!" 
    TaskType = "pyTask"
    action = "RunTest"
    json_data=json.dumps({'TaskAction':"RunTest",'NoPassed':pno,'NoFailed':fno,'TotalTC':TotalTC})
#    json_data=json.dumps({'TaskAction':"Run",'CompileStatus':"Success",'Message':out,'TaskType':action})

    return render_template('/courseHome/feedback/feedback.html',TaskAction=action,TaskType="pyTask",extends_base="False",TestStatus="Success" ,execData=json.loads(json_data))  


@app.route('/test')
def test1():
    user='guest'
#    session['LH']={"A07":"M01,sc01,A01_2,30%,40%","A08":"M01,sc01,A03_2,20%,10%","A01":"M01,sc01,A01_2,30%,40%","A03":"M01,sc01,A03_2,20%,10%","A05":"M01,sc01,A05_2,20%,10%","A06":"M01,sc01,A06_2,20%,10%" }
    session['userid'] = 'guest'  
    session['myCourses']='{"hk01","A03" }'
    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    session['LH']= result
    cid="hk01"
    mid="M001"
    qn="hk01_3"
    return redirect("hackathon/hk01/hk01_3")

#WEB
'''   app.logger.info("****** Test path invoked")
    user='guest'
#    session['LH']={"A07":"M01,sc01,A01_2,30%,40%","A08":"M01,sc01,A03_2,20%,10%","A01":"M01,sc01,A01_2,30%,40%","A03":"M01,sc01,A03_2,20%,10%","A05":"M01,sc01,A05_2,20%,10%","A06":"M01,sc01,A06_2,20%,10%" }


    session['userid'] = 'guest'  
    session['myCourses']='{"A01","A03" }'
    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    session['LH']= result
    cid="A05"
    mid="M001"
    qn="A05_2"
#   get the Learning history
'''
  
 #   return redirect(url_for('getModulePageParticularQn',cid=cid,mid=mid,taskId=qn))'''

#HACKATHON

#    
#currentOutput 
#
@app.route('/solution/<userId>/<taskId>/',methods = ['POST','GET'])
def userSolution(userId,taskId):
    error = None

    try:
       userid=   session['userid']
       page=f"/root/Environment/Dev/scratchpad/users/{userId}/{taskId}/solution.html"       
       return render_template(page) 
    except  requests.exceptions.RequestException as error:
       app.logger.info("******Platform service failed", error)
       return None

@app.route('/Scratchpad/<courseId>/',methods = ['POST','GET'])
def htmlScratchpad(courseId):
    error = None
    userid=   session['userid']

#    page=f"/htmlScratchpad/{userid}/{courseId}/solution.html".format( userid , password ))
    SubmissionServiceURL=config.SubmissionServiceURL
    fileName="solution.html"
      

    data ={"userId":userid,"TaskId": "A05_07","TaskAction": "readService","fileName": fileName, "courseId": courseId}
    try:
       response=requests.post(SubmissionServiceURL,json= data )
       jsonResponse = response.json()
       app.logger.info("******Platform service successful")
       res=json.loads(jsonResponse )
       return  res["Contents"]
    except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service failed", error)
        return None

@app.route('/')
def index():
    error = None
    return render_template(config.marketingPage)

@app.route('/catalog')
def courses():
    error = None
    userDetails=   session['userid']
    return render_template('/courseHome/Courses_Catalog.html',profile=userDetails)
@app.route('/LearningPathWeb')
def LearningPath():
    error = None
    userDetails= session['userid']
    return render_template('/LearningPathWeb.html',profile=userDetails)

@app.route('/course')
def courseLogin():
    error = None
    return render_template(config.loginPage)

@app.route('/course/logout')
def logout():
      session.pop('userid', None)
 
      return redirect(url_for('courseLogin'))

@app.route('/gitlogin' ,methods = ['POST'])
def gitLogin(): 

    return github.authorize()

 
@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    
    app.logger.info("User" + oauth_token)

    if oauth_token is None:
        flash("Authorization failed.")
 

    user='guest'
    session['userid'] = 'guest'  
    session['userid'] = 'guest'  
    session['myCourses']='{"A01","A03" }'
    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

#   get the Learning history

#    session['LH']={"A07":"M01,sc01,A01_2,30%,40%","A08":"M01,sc01,A03_2,20%,10%","A01":"M01,sc01,A01_2,30%,40%","A03":"M01,sc01,A03_2,20%,10%","A05":"M01,sc01,A05_2,20%,10%","A06":"M01,sc01,A06_2,20%,10%" }


    session['LH']= result
    out=session['LH']
    resDict=json.loads(out)
    app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))

    app.logger.info('*****Login:LH history from session****** status{0} result{1}'.format( status, result))
 
    session['Badge'] = "ninjaBeginner"
    session['LHHours'] ="30"
    session['Score'] = "2.0"
    session['LearningTrack'] = "Foundation"
    session['recentCourses']  =["cs001","cs003"]    
#    user.github_access_token = oauth_token

 #   github_user = github.get('/user')
 #   github_id = github_user['id']
 #   github_login = github_user['login'] 
 #   app.logger.info('***** Github User{0} Id{1} login{2}'.format( github_user, github_id,github_login))  

    return redirect(url_for('homePage',userId=user ))
     
@github.access_token_getter
def token_getter():
    user = g.user
    app.logger.info('*************** username {0} '.format( user   ))
    if user is not None:
        return user.github_access_token

#B1
@app.route('/course/login' ,methods = ['POST'])
def courseLoginSubmit():
    app.logger.info('*************** login page')

    error = None
    userid=request.form['email'];
    password=request.form['password'];
    print(userid)
    app.logger.info('*************** username {0} {1}'.format( userid , password ))
    session['userid'] = userid.split("@")[0]
    app.logger.info('*************** username {0} '.format( session['userid'] ))
    session['myCourses']='{"A01","A03" }'

#bug1 
    session['Badge'] = "ninjaBeginner"
 
    session['recentCourses']  =["cs001","cs003"] 
#  check services
    if checkServices("test")== False:
      app.logger.error('*****Health check Error')
 
      page=config.page500          
      return render_template(page,msg="Platform services is down"), 500  
    else: 
        app.logger.info('*****Health check Success')
    app.logger.info('*****role history' )
#   get the Learning history

    session['user_info']=userid 

    if userid=="guest@sw.com" and password=="guest":
       session['role']="admin" 
       app.logger.info('***************loggedin_v3.0' )


    elif userid=="tanu@sw.com" and password=="guest":
       session['role']="admin" 
       app.logger.info('***************loggedin_v2.0' )

    elif userid=="guest11@sw.com" and password=="guest11":
       app.logger.info('***************loggedin_v2.0' )
 

    elif userid=="ninja@sw.com" and password=="ninja":
       session['role']="admin" 
       app.logger.info('***************loggedin_v2.0' )
       return redirect("http://192.46.208.71:3000/pages/home/userId=userid",)

    elif userid=="shankar@sw.com" and password=="shank":

       app.logger.info('***************loggedin_v2.0' +userId )
 

    elif userid=="sreyas@sw.com" and password=="sreyas":
       session['role']="student" 
       app.logger.info('***************loggedin_v2.0' +userid)
 

    elif userid=="sagar@sw.com" and password=="sagar":
       session['role']="teacher" 


    else:
       app.logger.info('***************invalid username' )
       error="Invalid userId and password" 
       return render_template(config.loginPage,msg=error)
    role=session['role']
    app.logger.info(f'***************loggedin_v2.0 {userid} {role}')
    role=session['role']
    if role =="student":

       status,result=fetchLHAll(session['userid'])
       session['LH']= result
       out=session['LH']
       resDict=out
       app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))
       app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    elif role =="teacher":
       status,result=fetchLHAll(session['userid'])
       session['LH']= result
       out=session['LH']
       resDict=out
       app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))
       app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    elif role =="admin":  
       status,result=fetchLHAll(session['userid'])
       session['LH']= result
       out=session['LH']
       resDict=out
       app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))
       app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))
    elif role =="guest":  
         pass
    return redirect(url_for('homePage',userId=userid ))    

@app.route('/course/home' ,methods = ['POST','GET'])
def homePage():
    app.logger.info('***************Home page v2.0' )
    error = None
    userDetails=session['user_info']
    userId=session['userid']
    LH=session['LH']
    app.logger.info(f'***************Home page v2.0 {LH}' )
    role=session['role']

    tasktemplate='''
 
          <tr>      
             <td>#1# </td>
             <td>#2#</td>
             <td>#3#</td>
             <td>#4#</td>
             <td>#5#</td>
         </tr>
 
             '''


    tasks=[{"id":"01","description":"Induction to course","date":"12/08/21","author":"Nirmal","category":"General","status":"pending"},
           {"id":"02","description":"Introduction to Java course","date":"12/08/21","author":"Mentor San","category":"General","status":"pending"},]


    userDetails=session['userid']
    taskList=[]
    for i in range(len(tasks)):
      obj=tasks[i]
      app.logger.info('***************Webinar page v2.0' + str(len(obj)) + str(type(obj)))
      app.logger.info('***************Webinar page v2.0' + obj["id"] )

      arr=[obj["id"],obj["description"],obj["category"],obj["author"],obj["date"],obj["status"]]  
     # item=Utils.createStringTemplate(tasktemplate,arr)
      #taskList.append(item) 
    #app.logger.info('***************Webinar page v2.0' +  str(taskList))



    activities=  {"pending":[{
	"Id": "A01",
	"desc": "Java Basics",
	"date": "12/12/2021",
	"author": "Nirmal",
                     "status": "Pending"  
                      },
                     {
	"Id": "A02",
	"desc": "Java Basics",
	"date": "12/12/2021",
	"author": "Nirmal",
                     "status": "Pending"  
                      },
                     {
	"Id": "A03",
	"desc": "Java Basics",
	"date": "12/12/2021",
	"author": "Nirmal",
                     "status": "Pending"  
                      },
                      {
	"Id": "A04",
	"desc": "Java Basics",
	"date": "12/12/2021",
	"author": "Nirmal",
                     "status": "Pending"  
                      }]}
    userDetails={    "notifications": "3",
	"learningPathCrnt": "foundation",
	"learningPathNxt": "Ninja Practitioner",
	"ninjaScore": LH['totScore'], 
	"totQnCompletedCnt": LH['totCompletedQnCourse'],
	"learningHistory": "10",
                     "completedCourse":LH['totCompletedCourse'],

	"lastLogin": "21/12/21 12:20",
	"userName": userId,
	"badgeList": ["badge", "badge2"]
               }

    webinarHistory= {"webinarHistory": [{
	"webinarId": "foundation",
	"desc": "Web",
	"date": "50",
	"time": "10",
	"author": "10"}
                      ,{"webinarId": "foundation",
	"desc": "Web",
	"date": "50",
	"time": "10",
	"author": "10"},
                     {"webinarId": "foundation",
	"desc": "Web",
	"date": "50",
	"time": "10",
	"author": "10"}]
                    }
    courseHistory=  {"courseHistory":[{
	"courseId": "B02",
	"moduleId": "M001",
                     "courseDesc":"introduction to blockly", 
                     "progress":"10",
	"taskId": "B02_1",
	"moduleDesc": "Module 1",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "Continue"  
                      }
                      ,   

                     {
	"courseId": "A01",
	"moduleId": "M001",
                     "courseDesc":" Introduction to <br> Python", 
                     "moduleDesc":"Module 1",

                     "progress":"10",
	"taskId": "A01_1",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "Continue"  
                     },


                   {
	"courseId": "A05",
	"moduleId": "M001",
                     "courseDesc":" Introduction to <br> HTML", 
                     "moduleDesc":"Module 1",

                     "progress":"10",
	"taskId": "A05_1",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "Continue"  
                     },
                     {
	"courseId": "H01",
	"moduleId": "M001",
                     "courseDesc":"Introduction to <br> CSS", 
                     "moduleDesc":"Module 1",
                     "progress":"10",
	"taskId": "A02_1",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "Continue"  
                     },
                      {"courseId": "H01", 
     	 "moduleId": "M001",
                     "courseDesc":"Introduction to <br> Javascript", 
                     "moduleDesc":"Module 1",
                      "progress":"10",
	 "taskId": "A02_1",
	 "date": "12/12/2021",
	 "time": "10",
	 "author": "10",
                      "status": "Pending"}]
                    }
    testHistory=  {"testHistory":[{
	"testId": "foundation",
	"desc": "Web",
	"date": "50",
	"time": "10",
	"author": "10"}
                      ,{"testId": "foundation",
	"desc": "Web",
	"date": "50",
	"time": "10",
	"author": "10"},
                     {"testId": "foundation",
	"desc": "Web",
	"date": "50",
	"time": "10",
	"author": "10"}]
                    }

    app.logger.info('***************loggedin_v2.0'+ userId )
    role=session['role']
    page=config.home.format(config.homeMain,config.rolesPage[role])
    return render_template(page,result=LH,activities=taskList,details=userDetails,webinarHistory=webinarHistory,courseHistory=courseHistory,testHistory=testHistory,userId =userId )

 



@app.route('/eduninja/history/', methods = ['POST', 'GET'])
def learningHistroy():
    courseList=session['myCourses']
    LH=session['LH']
    badge=session['Badge'] 
    hours=session['LHHours']
    Score=session['Score']  
    track=session['LearningTrack'] 

    out= json.dumps({ 'courseList': courseList,'LH': LH,'badge': badge, 'hours':hours,'Score': Score,'track': track })
    return out

@app.route('/eduninja/setCurrentQn/<qno>')
def setCurrQn(qno):
    if 'userid' in session:
       session['currQn']=qno
    else:
      return redirect(url_for('courseLogin'))
    error = None
    app.logger.info('***************'+ courseId  )

    page='	'
    return render_template(page) 
 
def getCourseDetails(cid):

   data ={"courseId":cid,"TaskAction":"getCourseDtls"}
   courseDetailsUrl=config.questionRepoURL

   try:
       response=requests.post(courseDetailsUrl,json= data )
       jsonResponse = response.json()
       app.logger.debug(f"******Platform service getCourseDtls retrieval successful {jsonResponse}")
       return  json.loads(jsonResponse)  
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service getCourseDtls retrieval failed", error)
        return False,None


'''   courseUserDetails=[         {      "courseId": "A01",
                 	                     "totModules": 3,
                                          "courseStatus": "Start",
                             	"Modules": [{
			"Mid": "1",
			"MHead": "Introduction to python",
			"MType": "Course",
			"MDesc": "Introduction to python",
                                                               "TaskId":["A01_3","A01_13","A01_13"],
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		           },
		           {
			"Mid": "2",
			"MHead": "Writing reusable code",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_3","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		         {
			"Mid": "3",
			"MHead": "Quiz",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MType": "Course",
			"MDesc": "Check your knowledge in this final part of the course!",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		        }]},

                                 {        "courseId": "A02",
                 	                     "totModules": 3,
                                          "courseStatus": "Start",
                             	"Modules": [{
			"Mid": "1",
			"MHead": "Introduction to Java",
			"MType": "Course",
			"MDesc": "Introduction to python",
                                                               "TaskId":["A01_3","A01_13","A01_13"],
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		           },
		           {
			"Mid": "2",
			"MHead": "Java operators and conditional operations",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		           {
			"Mid": "3",
			"MHead": "Writing reusable code",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		           {
			"Mid": "4",
			"MHead": "Java classes",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		           {
			"Mid": "5",
			"MHead": "Arrays",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		         {
			"Mid": "6",
			"MHead": "Quiz",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MType": "Course",
			"MDesc": "Check your knowledge in this final part of the course!",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		        }
                                                  ]},
                                 {        "courseId": "A05",
                 	                     "totModules": 3,
                                          "courseStatus": "Start",
                             	"Modules": [{
			"Mid": "1",
			"MHead": "Introduction to Java",
			"MType": "Course",
			"MDesc": "Introduction to python",
                                                               "TaskId":["A01_3","A01_13","A01_13"],
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		           },
		           {
			"Mid": "2",
			"MHead": "Java operators and conditional operations",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		           {
			"Mid": "3",
			"MHead": "Writing reusable code",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		           {
			"Mid": "4",
			"MHead": "Java classes",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		           {
			"Mid": "5",
			"MHead": "Arrays",
			"MType": "Course",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MDesc": "Discover how to write your own functions and use them later multiple  times.",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		         },
		         {
			"Mid": "6",
			"MHead": "Quiz",
                                                               "TaskId":["A01_3","A01_9","A01_13"],
			"MType": "Course",
			"MDesc": "Check your knowledge in this final part of the course!",
			"totalExercises": "10",
			"completedExercises": "0",
			"status": "Start"
		        }
                                                  ]}


                                           ] 

   jsonout=json.loads(courseUserDetails)
   app.logger.debug(f'..................// Course {jsonout} ')

   for course in jsonout:
      if course['courseId']==cid:
         app.logger.debug(f'*************** Course {cid} -learning history' + course['courseId'])
         app.logger.debug(f'                       ***************')
         return course
   return None  
'''  
# course page

@app.route('/course/<cid>')
def courseIndex(cid):
    return redirect(url_for('coursePage',cid=cid,status="Module"))

#0
@app.route('/course/sb')
def marketingHome():
   error = None
   return render_template(config.marketingPage)
@app.route('/course/sw')
def swgHome():
   error = None
   return render_template(config.swPage)

@app.route('/course/sw/contact')
def marketingContact():
   error = None
   return render_template(config.sw_contact)

@app.route('/course/sw/about')
def marketingAbout():
   error = None
   return render_template(config.sw_about)

#game
#taskId

@app.route('/course/<cid>/game/name=<name>/level=<level>')
def gamePage(cid,name,level):
    app.logger.debug(f'..................// Course {cid}- {name} -  - V2.0')


    if 'userid' in session:

      userId = session['userid']
      app.logger.debug(f'.................. logged in // Course {cid}- {userId } -  - V2.0')
    else:
      return redirect(url_for('courseLogin'))
    error = None

    app.logger.debug(f'..................// Course {cid}- {name} -  - V1.0')
    if cid=="B02":
      app.logger.debug(f'..................// Course {cid}- Game {name} - {level}  - V1.0')
      return render_template(config.gameHolder.format(config.courseBase,cid,name) ,cid=cid,name=name,level=level)

@app.route('/course/<cid>/<status>')
def coursePage(cid,status):
    app.logger.debug(f'..................// Course {cid}- {status} -  - V1.0')

    courseStatus=status 
    if 'userid' in session:
      userId = session['userid']
    else:
      return redirect(url_for('courseLogin'))
    error = None
    if cid=="B02":
      return render_template(config.gameIndex)


    status,courselhObj=getLH(userId,cid)
    app.logger.debug(f'..................// Course {cid}- {status} -learning history {courselhObj} - V1.0')
 
    cidHead=f"{cid}"
    app.logger.debug(f'*************** Course {cid} -learning history {courselhObj}')
    courseMetaData=getCourseDetails(cid)
    app.logger.debug(f'*************** Course Metadata {courseMetaData}  ')
    if 'courseId' not in courselhObj:
       app.logger.info(f'*******  Course has not yet started {cid }' )
       courselhObj={}
       courselhObj['courseId']=cid
       courselhObj['cQnCnt']=0
       courselhObj['cstatus']='Start' 
       app.logger.info('*******  courseDetails is in progresss:' +   str(courselhObj) )
 

       insertCourseHistory(userId,cid,"M001")
 

    else:
       courseMetaData['courseStatus']="inprogress"
       for mdCnt in   range(courseMetaData['totModules']):
         modId=mdCnt+1
         midHead=f"M{modId}_head"
         app.logger.debug(f'******* processed for module- {midHead} ' )

         if midHead in courselhObj["Modules"]: 
             app.logger.debug(f'******* processed for module-{midHead} // {courselhObj["Modules"][midHead ][9]} // {courselhObj["Modules"][midHead ][8]}' )
             courseMetaData['Modules'][mdCnt]['completedExercises']=courselhObj["Modules"][midHead ][8]
             app.logger.debug(f"******* processed for module-{midHead} // {courseMetaData['Modules'][mdCnt]['status']} // {courseMetaData['Modules'][mdCnt]['completedExercises']}" )

             if courselhObj["Modules"][midHead ][9]!="done":
                courseMetaData['Modules'][mdCnt ]['status']='Progress'
             else:
                courseMetaData['Modules'][mdCnt]['status']='Completed'
     #  app.logger.debug(f"******* processed for module-{mdCnt } // {courseMetaData['Modules'][mdCnt ]['status']} // {courseMetaData['Modules'][mdCnt ]['completedExercises']}" )
       app.logger.info('*******  courseDetails is in progresss:' +   str(courseMetaData))
      
    app.logger.debug('*************** course learning history'+ str(courselhObj))
    return render_template(config.courseIndex.format(config.courseBase,cid),courseStatus=courseStatus,pageStatus=status,cid=cid,courseDetails=json.dumps(courseMetaData),courseHistoryDetails=courselhObj)


def insertCourseHistory(userId,cid,moduleId):

   learningHistoryURL=  config.learningHistoryURL
   taskId=getQn(cid,moduleId)
   app.logger.debug("****** Coreplatform:- insertCourseLH - {cid} {moduleId} successful")
   data ={"userId":userId,"courseId":cid,"moduleId":moduleId,"taskId":taskId,"action":"InsertCourseLH", "type":'course'}

   try:
       response=requests.post(learningHistoryURL,json= data )
       jsonResponse = response.json()
       app.logger.info("******Platform service insertCourseLH successful")
       return True, jsonResponse  
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service insertCourseLH failed", error)
        return False,None


#Pending module/ progressModule
# what will you do if the current module is pending
  
def checkModulePendingInHistory(cid,mid,LH):
           
     app.logger.debug("****** LH:checkModulePendingInHistory" + str(LH))
     mod=LH["Modules"] 
     mhead=f"{mid}_head" 
     app.logger.debug("****** LH:checkModulePendingInHistory" + str(mod))

     for modObj in mod:
       app.logger.debug("****** LH:checkModulePendingInHistory" + str(modObj))
       if   mhead in modObj:
          app.logger.debug(f"****** checkModulePendingInHistory {modObj[mhead]} {mhead}")
          if (modObj[mhead][9]== "pending" or  modObj[mhead][9]== "progress" or modObj[mhead][9]== "done") :
             app.logger.debug("****** checkModulePendingInHistory status" )
             return True
          else:
            app.logger.info(f"****** checkModulePendingInHistory Module {mid} not available")
            return False
       else:
         app.logger.debug(f"****** checkModulePendingInHistory key not found  {mhead}")
 

def updateTaskHistory(cid,mid):
    pass


#updateModuleHistoryStatus
#called from :getModulePageParticularQn
#(userId,cid,moduleId,taskId,status)
#external call:config.learningHistoryURL ->updateCourseStatus(loginId,courseId,moduleId,taskId,status,) 
# action"XMT"
 
#
#Processing:
#
#
#Output
def updateModuleHistoryStatus(userId,cid,moduleId,taskId,status):

   learningHistoryURL=  config.learningHistoryURL
   data ={"userId":userId,"courseId":cid,"moduleId":moduleId,"taskId":taskId,"status":status,"action":"UpdateCourseStatusLH" }

   try:
       response=requests.post(learningHistoryURL,json= data )
       jsonResponse = response.json()
       app.logger.info("******Platform service updateModuleHistoryStatus M{moduleId} T {taskId } status- {status} successful")
       return True, jsonResponse  

   except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service updateModuleHistoryStatus M{moduleId} T {taskId } status- {status}, processing failed", error)
        return False,None


def getNxtQn(cid,mid,taskId):
   cnt=int(mid[3:4])-1
   if cnt==  len(modules):
      pass    
#      redirect to modulepage   
      taskId=None
   else:
      taskIdCnt= cnt+ 1
      taskId=courseMetaData['Modules'][cnt]['TaskId'][taskIdCnt]
   app.logger.debug(f'******  {taskId} ') 
   return taskId
 
# bug always taking second qn -fixed
# retrieves the current qn based on number of completed qn, see how it is tracked
#
def getQn(cid,mid):

   app.logger.debug(f'******inside getQn v2.0 {cid} {mid} {mid[3:4]} ')
   userId = session['userid']
   courseMetaData=getCourseDetails(cid)
   cnt=int(mid[3:4])-1
   app.logger.debug(f'******inside getQn v2.0 {courseMetaData}   ')
   totalExercises=int(courseMetaData['Modules'][cnt]['totalExercises'])
#['totalExercises']         
   completedExercises=0
#int(courseMetaData['Modules'][cnt]['completedExercises'])
#['completedExercises']       
   app.logger.debug(f'******{cnt} {totalExercises} {completedExercises} ')
   moduleId=courseMetaData['Modules'][cnt]
#   insertCourseHistory(userId,cid,mid)

   if totalExercises== completedExercises and cnt <=courseMetaData['totModules']:
      cnt=cnt+1
      taskIdCnt=0

   else:
      taskIdCnt= completedExercises + 1

   taskId=courseMetaData['Modules'][cnt]['TaskId'][taskIdCnt-1]
   app.logger.debug(f'******  {taskId} ') 
   return taskId


#B2
#invoked from the index page
#
@app.route('/course/<cid>/modules/<mid>', methods = ['POST', 'GET'])
def getModulePage(cid,mid):

    app.logger.debug(f'****** getModulePage v3.0 -{cid} {mid}')
    
    # add to session
    if 'userid' in session:
      username = session['userid']
    else:
      return redirect(url_for('courseLogin'))
    error = None

    status,out=fetchCourseLH(username,cid)
 
    app.logger.info('*******  courseDetails :' +   str(len(out)) )

#    cidHead=cid+'_head'
    courseLHDetails=json.loads(out)

    app.logger.info(f'*******  Course has not yet started {courseLHDetails} ')

    status= checkModulePendingInHistory(cid,mid,courseLHDetails)

#review1
    qn=getQn(cid,mid)

# module is still pending
    if status == True:
       updateModuleHistoryStatus(username,cid,mid,qn,"progress")     
    app.logger.info('*******  courseDetails:' +   str(courseLHDetails) )
    data = {"TaskId": qn}

    try:
       app.logger.info('******* response- TaskDetails: gradingType' + config.gradingTypeURL) 
       response=requests.post(config.gradingTypeURL,json= data ) 
 
       json_data = json.loads(response.json())
       app.logger.info("data" + str(json_data))

  #     for key,value in json_data.items(): 
  #      app.logger.info('******* response- TaskDetails: qn'+ key + value  )
       app.logger.info('******* response- TaskDetails: qn'+ json_data['gradeType'])
       gradeType = json_data['gradeType']

    except  requests.exceptions.RequestException as error:
        app.logger.error("****** Exception:", error) 

    ''' remove11   questionRepoURL= config.questionRepoURL
    data = {"TaskId": qn}

    app.logger.info('******* response- TaskDetails: qn'+ qn   )
    app.logger.info('******* response- TaskDetails:'+ questionRepoURL   )

    app.logger.info('******* response- TaskDetails:'+   json.dumps(data) )'''

#rw001 why is this
#already there is a javascript in index page
#why gradingType

    if mid=='M005':
       return redirect(url_for('getQuizModule',cid=cid,quizId=quizId))
    else:
       return redirect(url_for('getModulePageParticularQn',cid=cid,mid=mid,taskId=qn,gradeType=gradeType))

def getLH(userId,courseId):

   learningHistoryURL=  config.learningHistoryURL
   data ={"userId":userId,"courseId":courseId,"action":"RetrieveCourseLH"}

   try:
       response=requests.post(learningHistoryURL,json= data )
       jsonResponse = json.loads(response.json())
       app.logger.info("******Platform service successful" + str(jsonResponse ))
       return True, jsonResponse  
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service failed", error)
        return False,None

#update TaskStatus frm pending to progress
def upsertTaskHistory(cid,mid,taskId,status):
   userId= session['userid']
   learningHistoryURL=  config.learningHistoryURL
   data ={"userId":userId,"courseId":cid,"moduleId":mid,"taskId":taskId,"status":status,"action":"Insert"}

   try:
       response=requests.post(learningHistoryURL,json= data )
       jsonResponse = response.json()
       app.logger.info(f"******Platform service: upsertTaskHistory T -{taskId} S-{status}successful")
       return True, jsonResponse  
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service: upsertTaskHistory failed", error)
        return False,None

def  checkLHUpdation(taskStatus):
     return True

@app.route('/course/<cid>/module/<mid>/<taskId>/next', methods = ['POST','GET'])
def getNextTask(cid,mid,taskId):
    nextTaskId=getNxtQn(cid,mid,taskId)
    if  nextTaskId !=None:
        getModulePageParticularQn(cid,mid,nextTaskId)
    else:
        return render_template("courseIndex",cid=cid) 

#B3
#
#Called From : getModulePage
# need course details like language and next task details
@app.route('/course/<cid>/module/<mid>/<taskId>', methods = ['POST','GET'])
def getModulePageParticularQn(cid,mid,taskId):

    tempSplit=taskId.split("_")
    app.logger.debug(f'getModulePageParticularQn: *************** {tempSplit} {len(tempSplit)}')      

    taskStatus="progress"

    app.logger.debug(f'*************** LH Updation of Task')    

  
    status=checkLHUpdation(taskStatus)


    if status== True:
       status="progress" 

    upsertTaskHistory(cid,mid,taskId,status)

    app.logger.info('***************metadata- CourseId- {0} ModuleId- {1} taskId-{2}'.format(cid,mid,taskId))
    if len(tempSplit) ==3 and tempSplit[2]=="next":
       taskId=   tempSplit[0] + "_"+tempSplit[1]
       data = {"courseId":cid,"moduleId":mid, "TaskId": taskId,"TaskAction": "getNxtTask"}
    else:
       data = {"TaskId": taskId,"TaskAction": "getTask"}
 
    langDict = {"A01": "python","A04": "react","A05":"web"}
#next tasks
    taskIdDict={"A01_H":["python"],"A01_1":[ "python","A01_2","619968946"],"A05_1":[ "HTML","A05_2","619968946"],"A01_2":[ "python","A01_3"],"A01_3":[ "python","A01_4"]} 

    language= langDict[cid]

    nextTaskId="A01_1"
    app.logger.info('++++++++++++++++++++++++++ Next Task {0} // {1}++++++++++++++++++++++++++++++'.format(taskId,nextTaskId))
    app.logger.info('******* request- TaskDetails URL:-{0} data- {1}'.format(config.questionRepoURL, json.dumps(data)))

    status,LHistory=getLH(session['userid'],cid)
    modules=LHistory["Modules"]
    moduleLHDict=""
    out={}

    for module in modules:
        id=module['Mid'] 
        out[str(id)]="module"
        app.logger.info(f'******* Module details{out} ')
    moduleLHDictStr=json.dumps(out)
    modDetails= getmodDetails(cid,mid) 

    app.logger.info(f'******* Module details{moduleLHDictStr} ')

    try:
       response=requests.post(config.questionRepoURL,json= data) 
       jsonResponse = response.json()
       json_data = json.loads(response.json())

       app.logger.info('******* jsonResponse :{0}'.format(jsonResponse))      
       app.logger.info('******* jsonResponse :{0}'.format(type(json_data))) 
       app.logger.debug('******* Question Retrieve  *******' + json_data["status"])

       if json_data["status"]== "Fail":
          app.logger.info("******Moduel  retrieval request failed")
          page=config.page500.format(config.error)  
          return render_template(page,msg="Administrator-DB001"), 500  

       elif   json_data["status"]== "Module_Finished":
              status="Module_Finished"  
              app.logger.debug('******* Module Finished *******')
              return redirect(url_for('coursePage',cid=cid,status=status))
       elif   json_data["status"]== "Course_Finished":
              status="Course_Finished"  
              app.logger.debug('******* Module Finished *******')
              return redirect(url_for('coursePage',cid=cid,status=status))

       taskType=json_data["taskType"]
       taskId=json_data["TaskId"]
 
       app.logger.debug(f'*******LHistory ******* {LHistory}') 
       app.logger.info('******* request Type :{0}'.format(taskType) )

#      TaskType validation

       cmPath=config.courseModuleBasePath.format(config.courseBase,cid,mid)
       app.logger.info('*******  courseModulePath:{0}'.format(cmPath) )

       if taskType=='Video':      
          videoId=json_data["linkedQuestion"]
          app.logger.debug('******* request TypeVideo :{0}'.format(type) )
          # move to config page 
          page=config.videoPage.format(config.common)
          currentTime="120"
          app.logger.debug('******* videoID:{0} {1}'.format(taskId , videoId) ) 
          app.logger.debug('******* page:{0} {1}'.format(page, session['userid']) ) 
          return render_template(page,courseId=cid,mid=mid,taskId=taskId,taskType="Video",videoId=videoId,currentTime=currentTime,mdDetails=modDetails,status=LHistory,json=response.json(),courseModulePath=cmPath,userId=session['userid'],LH=LHistory,fileTreeNavigation="fileNavigation")

       elif taskType.strip()=='pdf_tut':  

          app.logger.debug('******* request TypeVideo :{0}'.format(type) )
          # move to config page 
          page=config.pdfPage.format(config.common)
          pdfId=json_data["field1"]
          app.logger.debug('******* videoID:{0} {1}'.format(taskId , pdfId) ) 
          app.logger.debug('******* page:{0} {1}'.format(page, session['userid']) ) 
          return render_template(page,mdDetails=modDetails,status=LHistory,json=response.json(),courseModulePath=cmPath,taskType='pdf_tut',taskId=taskId,pdfId=pdfId,userId=session['userid'],LH=LHistory,fileTreeNavigation="fileNavigation",courseId=cid,mid=mid)

       elif taskType.strip()=='Assgn':  

          app.logger.debug('******* request Type :{0}'.format(type) )
          # move to config page 
          page=config.assgPage.format(config.common)
          app.logger.debug('******* videoID:{0} '.format(taskId ) ) 
          app.logger.debug('******* page:{0} {1}'.format(page, session['userid']) ) 
          return render_template(page,pgStatus=False,mdDetails=modDetails,status=LHistory,json=response.json(),courseModulePath=cmPath,taskType="assgn",taskId=taskId,userId=session['userid'],LH=LHistory,courseId=cid,mid=mid)

       elif taskType.strip()=='Quiz':  

         app.logger.info('******* Quiz: Single Qn :{0}'.format(type) )    
         # taskSolutionTokens=json_data["solution"].split("//")
         # create json date from Task Table
         json_data =json.dumps({"TaskList":[ {"qn":"1", "QnDesc":'What is the output when running the below code?<br/><br/>games =\
         ["softball", "vollyball", "golf"] print("|".join(games))?',"type":"mulitple","ans":"A",       \
          "options":['["softball","vollyball", "golf"]','softball|vollyball|golf','softball|vollyball|golf|','None of these']}]})                            \
         
         page=config.quizPage.format(config.common)
         app.logger.info('******* page:{0}'.format(page) ) 
         return render_template(page,mdDetails=modDetails,status=LHistory,json=json_data,count=1,courseModulePath=cmPath,LH=LHistory,taskType="Quiz",taskId=taskId,userId=session['userid'],courseId=cid,moduleId=mid)

       elif taskType=='Tutorial':

         page=config.tutpage	
         cmPath=config.courseModuleBasePath.format(config.courseBase,cid,mid) 
         app.logger.info('******* page:{0}'.format(page) ) 
         return render_template(page,mdDetails=modDetails,userId=session['userid'],cid=cid,status=LHistory,json=json_data,courseModulePath=cmPath,taskType="Tutorial",moduleId=mid)

#         return redirect(url_for('getTutPage',json="",cid=cid,mid=mid,taskId=taskId))

       elif taskType=='Game':

         page=config.gamePage
#         page=config.output
         solution="none"	
         cmPath=config.courseModuleBasePath.format(config.courseBase,cid,mid) 
         app.logger.info('******* page:{0}'.format(page) ) 
#         return render_template(page,mdDetails=modDetails,userId=session['userid'],cid=cid,status=LHistory,json=json_data,courseModulePath=cmPath,taskType="Tutorial",moduleId=mid)

         return render_template(page,code=solution,courseId=cid,mid=mid,mdDetails=modDetails,moduleLHDict=moduleLHDictStr,status=LHistory,json=json.dumps(json_data),courseModulePath=cmPath,\
                 taskId=taskId,nextTaskId=nextTaskId,language=language,userId=session['userid'],taskType="Task",LH=LHistory)



       elif taskType=='Task':
   
          app.logger.info('******* response- TaskDetails:'+ str(response.json()))
          app.logger.info('******* response- TaskDetails:'+ str(response))  

          if cid == 'A04':
             taskPage=config.webtaskPage.format(config.common)
          elif cid == 'A07':
              taskPage=config.terminaltaskPage.format(config.common)   
          else:
               taskPage=config.taskPage  
 
          app.logger.info('******* page:{0}'.format(taskPage) ) 
          app.logger.info('******* json:{0}'.format(json_data ) )
           
          if cid=="A04":
             fileNavigation= True
          else:
            fileNavigation= False  

          scratchpadContents=Utils.readScratchpad(cid)

          app.logger.info('******* scratchpadContents:{0}'.format(scratchpadContents ) )
          app.logger.info('******* Redirected to taks page userId:{0}'.format(session['userid'] ) )

          # fetchAny code if their from the database
          #userId
          # code
          # taskId 
          #lastupatedtime
          #lastupated req

          solution=getSolForTask(session['userid'],taskId,cid)
          if solution== None:
             solution="" 
   #       code='<!DOCTYPE html><html><head<title>Python inside</title></head>''<body><h1>Parse me!</h1><body></html>'
          return render_template(taskPage,code=solution,courseId=cid,mid=mid,mdDetails=modDetails,moduleLHDict=moduleLHDictStr,status=LHistory,json=json.dumps(json_data),courseModulePath=cmPath,fileTreeNavigation=fileNavigation,\
                 taskId=taskId,nextTaskId=nextTaskId,language=language,userId=session['userid'],taskType="Task",LH=LHistory,scratchpadContents=scratchpadContents)


       else:
          raise Exception("Invalid tasktype")
    except  requests.exceptions.RequestException as error:
        app.logger.info("******Moduel  retrieval request failed", error)
        page=config.page500.format(config.error)          
        return render_template(page), 500  



def getSolForTask(userId,taskId,cid):
    try:
       data = {"TaskAction": "getSolTask","taskId":taskId,"userId":userId} 
       response=requests.post(config.questionRepoURL,json= data )
       hostIp= "http://192.46.208.71"
       port= "5022"
       API_ENDPOINT = f"{hostIp}:{port}/ps/api/v2/platformServices/SubmissionService/"
       data={"api_dev_key":"API_KEY",
              "TaskAction":"getSolTask", 
              "userId":userId,
              "courseId":cid, 
               "taskId":taskId 
              }
       resp = requests.post(url = API_ENDPOINT, data=json.dumps(data), headers={'Content-Type': 'application/json'}) 
       
       jsonResponse = resp.json()
       app.logger.info("******Module details"+ str(jsonResponse ))
       
       obj=json.loads(resp.json())

       solution=obj['solution']
       return solution
    except  requests.exceptions.RequestException as error:
        app.logger.info("******getSolForTask request failed", error)
        page=config.page500.format(config.error)          
        return  None  



def getmodDetails(cid,mid):
    try:
       data = {"TaskAction": "getModuleDtls","courseId":cid,"moduleId":mid} 
       response=requests.post(config.questionRepoURL,json= data )
       
       jsonResponse = response.json()
       app.logger.info("******Module details"+ str(jsonResponse ))
       return response.json()
    except  requests.exceptions.RequestException as error:
        app.logger.info("******Moduel  retrieval request failed", error)
        page=config.page500.format(config.error)          
        return render_template(page), 500  


@app.route('/course/<cid>/module/<mid>/<taskId>', methods = ['POST','GET'])
def getTutPage(cid,mid,taskId):
    app.logger.info('******* page:{0}'.format(page) ) 
    page=config.tutpage

 #   return render_template(page), 500
 
    try:
 
       cmPath=config.courseModuleBasePath.format(config.courseBase,cid,mid) 
     
       app.logger.info('******* page:{0}'.format(page) ) 
  #     return render_template(page,mdDetails=modDetails,status=LHistory,courseModulePath=cmPath,taskType="Tutorial")

    except  requests.exceptions.RequestException as error:
       app.logger.info("******Moduel  retrieval request failed", error)
       return render_template(page), 500  


#http://192.46.208.71:9085/feedback/hk01/guest/hk01_2/pyTask/ 

@app.route('/course/MyCourses', methods = ['POST','GET'])
def getAllMyCourses():

    app.logger.info('***************My Courses v2.0' )
    error = None
    userDetails=   session['userid']
    courseList=session['myCourses']
    courseHistory=  {"pending":[{
	"courseId": "A01",
	"moduleId": "M001",
	"taskId": "A01_1",
	"desc": "Java Basics",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "Pending"  
                      }
                      ,{"courseId": "A02",
   	   "moduleId": "M001",
  	   "taskId": "A01_1",
	   "desc": "SQL Basics",
	   "date": "12/12/2021",
	   "time": "10",
	   "author": "10",
                       "status": "Pending"}
                      ,{"courseId": "A03",
   	   "moduleId": "M001",
  	   "taskId": "A01_1",
	   "desc": "Python Basics",
	   "date": "12/12/2021",
	   "time": "10",
	   "author": "10",
                       "status": "Pending"}],
                     "inprogress":[{
	"courseId": "A01",
	"moduleId": "M001",
	"taskId": "A01_1",
	"desc": "Java Basics",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "Pending"  
                      }],
                     "completed":[{
	"courseId": "A10",
	"moduleId": "M001",
	"taskId": "A01_1",
	"desc": "Introduction to Social Wings",
	"date": "12/12/2021",
	"time": "10",
	"author": "10",
                     "status": "completed"  
                      }]


                    }
    app.logger.info('***************My Courses v2.0' ) 
 
    return render_template(config.myCourses,profile=userDetails,courseList=courseHistory)

@app.route('/course/<cid>/<mid>/<taskId>/upload', methods = ['POST','GET'])
def fileUpload(cid,mid,taskId):
       status=True
       assgnSol = request.files['file']
       assgnSol.save("/root/Environment/Dev/scratchpad/guest/test.sol") 
       status,LHistory=getLH(session['userid'],cid)
       modDetails= getmodDetails(cid,mid) 
       data = {"TaskId": taskId,"TaskAction": "getTask"}
       response=requests.post(config.questionRepoURL,json= data) 
       jsonResponse = response.json()
       json_data = json.loads(response.json())
       app.logger.info('******* jsonResponse :{0}'.format(jsonResponse))      
       app.logger.info('******* jsonResponse :{0}'.format(type(json_data))) 
        
       if json_data["status"]== "Fail":
          status=False 
          app.logger.info("******Moduel  retrieval request failed")
          page=config.page500.format(config.error)  
          return render_template(page,msg="Administrator-DB001"), 500  

       taskType=json_data["taskType"]
       taskId=json_data["TaskId"]
       out=session['LH']
       courseDetails=json.loads(out) 
       app.logger.info('******* LH result :{0}'.format(courseDetails) )
       app.logger.info('******* request Type :{0}'.format(taskType) )

#      TaskType validation

       cmPath=config.courseModuleBasePath.format(config.courseBase,cid,mid)
       app.logger.info('*******  courseModulePath:{0}'.format(cmPath) )
       app.logger.debug('******* request Type :{0}'.format(type) )
       # move to config page 
       page=config.assgPage.format(config.common)
       app.logger.debug('******* videoID:{0} '.format(taskId ) ) 
       app.logger.debug('******* page:{0} {1}'.format(page, session['userid']) ) 
       return render_template(page,pgStatus = status,msg="Successfully uploaded",status=LHistory,json=response.json(),courseModulePath=cmPath,taskType="assgn",taskId=taskId,userId=session['userid'],LH=courseDetails,courseId=cid,mid=mid)


@app.route('/course/MyTests', methods = ['POST','GET'])
def getAllMyTests():

    app.logger.info('***************My Courses v2.0' )
    error = None
    userDetails=   session['userid']
    courseList=session['myCourses']
#    courseList=session['recentCourses']
    LH=session['LH']
#    badge=session['Badge'] 
#    hours=session['LHHours']
#    Score=session['Score']  
#    track=session['LearningTrack'] 
 
    return render_template(config.myTests,profile=userDetails,courseList=courseList)

@app.route('/course/blog', methods = ['POST','GET'])
def getBlog():
    posts=[{ "author": "guest","date_posted": "20/12/2021","title":"welecome" ,"content" :"Welcome to introduciton to python" },
           { "author": "guest2","date_posted": "20/12/2021","title":"Session" ,"content" :"introduciton to python" } 
         ]
    app.logger.info('***************My Courses v2.0' )
    error = None
    userDetails=   session['userid']
    courseList=session['myCourses']
#    courseList=session['recentCourses']
    LH=session['LH']
#    badge=session['Badge'] 
  #  hours=session['LHHours']
  #  Score=session['Score']  
  #  track=session['LearningTrack'] 
 
    return render_template(config.blog,profile=userDetails,posts=posts)
@app.route('/course/MyLearningPath', methods = ['POST','GET'])
def getMyLearningPath():

    app.logger.info('***************My Courses v2.0' )
    error = None
    userDetails=   session['userid']
    courseList=session['myCourses']
#   courseList=session['recentCourses']
    LH=session['LH']
    badge=session['Badge'] 
    hours=session['LHHours']
    Score=session['Score']  
    track=session['LearningTrack'] 
 
    return render_template(config.myLearningPath,profile=userDetails,courseList=courseList)

@app.route('/course/tryTest/<taskId>' , methods = ['POST','GET'])
def takeTest(taskId):

   data = {"TaskId": "A01_2"}
  
   #Authentication
   # authenticationError 
   hackId="dummy"
   session['LH']='{}'
   session['userid']='guest'

   return redirect('/course/hackathon/dummy/'+taskId)

@app.route('/course/hackathon/<hackId>' , methods = ['POST','GET'])
def hackathonStart(hackId):
   try:    
       return render_template(config.hackathonStartPage,hackId=hackId)
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Hackathon details retrieval request failed", error)
        page=config.page500          
        return render_template(page), 500  

@app.route('/course/profile/<profileId>' , methods = ['POST','GET'])
def profile(profileId):
   try:    
    return render_template(config.profilePage,profileId=profileId)
 
   except  requests.exceptions.RequestException as error:
        app.logger.info("****** retrieval request failed", error)
        page=config.page500          
        return render_template(page), 500  

@app.route('/course/hackathon/start/<hackId>' , methods = ['POST','GET'])
def hackathon(hackId):
   data = {"TaskId": "A01_2"}
  
   #Authentication

   try:

       error = None
       userName=session['userid']
       testdetails='''[{"testId": "hk001",
		"testdetails": [{
				"questionId": "1",
				"questionDesc": "Python Movies Analytics",
				"type": "coding",
				"time": "120"
			}, {
				"questionId": "2",
				"questionDesc": "React Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "3",
				"questionDesc": "MCQ Technical",
				"type": "MCQ",
				"time": "120"
			}
		]
	}, {
		"testId": "hk02",
		"testdetails": [{
				"questionId": "1",
				"questionDesc": "Python Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "2",
				"questionDesc": "React Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "3",
				"questionDesc": "MCQ Technical",
				"type": "MCQ",
				"time": "120"
			}
		]
	},
	{
		"testId": "hk03",
		"testdetails": [{
				"questionId": "1",
				"questionDesc": "Python Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "2",
				"questionDesc": "React Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "3",
				"questionDesc": "MCQ Technical",
				"type": "MCQ",
				"time": "120"
			}
		]
	},
	{
		"testId": "hk04",
		"testdetails": [{
				"questionId": "1",
				"questionDesc": "Python Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "2",
				"questionDesc": "React Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "3",
				"questionDesc": "MCQ Technical",
				"type": "MCQ",
				"time": "120"
			}
		]
	},
	{
		"testId": "hk05 ",
		"testdetails": [{
				"questionId ": "1",
				"questionDesc": "Python Customer Order ",
				"type ": "coding ",
				"time": "120"
			},
			{
				"questionId": "2",
				"questionDesc": "React Customer Order",
				"type": "coding",
				"time": "120"
			},
			{
				"questionId": "3",
				"questionDesc": "MCQ Technical",
				"type": "MCQ",
				"time": "120"}]}]'''
       qnDetails=None
       testdetailsJSONObj=json.loads(testdetails)
       app.logger.info("******Hackathon details:" + str(testdetailsJSONObj))

       #qnDetails={"qnDetails":[{"id":"hk01_1","name":"Python Movie Management","link":"/course/hackathon/hk01/hk01_1"},\
       #           {"id":"hk01_2","name":"React students List component.","link":"/course/hackathon/hk01/hk01_2"},\
       #           {"id":"hk01_3","name":"MCQ- Technical","link":"/course/hackathon/hk01/hk01_2"},\
       #          ] } 
       for obj in testdetailsJSONObj:
          app.logger.info("******Hackathon details:" + str(obj['testId'] ))

          if obj['testId']==hackId:
             qnDetails=obj['testdetails'] 
             app.logger.info("******Hackathon details:" + str(obj['testdetails'] ))
             break
       hackathonList=session['myCourses'] 

       return render_template(config.hackathon,userName=userName,qnDetails=qnDetails)
 
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Hackathon details retrieval request failed", error)
        page=config.page500          
        return render_template(page), 500  

@app.route('/course/hackathon/<hackId>/<taskId>', methods = ['POST','GET'])
def getHackathonTaskId(hackId,taskId):
    app.logger.info('***************metadata- CourseId- {0} ModuleId- {1} taskId'.format(hackId,taskId))
    data = {"TaskId": taskId,"TaskAction": "getTask"}
 
    app.logger.info('******* request- TaskDetails URL:-{0} data- {1}'.format(config.questionRepoURL, json.dumps(data)))

    try:
 
       response=requests.post(config.questionRepoURL,json= data ) 
       jsonResponse = response.json()
       json_data = json.loads(response.json())
       app.logger.info('******* jsonResponse :{0}'.format(jsonResponse ) )      
       app.logger.info('******* jsonResponse :{0}'.format(type(json_data) ) ) 
 
       taskType=json_data["taskType"]
       taskId=json_data["TaskId"]
       out=session['LH']
       courseDetails=None 
       if taskId=="hk01_3":  
          code=config.react1
          language="react" 
       elif taskId=="hk02_1":
          code=config.python1  
          language="python"
       app.logger.info('******* LH result :{0}'.format(courseDetails) )
       app.logger.info('******* request Type :{0}'.format(taskType) )
       app.logger.info('******* response- TaskDetails:'+ str(response.json())  )
       app.logger.info('******* response- TaskDetails:'+ str(response)  )  
       fileNavigation= False  

       if taskType == 'webTask':               
            taskPage=config.assessmentTask  
            fileNavigation= True
       elif taskType == 'devOPSTask':
              taskPage=config.terminaltaskPage.format(config.common)   
       else:
               taskPage=config.assessmentTask  
 
       app.logger.info('******* page:{0}'.format(taskPage) ) 
       app.logger.info('******* json:{0}'.format(json_data ) )
       scratchpadContents= " "

       app.logger.info('******* Redirected to taks page userId:{0}'.format(session['userid'] ) )
       app.logger.info('******* code:{0}'.format( code ) )
       return render_template(taskPage,json=json.dumps(json_data),language=language,code=code,taskType=taskType,baseTestTask="baseTest.html",fileTreeNavigation=fileNavigation,taskId=taskId,userId=session['userid'],LH=courseDetails,courseId=hackId,mid="mid",scratchpadContents=scratchpadContents)

    except  requests.exceptions.RequestException as error:
        app.logger.info("******Moduel  retrieval request failed", error)
        page=config.page500          
        return render_template(page), 500  

 
#review3
# 
#
#quiz section
@app.route('/course/<cid>/quiz/<quizId>', methods = ['POST','GET'])
def getQuizModule(cid,quizId):

#quiz
#Test
    data={'quizId':quizId,'courseId':cid,'TaskAction':"getMEndMCQ"}
#
    app.logger.info('******* inside {0} quiz page:{1}'.format(cid,quizId) ) 
    response=requests.post(config.quizRepoURL,json= data ) 
    jsonResponse = response.json()
    json_data = json.loads(response.json())
    courseDetails=""
    username=   session['userid']
    status,out=fetchCourseLH(username,cid)
    app.logger.info('*******  courseDetails :' +   str(len(out)) )
    courseDetails=json.loads(out)

    status= checkModulePendingInHistory(cid,quizId,courseDetails)
    if status == True:
       updateModuleHistoryStatus(username,cid,quizId,qn,"progress")


    app.logger.info('******* quiz details:{0}'.format(json_data) ) 
    quizList= json_data["TaskList"]
    try:

       page=config.mcqAssessmentPage.format(config.common,cid)    
       home="/course/{0}".format(cid)
       app.logger.info('******* home page:{0}'.format(home) )
       app.logger.info('******* targetpage:{0}'.format(page) )
 
       return render_template(page,json=response.json(),count=4, quizId=quizId,userId=session['userid'],courseId=cid,homeTestPage=home)
    except  requests.exceptions.RequestException as error:
       app.logger.info("******Moduel  retrieval request failed", error)
       return render_template(page), 500  

#quiz section
 
@app.route('/course/hackathon/<testId>/quiz/<quizId>', methods = ['POST','GET'])
def getHackathonQuizId(testId,quizId):

    data={'quizId':quizId,'testId':testId,'TaskAction':"getTest"}

    app.logger.info('******* inside {0} quiz page:{1}'.format("none",quizId) ) 
    response=requests.post(config.quizRepoURL,json= data ) 
 
    json_data = json.loads(response.json())
    json_data=eval(json.loads(response.json()))
    courseDetails=""


    quizList= json_data["quizR"]
    app.logger.debug('******* quiz list details:{0}'.format(quizList) ) 
    try:

       page=config.mcqAssessmentPage.format(config.common)
       home="/course/hackathon/{0}".format(testId)    
       app.logger.info('******* page:{0}'.format(page) ) 
       app.logger.info('******* page:{0}'.format(home) ) 

       return render_template(page,questionList=json.dumps(json_data),count=4, quizId=quizId,userId=session['userid'],testId=testId,homeTestPage=home)
    except  requests.exceptions.RequestException as error:
       app.logger.info("******Moduel  retrieval request failed", error)
       return render_template(page), 500  

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
@app.route('/test')
def test():
    error = None
    return render_template('cs002.html')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template(config.page404), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.info(e)
    return render_template(config.page500), 500

#####has to be removed
def fetchLHAll(userId):
    courseId=None
    moduleId=None
    return fetchLH(userId,courseId,moduleId)

def fetchLH(userId,courseId,moduleId):
   learningHistoryURL=config.learningHistoryURL

   data ={'action':'getStudentLH','userId':userId}
   try:

       response=requests.post(learningHistoryURL,json= data )
       jsonResponse = json.loads(response.json())

       app.logger.info("******Platform service successful- learning history" + str(jsonResponse ))

       return True, jsonResponse  

   except  requests.exceptions.RequestException as error:

        app.logger.info("******Platform service failed", error)
        return False,None


def fetchCourseLH(userId,courseId):

   learningHistoryURL=config.learningHistoryURL
   data = {"userId":userId,"courseId":courseId,"action": "RetrieveCourseLH"}

   try:

       response=requests.post(learningHistoryURL,json= data )
       jsonResponse = response.json()
       app.logger.info("******Platform service successful")
       return True, jsonResponse  

   except  requests.exceptions.RequestException as error:

        app.logger.info("******Platform service failed", error)
        return False,None
 
 
def checkServices(serviceName):
   healthCheckURL=  config.healthCheckURL  
   data = {"userId": session['userid'], "service": "platform servcies"} 

   try:
       response=requests.post(healthCheckURL,json= data )
       app.logger.info("******Platform service successful" + str(response.status_code))
       if response.status_code == 200:
         return True
       else:
         return False  
   except  requests.exceptions.RequestException as error:
        app.logger.info("******Platform service failed: " + healthCheckURL, error)
        return False
 
#####has to be removed

if __name__ == "__main__":
    print("enter the port")
 #   inport=input()
    port = int(os.environ.get("PORT",  9085))
    app.run(debug=False,host='0.0.0.0',port=9085)
