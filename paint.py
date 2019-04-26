from Tkinter import *
from tkColorChooser import askcolor
import tkFont
import math
import Tkconstants, tkFileDialog
import sys
import os
import os.path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor,ImageFont
from testCanvas import *
import webbrowser
import textwrap


#https://goo.gl/forms/874j9w3cQuu3jvGf2

class Paint(object):
    HALF_LINE=45
    PAGE_LINE=90
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'red'
    CANVAS_TOKEN=sys.argv[6]
    DEFAULT_WIDTH= int(sys.argv[1])-80
    DEFAULT_HEIGHT = int(sys.argv[2])-110
    homeWidth=1920
    homeHeight=1080*20
    pageHeight=1080
    SOURCE_FILE_DIR = sys.argv[3]
    courseSec=sys.argv[4]
    assNum=sys.argv[5]
    attBase=sys.argv[7]
    moveDis=3000
    print courseSec
    print assNum
    lineStr="____________________________________________________________________________________"
    
    
    def __init__(self):
    
        self.hold=False
        self.commentCounter=0
        self.commentDic=dict()
        self.fontsize=20
        self.upID=1000
        self.totalPage=0
        self.root = Tk()
        self.root.title(self.courseSec+self.assNum)
        #self.df = tkFont.Font(family='Ubuntu Mono',size=16)
        #self.df=tkFont.Font(font="TkFixedFont")
        #self.df.configure(size=14)
        self.df = tkFont.Font(family='FreeMono', size=14)
        self.pdf = ImageFont.truetype('FreeMono.ttf', size=18)
        self.r1=18.0/14.0
        self.cf= tkFont.Font(family='FreeSerif',size=16,weight='bold',slant='italic')
        self.pcf=ImageFont.truetype('FreeSerifBoldItalic.ttf',size=22)
        self.r2=24.5/18.0
        
        
        #self.pdf = ImageFont.truetype('UbuntuMono-R.ttf', size=22)
        
        #print(tkFont.families())
        self.codeTxt=[]
        self.nodeHopVector=[]
        self.drawDic=dict()
        self.lineDic=dict()
        self.studentList=sorted([fn for fn in os.listdir(self.SOURCE_FILE_DIR) if fn.endswith('_submit')])
        self.studentID=""
        self.studentIndex=-1
        self.score=[100]*len(self.studentList)
        #print COURSE
        self.ca=canvObj(API_URL,self.CANVAS_TOKEN,COURSE)
        self.url1=API_URL+"/courses/"+COURSE[self.courseSec]
        self.url1+="/gradebook/speed_grader?assignment_id="
        self.url1+=str(self.ca.findAssignmentID(self.courseSec,int(self.assNum)-1))
        self.url1+="#{\"student_id\":\""
        
        
        if self.studentList:
            self.studentIndex+=1
            self.studentID=self.studentList[self.studentIndex]
            self.studentDir=self.SOURCE_FILE_DIR+"/"+self.studentID+"/"
            self.filename = self.studentDir+"_"+self.studentID+".jpg"
        
        

        self.deltaW=self.homeWidth-self.DEFAULT_WIDTH
        self.deltaH=self.homeHeight-self.DEFAULT_HEIGHT

        self.image1 = Image.new("RGB", (self.homeWidth, self.homeHeight), 'white')
        self.draw1 = ImageDraw.Draw(self.image1)


        self.pre_button = Button(self.root, text='<---', command=self.prevStu)
        self.pre_button.grid(row=0, column=0)

        self.idFrame=Frame(self.root)
        self.idFrame.grid(row=0,column=1)

        self.enter_ssid=Entry(self.idFrame)
        self.enter_ssid.insert(END, self.studentID[0:-7])
        self.enter_ssid.pack(side=LEFT)
        self.next_button = Button(self.idFrame, text='find', command=self.selectStu)
        self.next_button.pack(side=RIGHT)
        
        self.next_button = Button(self.root, text='--->', command=self.nextStu)
        self.next_button.grid(row=0, column=2)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=3)

        self.deGFrame=Frame(self.root)
        self.deGFrame.grid(row=0,column=4)
        
        self.deGrad_button5 = Button(self.deGFrame,text='-5',command=self.deGrad5)
        self.deGrad_button5.pack(side=LEFT)
        self.deGrad_button = Button(self.deGFrame,text='-',command=self.deGrad)
        self.deGrad_button.pack(side=RIGHT)

        self.enter_score=Entry(self.root)
        self.enter_score.grid(row=0,column=5)
        
        self.upGFrame=Frame(self.root)
        self.upGFrame.grid(row=0,column=6)
        self.upGrad_button = Button(self.upGFrame,text='+',command=self.upGrad)
        self.upGrad_button.pack(side=LEFT)
        self.upGrad_button5 = Button(self.upGFrame,text='+5',command=self.upGrad5)
        self.upGrad_button5.pack(side=RIGHT)
        
        self.save_button = Button(self.root, text='save', command=self.save)
        self.save_button.grid(row=0, column=7)
        self.upload_button = Button(self.root, text='upload', command=self.upload)
        self.upload_button.grid(row=0, column=8)
        self.clear_all_button = Button(self.root,text='Clear', command=self.clearAll)
        self.clear_all_button.grid(row=0,column=9)
        helpmessage="Submit your ticket to: \n"
        urlmessage="https://goo.gl/forms/874j9w3cQuu3jvGf2"
        self.help_button = Button(self.root, text='Help', command=lambda: self.error_window(helpmessage,urlmessage))
        self.help_button.grid(row=0, column=10)
        
        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=11)

        self.frame=Frame(self.root,width=self.DEFAULT_WIDTH,height=self.DEFAULT_HEIGHT)
        self.frame.grid(row=1,columnspan=12)


        self.c = Canvas(self.frame, bg='white', width=min(self.DEFAULT_WIDTH,self.homeWidth), height=min(self.DEFAULT_HEIGHT,self.homeHeight),scrollregion=(0,0,self.homeWidth,self.homeHeight))
        #print self.homeHeight
        #print self.DEFAULT_HEIGHT
        self.hbar=Scrollbar(self.frame,orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM,fill=X)
        self.hbar.config(command=self.c.xview)
        self.vbar=Scrollbar(self.frame,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.c.yview)
        self.c.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.c.pack(side=LEFT,expand=True,fill=BOTH)
        
        self.c.create_text(900,20,text=self.courseSec+"  "+self.assNum,anchor='nw',font=self.df)
        
        self.setup()
        self.clearAll()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.attendSet=set()
        attF = open(self.attBase+"/Attendant Form"+str(self.assNum)+".csv")
        content = attF.readlines()
        ln=0
        #print "setting up"
        for line in content:
            lc=line.split(',')
            ln+=1
            if ln==1:
                continue
            else:
                self.attendSet.add(lc[1][1:-9])
            
        #print self.attendSet
        attF.close()
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<ButtonRelease-3>', self.comment)
        self.c.bind('<ButtonRelease-4>', self.upS)
        self.c.bind('<ButtonRelease-5>', self.downS)
    def symbol_up(self,var):
        if var>0:
            self.commentCounter+=1
        
        if var<0:
            self.commentCounter-=1
            self.commentCounter=max(self.commentCounter,0)
        
        self.curStr='C_'+str(self.commentCounter) 
        valueTup=()
        if self.curStr in self.commentDic:
            valueTup=self.commentDic[self.curStr]
            
        else:
            valueTup=(self.commentCounter,"")
            self.commentDic[self.curStr]=valueTup   
            
        self.symbol_enter.delete(0,END)
        self.symbol_enter.insert(0,self.curStr)
        self.symbol_txt.delete(1.0,END)
        self.symbol_txt.insert(END,valueTup[1])
    
    def comment(self,event):
        if self.hold:
            return
        self.hold=True
  
        self.comx=self.hbar.get()[0]*self.homeWidth+event.x
        self.comy=self.vbar.get()[0]*self.homeHeight+event.y  
        self.m = Toplevel(self.root)
        
        self.m.protocol("WM_DELETE_WINDOW", self.setHold)
        self.m.wm_title("Enter your comments")
        symbol_frame=Frame(self.m)
        
        symbol_up_button=Button(symbol_frame,text='/\\', command=lambda: self.symbol_up(1))
        symbol_up_button.grid(row=0,column=0)
        self.symbol_enter=Entry(symbol_frame)
        self.symbol_enter.grid(row=0,column=1)
        
       
        
        symbol_up_button=Button(symbol_frame,text='\\/', command=lambda: self.symbol_up(-1))
        symbol_up_button.grid(row=0,column=2)
        symbol_frame.grid(row=0,column=0)
        
        find_button=Button(self.m,text='Find comments', command=self.findSymbol)
        find_button.grid(row=0,column=1)
        
        self.symbol_size = Scale(self.m, from_=8, to=80, orient=HORIZONTAL)
        self.symbol_size.set(20)
        self.symbol_size.grid(row=0, column=2)
        
        
        self.symbol_txt=Text(self.m, height=15, width=80)
        self.symbol_txt.grid(row=1,rowspan=5,columnspan=3)
        
        symbol_confirm=Button(self.m,text='Confirm',command=self.on_closing)
        symbol_confirm.grid(row=6,column=1)
        self.symbol_up(0)
        
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = 700
        h = 400
        yoff= min(400,max(0,1000-h))
        self.m.geometry("%dx%d+%d+%d" % (w, h, x + self.DEFAULT_WIDTH/2,yoff))
        
        return
    
    def findSymbol(self):
        symbol=self.symbol_enter.get()
        if symbol in self.commentDic:
            valueTup=self.commentDic[symbol]
            self.commentCounter=valueTup[0]
            self.symbol_txt.delete(1.0,END)
            self.symbol_txt.insert(END,valueTup[1])
        else:
            valueTup=(self.commentCounter,self.symbol_txt.get(1.0,END))
            self.commentDic[symbol]=valueTup
    
    def on_closing(self):
        self.line+=1
        self.hold=False
        
        comSymbol=self.symbol_enter.get()
        self.commentDic[comSymbol]=(self.commentCounter,self.symbol_txt.get(1.0,END))
        self.fontsize=int(round(float(self.symbol_size.get())*self.r2))
        ccf= tkFont.Font(family='FreeSerif',size=int(self.symbol_size.get()),weight='bold',slant='italic')
        ppf=ImageFont.truetype('FreeSerifBoldItalic.ttf',size=self.fontsize)
        
        self.nodeHopVector.append(self.c.create_text(self.comx,self.comy ,text=self.symbol_enter.get(),fill='red',font=ccf,anchor='nw',tags=self.fontsize))
        self.draw1.text((self.comx,self.comy),text=self.symbol_enter.get(),anchor='nw',fill='red',font=ppf)
        
        sp=self.findPos(self.line)
        ttt=self.symbol_txt.get(1.0,END)
        margin =sp[0]+50
        offset = sp[1]
        
        w = textwrap.TextWrapper(width=80,break_long_words=True,replace_whitespace=False)
        body=w.wrap(ttt)
        self.draw1.text((margin, offset), text=self.symbol_enter.get()+" :", font=ppf, fill="red",anchor='nw')
        self.nodeHopVector.append(self.c.create_text(margin, offset, text=self.symbol_enter.get()+" :", font=ccf, fill="red",anchor='nw',tags=26))
        self.line+=1
        offset=self.findPos(self.line)[1]+ppf.getsize(" ")[1]
        for line in body:
            self.nodeHopVector.append(self.c.create_text(margin, offset, text=line, font=self.cf, fill="red",anchor='nw',tags=18))
            offset += self.pcf.getsize(line)[1]
            
        margin =sp[0]+50
        offset=self.findPos(self.line)[1]+ppf.getsize(" ")[1]
        #print body 
        #print len(body)
        for line in body:
            #print str(line)
            self.line+=2*str(line).count('\n')
            self.line+=3
            
            self.draw1.text((margin, offset), text=line, font=self.pcf, fill="red",anchor='nw')
            offset += self.pcf.getsize(line)[1]
        self.lineDic[self.studentIndex]=self.line+3
        self.commentCounter+=1
        self.m.destroy()
        
    def setHold(self):
        self.hold=False
        self.m.destroy()
    
    def upS(self,event):
        if self.vbar.get()[0]-0.01>=0.0:
            self.vbar.set(self.vbar.get()[0]-0.01,self.vbar.get()[1]-0.01)
            self.c.config(yscrollcommand=self.vbar.set)


    def downS(self,event):
        if self.vbar.get()[1]+0.01<=1.0:
            self.vbar.set(self.vbar.get()[0]+0.01,self.vbar.get()[1]+0.01)
            self.c.config(yscrollcommand=self.vbar.set)




    def prevStu(self):
        self.moveOut(self.moveDis)
        if self.studentIndex>0:
            self.studentIndex-=1
        else:
            self.studentIndex=len(self.studentList)-1
        self.clearAll()
        
    def selectStu(self):
        self.moveOut(self.moveDis)
        sel=self.enter_ssid.get()+'_submit'
        #print sel
        if sel in self.studentList:
            self.studentIndex=self.studentList.index(sel)
        else:
            self.error_window( "No such student can be found")
        self.clearAll()

    def nextStu(self):
        self.moveOut(self.moveDis)
        if self.studentIndex<len(self.studentList)-1:
            self.studentIndex+=1
        else:
            self.studentIndex=0
        self.clearAll()
    
   
    
    
    def moveOut(self,dis):
        if self.nodeHopVector:
            for vv in self.nodeHopVector:
                self.c.move(vv,-dis,0)
            self.drawDic[self.studentIndex]=self.nodeHopVector
            self.nodeHopVector=[]                

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def save(self):
        
        self.score[self.studentIndex]=self.enter_score.get()
        self.totalPage=math.ceil(self.totalPage)
        self.image1.crop((0,0,self.homeWidth,int(self.pageHeight*self.totalPage))).save(self.filename)
        
        
    def deGrad(self):
        curGrad=int(self.enter_score.get())
        self.enter_score.delete(0,END)
        self.enter_score.insert(0,str(max(0,curGrad-1)))    
        
    def upGrad(self):
        curGrad=int(self.enter_score.get())
        self.enter_score.delete(0,END)
        self.enter_score.insert(0,str(min(100,curGrad+1))) 
    def deGrad5(self):
        curGrad=int(self.enter_score.get())
        self.enter_score.delete(0,END)
        self.enter_score.insert(0,str(max(0,curGrad-5)))    
        
    def upGrad5(self):
        curGrad=int(self.enter_score.get())
        self.enter_score.delete(0,END)
        self.enter_score.insert(0,str(min(100,curGrad+5)))     
    def upload(self):
        self.save()
        
        if self.ca.findStudentID(self.studentID[0:-7]) and (self.studentID[0:-7] in self.attendSet):
            self.upID+=1
            file_from = self.filename
            
            stuid=self.ca.findStudentID(self.studentID[0:-7])
            aNum=int(self.assNum)-1
            self.ca.upFile(self.courseSec,aNum,stuid,file_from)
            self.ca.editGrad(self.courseSec,aNum,stuid,self.score[self.studentIndex])
        elif self.ca.findStudentID(self.studentID[0:-7]):
            other=self.SOURCE_FILE_DIR+"/_NoAttendance_"+self.studentID+".jpg"
            self.image1.crop((0,0,self.homeWidth,int(self.pageHeight*self.totalPage))).save(other)
            errorMessage="Student "+self.studentID[0:-7]+" is not attendant to the class.\n"
            errorMessage+="The graded file is not uploaded. However it has been saved at the Dir: "
            errorMessage+=other
            self.error_window(errorMessage)
        else:
            other=self.SOURCE_FILE_DIR+"/_wrongSection_"+self.studentID+".jpg"
            self.image1.crop((0,0,self.homeWidth,int(self.pageHeight*self.totalPage))).save(other)
            errorMessage="Student "+self.studentID[0:-7]+" is not belong to this section.\n"
            errorMessage+="The graded file is not uploaded. However it has been saved at the Dir: "
            errorMessage+=other
            self.error_window(errorMessage)
        
        self.nextStu()
        
        
        

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        curX=self.hbar.get()[0]*self.homeWidth+event.x
        curY=self.vbar.get()[0]*self.homeHeight+event.y
        if self.old_x and self.old_y:
            #print self.vbar.get()[0]
       
            self.nodeHopVector.append(self.c.create_line(self.old_x, self.old_y,curX ,curY ,width=self.line_width, fill=paint_color))
            cor=[self.old_x, self.old_y, curX, curY]
            #print cor
            self.draw1.line(cor, paint_color,width=self.line_width)
        self.old_x = curX
        self.old_y = curY

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clearAll(self):
        
        self.line=0
        self.totalPage=0
        #self.c.delete("all")
        for ct in self.codeTxt:
            self.c.delete(ct)
        self.codeTxt=[]
        for vv in self.nodeHopVector:
                self.c.delete(vv)
        self.nodeHopVector=[]
        self.enter_score.delete(0,END)
        self.image1 = Image.new("RGB", (self.homeWidth, self.homeHeight), 'white')
        self.draw1 = ImageDraw.Draw(self.image1)


        if self.studentList:
            self.studentID=self.studentList[self.studentIndex]
            self.studentDir=self.SOURCE_FILE_DIR+"/"+self.studentID+"/"
            self.filename = self.studentDir+"_"+self.studentID+".jpg"
        self.enter_ssid.delete(0,END)
        self.enter_ssid.insert(0,self.studentID[0:-7])   
        self.enter_score.insert(0,self.score[self.studentIndex])
         

        sourceFiles=os.listdir(self.studentDir)
        fname="_"+self.studentID+".jpg"
        
        
            
        for src in [fn for fn in sourceFiles if not fn.endswith('.jpg')]:
            with open(self.studentDir+src) as f:
                self.line=self.nextPage(self.line)
                content = f.readlines()
                for cc in content:
                    sp=self.findPos(self.line)
                    if self.line%self.HALF_LINE==0:
                        self.totalPage+=0.5
                        self.codeTxt.append(self.c.create_text(sp[0],sp[1]-30,text=src,anchor='nw',font=self.df))
                        self.codeTxt.append(self.c.create_text(sp[0],sp[1]-22,text=self.lineStr,anchor='nw',font=self.df))
                        self.codeTxt.append(self.c.create_text(sp[0],sp[1]+918,text=self.lineStr,anchor='nw',font=self.df))
                        self.codeTxt.append(self.c.create_text(sp[0]+400,sp[1]+950,text=self.studentID,anchor='nw',font=self.df))
                        self.codeTxt.append(self.c.create_line(sp[0]-2,sp[1]-1,sp[0]-2,sp[1]+937,fill='black'))
                        self.codeTxt.append(self.c.create_line(sp[0]+922,sp[1]-1,sp[0]+922,sp[1]+937,fill='black'))
                        self.draw1.text((sp[0],sp[1]-30),text=src,anchor='nw',fill='black',font=self.pdf)
                        self.draw1.text((sp[0],sp[1]-21),text=self.lineStr,anchor='nw',fill='black',font=self.pdf)
                        self.draw1.text((sp[0],sp[1]+918),text=self.lineStr,anchor='nw',fill='black',font=self.pdf)
                        self.draw1.text((sp[0]+400,sp[1]+950),text=self.studentID,anchor='nw',fill='black',font=self.pdf)
                        self.draw1.line([sp[0]-2,sp[1]-1,sp[0]-2,sp[1]+937],fill='black')
                        self.draw1.line([sp[0]+922,sp[1]-1,sp[0]+922,sp[1]+937],fill='black')
                    self.codeTxt.append(self.c.create_text(sp[0],sp[1],text=cc,anchor='nw',font=self.df))
                    #print cc
                    pilsp=(sp[0]+10,sp[1])
                    self.draw1.text(sp,text=cc,fill='black',font=self.pdf)
                    self.line+=1
        self.line=self.nextPage(self.line)
        self.totalPage+=0.5  
        
        
        if self.studentIndex in self.drawDic:
            self.nodeHopVector=self.drawDic[self.studentIndex]
            if self.studentIndex in self.lineDic:
                self.line=self.lineDic[self.studentIndex]
            for vv in self.nodeHopVector:
                self.c.move(vv,self.moveDis,0)
                if self.c.type(vv)=="line":
                    color = self.c.itemcget(vv, "fill")
                    wid=self.c.itemcget(vv, "width")
                    cor=self.c.coords(vv)
                    #print cor
                    self.draw1.line(cor,color,width=self.line_width)
                elif self.c.type(vv)=="text":
                    #ccf= tkFont.Font(family='FreeSerif',size=self.symbol_size.get(),weight='bold',slant='italic')
                    cor=self.c.coords(vv)
                    commm=self.c.itemcget(vv,"text")
                    csize=int(self.c.itemcget(vv,"tags"))

                    #print csize
                    ppf=ImageFont.truetype('FreeSerifBoldItalic.ttf',size=csize)
                    
                    self.draw1.text(cor,text=commm,anchor='nw',fill='red',font=ppf)
        
        
         
        
         
    def findPos(self,line):
        n=(line/self.HALF_LINE)%4
        if n==1 or n==2:
            n=1
        else:
            n=0
        hn=line/self.PAGE_LINE
        c=line%self.HALF_LINE
        return (20+n*960,c*20+hn*1080+60)
        
    def nextPage(self,line):
        n=(line/self.HALF_LINE)%2
        hn=line/self.PAGE_LINE
        c=line%self.HALF_LINE
        if c==0:
            return line
        if n==0:
            return hn*self.PAGE_LINE+self.HALF_LINE
        else:
            return (hn+1)*self.PAGE_LINE
    def openUrl(self,event):
        webbrowser.open_new(self.url_label['text'])    
    def error_window(self,message,url=""):
        self.t = Toplevel(self.root)
        self.t.wm_title("Error message")  
        
        message_label=Label(self.t,text=message+"\n",wraplength=1000,justify=CENTER)
        
        message_label.config(font=("Courier", 28))
        message_label.grid(row=0,column=0)
        
        self.url_label=Label(self.t,text=url,wraplength=1000,justify=CENTER, fg="blue", cursor="hand2")
        
        self.url_label.config(font=("Courier", 16))
        self.url_label.grid(row=1,column=0)
        self.url_label.bind("<Button-1>", self.openUrl)
        '''
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = 600
        h = 300
        yoff= min(300,max(0,1000-h))
        self.t.geometry("%dx%d+%d+%d" % (w, h, x + self.DEFAULT_WIDTH/2,yoff)) 
        '''

if __name__ == '__main__':
    Paint()
