import  json 
import logging 
import pymysql 
import os 
from subprocess import Popen, PIPE, STDOUT
from flask import Flask

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
 

def readScratchpad(courseId):
    courseList=["A05"]
    if courseId not in courseList:
       return ""
    sol_outfile=None
    try:
        app.logger.info("****** Reading Scratchpad"	)
        fileName=f"/root/Environment/Dev/CoursePortal/templates/htmlScratchpad/guest/{courseId}/solution.html"

        with open(fileName, 'r') as sol_outfile:
          contents=sol_outfile.read()

    except IOError.Error as error:
        app.logger.info("******Writing file", error)
        return None;
    finally:
        if (sol_outfile):
            sol_outfile.close()
            app.logger.info("File closed****")

    return str(contents);


def writeContents(file,data):
    try:
        file4 = open(file, 'w')
        file4.writelines(data)
    except IOError.Error as error:
        app.logger.info("******Writing file", error)
        return False;
    finally:
        if (file4):
            file4.close()
            app.logger.info("File closed****")

    return True;

   #move to utils
def createStringTemplate(self,shellCommandTemplate,arr):
   app.logger.info("************ Grading- replacing the template" + str(arr) +str( len(arr)) )

   cnt=0 
   for x in arr:

      repStr="#"+str(cnt+1) + "#"
      shellCommandTemplate=shellCommandTemplate.replace(repStr, arr[cnt])
      cnt=cnt+1 
   return shellCommandTemplate

   #grading module
   #read the ouput completed,error from the scratchpad directory
   #need to write to thedatabase
def readFile(self,stdId,inFile):
   basedir="/root/scratchpad"
   delim="/"
   target=basedir +delim+stdId  
   app.logger.info("grading: reading execution output" + target )   
   file3 = open(target+delim+inFile, 'r')
   Lines = file3.read()
#      for line in Lines:
#         app.logger.info("************ " + line)
   return Lines

def writeToFile(self,stdId,out,fileName):
       basedir="/root/scratchpad"
       delim="/"
       target=basedir +delim+stdId  +delim+fileName

       file4 = open(target, 'w')
       file4.writelines(out)
       file4.close()

def executeCommand(command):

   p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
   stderr=STDOUT, close_fds=True)
   output = p.stdout.read()
   return output