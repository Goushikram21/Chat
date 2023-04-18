
from tkinter import *
import tkinter as tk

import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

import win32com.client as wincl

import time
import os









window = tk.Tk()

    #helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Auth")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

     

window.configure(background='#6a81a6')

    #window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
#lbl,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb8,lbl0=""







vname=StringVar()
vid=StringVar()
dat=StringVar()
name_r=StringVar()
id_r=StringVar()












def main_window():
   





    message = tk.Label(window, text="FACE BASED E_VOTING" ,bg="#9bdede"  ,fg="white"  ,width=50  ,height=3,font=('times', 30, 'italic bold')) 

    message.place(x=100, y=20)

    lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="#6e3f3f"  ,bg="#dedb9b" ,font=('times', 15, ' bold ') ) 
    lbl.place(x=400, y=200)

    txt = tk.Entry(window,width=20 ,textvar=id_r ,bg="#dedb9b" ,fg="#6e3f3f",font=('times', 15, ' bold '))
    txt.place(x=700, y=215)

    lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="#6e3f3f"  ,bg="#dedb9b"    ,height=2 ,font=('times', 15, ' bold ')) 
    lbl2.place(x=400, y=300)

    txt2 = tk.Entry(window,width=20  ,bg="#dedb9b" ,textvar=name_r ,fg="#6e3f3f",font=('times', 15, ' bold ')  )
    txt2.place(x=700, y=315)

    lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="#6e3f3f"  ,bg="#dedb9b"  ,height=2 ,font=('times', 15, ' bold underline ')) 
    lbl3.place(x=400, y=400)

    message = tk.Label(window, text="" ,bg="#dedb9b"  ,fg="#6e3f3f"  ,width=30  ,height=2, activebackground = "#dedb9b" ,font=('times', 15, ' bold ')) 
    message.place(x=700, y=400)
    
    
    
    





    takeImg = tk.Button(window, text="Register User Face", command=TakeImages  ,fg="#6e3f3f"  ,bg="#dedb9b"  ,width=20  ,height=3, activebackground = "#6e3f3f" ,font=('times', 15, ' bold '))
    takeImg.place(x=200, y=500)
    trainImg = tk.Button(window, text="Train User", command=TrainImages  ,fg="#6e3f3f"  ,bg="#dedb9b"  ,width=20  ,height=3, activebackground = "#6e3f3f" ,font=('times', 15, ' bold '))
    trainImg.place(x=500, y=500)
    track = tk.Button(window, text="TRACK", command=TrackImages  ,fg="#6e3f3f"  ,bg="#dedb9b"  ,width=20  ,height=3, activebackground = "#6e3f3f" ,font=('times', 15, ' bold '))
    track.place(x=760, y=500)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="#6e3f3f"  ,bg="#dedb9b"  ,width=20  ,height=3, activebackground = "#6e3f3f" ,font=('times', 15, ' bold '))
    quitWindow.place(x=1030, y=500)








     
    window.mainloop()

















 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(vid.get())
    name=(vname.get())
    d=(dat.get())
    p=name+str(Id)
    conn = pymysql.connect('localhost','root','root','face_auth')
    with conn:
        cursor=conn.cursor()
    
    cursor.execute('INSERT INTO user_detail (id,name,pass) VALUES(%s,%s,%s)',(Id,name,p))
    cursor.execute('INSERT INTO current_poll (voter_id,name,dat) VALUES(%s,%s,%s)',(Id,name,d))
    conn.commit()
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captu#6e3f3f face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('user_detail\Details.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("Recognizers\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
   
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("recognizers\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("user_detail\Details.csv")
    cam = cv2.VideoCapture(0)
    
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                time.sleep(1)
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
                
            else:
                Control()
                Id='Unknown'                
                tt=str(Id)
                
                      
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    
    fileName="Detail_1\Detail_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    
    cam.release()
    cv2.destroyAllWindows()
    return aa
    #print(attendance)

    
    
    
    


def new():
    
#lbl,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb8,lbl0=""
    l1 = tk.Label(window, text="User Voting PANEL",bg="#e09fc1"  ,fg="white"  ,width=40  ,height=2,font=('times', 30, 'italic bold'))
    l1.place(x=200,y=53)


    l2 = tk.Label(window, text="Voter ID:",fg="#6e3f3f"  ,bg="#dedb9b",width=20,font=("bold", 10))
    l2.place(x=400,y=240)
    
    txt7 = tk.Entry(window,textvar=vid)
    txt7.place(x=600,y=240)
    l4 = tk.Label(window, text="Name:",fg="#6e3f3f"  ,bg="#dedb9b",width=20,font=("bold", 10))
    l4.place(x=400,y=300)

    txt9 = tk.Entry(window,textvar=vname)
    txt9.place(x=600,y=300)

    
    tk.Button(window, text='candidate1',command=login1,fg="#6e3f3f"  ,bg="#dedb9b",width=25,height=3).place(x=250,y=440)
    tk.Button(window, text='candidate2',command=login2,fg="#6e3f3f"  ,bg="#dedb9b",width=25,height=3).place(x=500,y=440)
    tk.Button(window, text='candidate3',command=login3,fg="#6e3f3f"  ,bg="#dedb9b",width=25,height=3).place(x=750,y=440)
    
    
def winner():
    
    conn = pymysql.connect('localhost','root','root','face_auth')
    with conn:
        cursor=conn.cursor()
    
    cursor.execute("select * from vote")
    rec = cursor.fetchall()
    for i in rec:
        if(i[1]>i[2] and i[1]>i[3]):
            from tkinter import messagebox

            messagebox.showinfo("Result", "Candidate-1 is winner")
        elif(i[2]>i[3] and i[2]>i[1]):
            from tkinter import messagebox

            messagebox.showinfo("Result", "Candidate-2 is winner")
        elif(i[3]>i[1] and i[3]>i[2]):
            from tkinter import messagebox

            messagebox.showinfo("Result", "Candidate-3 is winner")
            

   
    
def admin_home():
    
   
#lbl,lb2,lb3,lb4,lb5,lb6,lb7,lb8,lb8,lbl0=""
    label_0 = tk.Label(window, text="ADMIN PANEL",bg="#e09fc1"  ,fg="white"  ,width=40  ,height=2,font=('times', 30, 'italic bold'))
    label_0.place(x=200,y=53)


    l6 = tk.Label(window, text="Aadhar no:",fg="#6e3f3f"  ,bg="#dedb9b",width=20,font=("bold", 10))
    l6.place(x=400,y=240)
    
    txt7 = tk.Entry(window,textvar=vid)
    txt7.place(x=600,y=240)
    l7 = tk.Label(window, text="Voter Name:",fg="#6e3f3f"  ,bg="#dedb9b",width=20,font=("bold", 10))
    l7.place(x=400,y=300)

    txt9 = tk.Entry(window,textvar=vname)
    txt9.place(x=600,y=300)

    l8 = tk.Label(window, text="Date & Time:",fg="#6e3f3f"  ,bg="#dedb9b",width=20,font=("bold", 10))
    l8.place(x=400,y=360)

    txt8 = tk.Entry(window,textvar=dat)
    txt8.place(x=600,y=360)
    tk.Button(window, text='Register face',fg="#6e3f3f"  ,bg="#dedb9b",command=TakeImages,width=25,height=3).place(x=100,y=440)
    tk.Button(window, text='Register face',fg="#6e3f3f"  ,bg="#dedb9b",command=TrainImages,width=25,height=3).place(x=300,y=440)
    tk.Button(window, text='Submit',fg="#6e3f3f"  ,bg="#dedb9b",command=reg,width=25,height=3).place(x=500,y=440)
    tk.Button(window, text='view_result',fg="#6e3f3f"  ,bg="#dedb9b",command=view_1,width=25,height=3).place(x=700,y=440)
    tk.Button(window, text='Result',fg="#6e3f3f"  ,bg="#dedb9b",command=winner,width=25,height=3).place(x=900,y=440)
    
    
    

def reg():
    s1=vid.get()
    s2=vname.get()
    s3=dat.get()
    print(s1)
    print(s2)
    conn = pymysql.connect('localhost','root','root','face_auth')
    with conn:
        cursor=conn.cursor()
    
    cursor.execute('INSERT INTO current_poll (voter_id,name,dat) VALUES(%s,%s,%s)',(s1,s2,s3))
    conn.commit()
    
    
def view_1():
    root = Tk()  
    root.title("Voted Records")
    root.minsize(800,500)
    root.geometry("1200x800")
    

    lb_header=['id', 'voter_id', 'name','dat']
    tree = ttk.Treeview(root,columns=lb_header,show='headings')
    for col in lb_header:
        tree.heading(col, text=col.title())
    # Database Call
    dbi = pymysql.connect('localhost','root','root','face_auth')
    cursor = dbi.cursor()

     
    tree.column("id", width=20)
    tree.column("voter_id", width=100)
    tree.column("name", width=100)
    tree.column("dat", width=100)
    


    cursor.execute("""SELECT * FROM voted_list """)
    myresult = cursor.fetchall()
    dbi.commit()
    for row in myresult:
        cpt = 0 
        tree.insert('', 'end', values=(row[0], row[1], row[2], row[3]))
        cpt += 1 # increment the ID
        tree.pack()


    
    




  
   
