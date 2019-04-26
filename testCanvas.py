from canvasapi import Canvas as cc
from canvasapi.requester import Requester
from canvasapi.upload import Uploader

# Canvas API URL
API_URL = "https://mst.instructure.com"
# Canvas API key
f=open('./_canvasInfo.txt','r')
lines=f.readlines()


API_KEY = lines[1][:-1]
COURSE=dict()
for x in xrange(3,len(lines)-1,2):
    COURSE[lines[x][:-1]]=lines[x+1][:-1]
# Initialize a new Canvas object
f.close()
class canvObj:
    def __init__(self,apiUrl,apiKey,course):
        self.canvas = cc(apiUrl, apiKey)
        self.STUDENT_DIC=dict()
        self.course=course


    def findAssignmentID(self,c,aNum):
        if c in self.course:
            cCourse = self.canvas.get_course(self.course[c])
            users=cCourse.get_users()
            for user in users:
                self.STUDENT_DIC[user.sis_user_id]=user.id
            return cCourse.get_assignments()[aNum].id
        else:
            return None

    def findStudentID(self,ssid):
        if ssid in self.STUDENT_DIC:
            return self.STUDENT_DIC[ssid]
        else:
            return None
            
    def findAllStudent(self,c):
        if c in self.course:
            cCourse = self.canvas.get_course(self.course[c])
            users=cCourse.get_users()
            return users
        else:
            return None
            
    def getCourse(self,c):
        if c in self.course:
            cCourse = self.canvas.get_course(self.course[c])
            return cCourse
        else:
            return None
            
    def getAssignments(self,c,aNum):
        if c in self.course:
            cCourse = self.canvas.get_course(self.course[c])
            users=cCourse.get_users()
            for user in users:
                self.STUDENT_DIC[user.sis_user_id]=user.id
            return cCourse.get_assignments()[aNum]
        else:
            return None
    
    def getSubmission(self,sec,aNum,stuid):
        ass=self.getAssignments(sec,aNum)
        if ass:
            return ass.get_submission(stuid)
        
            
    def editGrad(self,sec,aNum,stuid,grad):
        sub=self.getSubmission(sec,aNum,stuid)
        if sub:
            sub.edit(submission={'posted_grade':str(grad)})
            return True
        else:
            return False
    
    def upFile(self,sec,aNum,stuid,path):
        sub=self.getSubmission(sec,aNum,stuid)
        if sub:
            sub.upload_comment(path)
            return True
        else:
            return False









