'''


api.add_resource(QnoRepoServices, "/platformServices/qnRepo/")
api.add_resource(GradingServices, "/platformServices/grading/") 
api.add_resource(HealthCheckServices, "/platformServices/ServiceCheck/")  
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my precious'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = False  # change to true to enable Debug toolbar


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False

 
    STATIC_JS='CorePlatform/web/static'
    STATIC_TEMPLATE='CorePlatform/web/templates'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False

SECRET_KEY = 'Replace '

TITLE = ''
#hostIP="http://192.46.208.71"
hostIP="https://socialblocks.in"

port="5022"
#PlatformserviceBaseUrl=hostIP+":"+ port
PlatformserviceBaseUrl=hostIP+"/ps"

gradingURL=PlatformserviceBaseUrl+"/api/v1/platformServices/grading/"
questionRepoURL=PlatformserviceBaseUrl+'/api/v1/platformServices/qnRepo/'
feedbackURL= PlatformserviceBaseUrl+'/api/v1/platformServices/feedback/'
quizRepoURL=PlatformserviceBaseUrl+"/api/v1/platformServices/quizRepo/"
healthCheckURL=PlatformserviceBaseUrl+"/api/v1/platformServices/ServiceCheck/" 
learningHistoryURL=PlatformserviceBaseUrl+"/api/v1/platformServices/learningHistory/"
gradingTypeURL=PlatformserviceBaseUrl+"/api/v1/platformServices/gradingType/"
SubmissionServiceURL=PlatformserviceBaseUrl+"/api/v2/platformServices/SubmissionService/"
#
base='/coursePortal'
baseMarketing='/marketing'
baseSW='/sw'
marketingPage='{0}/index.html'.format(baseMarketing)
swPage='{0}/index.html'.format(baseSW)
joinus='{0}/joinus.html'.format(baseMarketing)
sw_contact='{0}/contact.html'.format(baseMarketing)
sw_about='{0}/about.html'.format(baseMarketing)
loginPage='{0}/login.html'.format(base)
 
rolesPage={"admin":"A","student":"S","teacher":"T","guest":"G"}


common="{0}/courseHome/common".format(base)
homeMain="{0}/courseHome".format(base)
courseBase="{0}/courseHome/courses".format(base)
gameIndex="{0}/courseHome/courses/B02/Selectgame.html".format(base)
gameHolder="{0}/{1}/game.html" 
expectedOutput=f"{courseBase}/A05/gameTask/flappyExpected.html"
output=f"{courseBase}/A05/gameTask/flappyOutput.html" 
error="{0}/errors".format(base)
 
home="{0}/dashboard/{1}dashboard.html" 
myCourses='{0}/myCourses.html'.format(common)
myTests='{0}/myHackathon.html'.format(common)
myLearningPath='{0}/myLearningPath.html'.format(common)
blog='{0}/blog.html'.format(common)

hackathon='{0}/hackathon.html'.format(common)
hackathonStartPage='{0}/hackathonStartpage.html'.format(common)


courseIndex="{0}/{1}/index.html"
courseModuleBasePath="{0}/{1}/modules/{2}_Sect.html"

videoPage="{0}/video.html"
quizPage="{0}/quiz.html"   

taskPage="{0}/task.html".format(common) 
gamePage="{0}/gametask.html".format(common) 

pdfPage="{0}/pdfviewer.html".format(common) 
assgPage="{0}/assgTask.html".format(common) 
webtaskPage="{0}/webtask.html".format(common)  
terminaltaskPage="{0}/terminaltask.html"
page500="{0}/500.html".format(error) 
page404="{0}/404.html".format(error) 
mcqAssessmentPage='{0}/mcqAssessment.html'
tutpage='{0}/tutorial.html'.format(common)
assessmentTask='{0}/assessmentTask.html'.format(common)
profilePage='{0}/profile.html'.format(common)
testHomePage='{0}/{1}/index.html'     
courseHomePage="{0}/{1}/index.html" 

react1='''
import React, { Component } from 'react';
import  { useState } from "react";
  
function App() {
  const [theme, setTheme] = useState("light");

  const toggleTheme = () => {
    const nextTheme = theme === "light" ? "dark" : "light";
    setTheme(nextTheme);
  };

  return <button onClick={toggleTheme}>
      Current theme: {theme}
    </button>;
}

export default App;
'''
python1='''
class Movie:
   def __init__(self, movieId, movieName,leadactor, views, rating, category):
        self.movieId=movieId
        self.movieName =movieName
        self.leadactor =leadactor
        self.views  =views
        self.rating=rating
        self.category=category

#        [movieObj0,movieObj1]
class Solution:
   def countMovieViewsIncategory (self,movieListObj):
       movieDict={ }
       for  movieTmpObj in movieListObj:
            if movieTmpObj.category in movieDict.keys():
               movieDict[movieTmpObj.category]=movieDict[movieTmpObj.category] +movieTmpObj.views
            else:
               movieDict[movieTmpObj.category]=movieTmpObj.views
  
       return movieDict



   def findBestLeadActorInCategory (self,movieListObj,category):
       tempList=[]
       for  movieTmpObj in movieList:
            if movieTmpObj.category == category:
               tempList.append(movieTmpObj)

       for  movieTmpObj in tempList:       
           print("temporary movie list",movieTmpObj.movieId,",",movieTmpObj.movieName,",",movieTmpObj.rating)

       movieListObj.sort(key=lambda x: x.rating, reverse=True)
       return movieListObj[0]
 
     


#main function         
if  __name__=='__main__':

      movieList=[]
      count= int(input())
      
      for i in range(count): 

          movieId=int(input()) 
          movieName= input()
          leadactor= input()
          views= int(input())
          rating= int(input())
          category=input()
          movieObj= Movie(movieId,movieName,leadactor,views,rating,category)
          movieList.append(movieObj)
          

      for  movieTmpObj in movieList:
         print("MovieObj",movieTmpObj.movieName)

      cat= input()
      solution=Solution()
      obj=solution.findBestLeadActorInCategory(movieList,cat)
      print(obj.leadactor)

'''


 
