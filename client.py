from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from socket import *
from threading import *

top = Tk()
top.title("Guess the photo (client)")
top.geometry("630x500")
top.config(bg="lightblue")

# Add animal images
img = Image.open("dog.png")
img = img.resize((70, 70), Image.LANCZOS)
dogImg = ImageTk.PhotoImage(img)

img = Image.open("cat.png")
img = img.resize((70, 70), Image.LANCZOS)
catImg = ImageTk.PhotoImage(img)

img = Image.open("sheep.png")
img = img.resize((70, 70), Image.LANCZOS)
sheepImg = ImageTk.PhotoImage(img)

label1 = Label(top, text="Your choice :", font=("Arial", 12))
label1.place(x=50, y=25)

myChoiceLabel = Label(top, width=30, height=17, bg="black")
myChoiceLabel.place(x=50, y=50)

label2 = Label(top, text="Opponent choice :", font=("bookman", 12))
label2.place(x=350, y=25)

opponentChoiceLabel = Label(top, width=19, height=11, bg="black", text="Still Choosing...", fg="white", font=(12))
opponentChoiceLabel.place(x=350, y=50)

vs = Label(top, text="VS", fg="black", font=("Arial", 18), bg="yellow")
vs.place(x=290, y=150)

myRespond = ''
opponentRespond = ''
imgIntended = dogImg
flag = False

def resetGame():
    global myRespond, opponentRespond, flag
    myRespond = ''
    opponentRespond = ''
    flag = False
    myChoiceLabel.config(image='', width=30, height=17, bg="black")
    opponentChoiceLabel.config(text="Still Choosing...", fg="white", width=19, height=11, bg="black")
    for child in frame.winfo_children():
        child.configure(state="normal")

def win(message):
    messagebox.showinfo("Result", message)
    if "Well done!" in message:
        top.destroy()
    else:
        resetGame()

def checkResult():
    if myRespond == opponentRespond:
        win(f"Both players guessed {myRespond}. Well done!")
    else:
        win("The choices do not match. Starting over...")


def checkRespond():
    global opponentRespond, imgIntended
    if opponentRespond == "dog":
        imgIntended = dogImg
    elif opponentRespond == "cat":
        imgIntended = catImg
    elif opponentRespond == "sheep":
        imgIntended = sheepImg

def clickDog():
    global flag, myRespond, opponentRespond, imgIntended
    flag = True
    myRespond = "dog"
    myChoiceLabel.config(image=dogImg, width=220, height=250, bg="#82f937", highlightbackground="black",
                         highlightthickness=3)
    catButton.config(bg="white")
    sheepButton.config(bg="white")
    for child in frame.winfo_children():
        child.configure(state="disabled")
    if opponentRespond != '':
        checkRespond()
        opponentChoiceLabel.config(image=imgIntended, width=220, height=250, bg="#f1fc30", highlightbackground="black",
                                   highlightthickness=3)
        checkResult()
    send("dog")

def clickCat():
    global flag, myRespond, opponentRespond, imgIntended
    flag = True
    myRespond = "cat"
    myChoiceLabel.config(image=catImg, width=220, height=250, bg="#82f937", highlightbackground="black",
                         highlightthickness=3)
    dogButton.config(bg="white")
    sheepButton.config(bg="white")
    for child in frame.winfo_children():
        child.configure(state="disabled")
    if opponentRespond != '':
        checkRespond()
        opponentChoiceLabel.config(image=imgIntended, width=220, height=250, bg="#f1fc30", highlightbackground="black",
                                   highlightthickness=3)
        checkResult()
    send("cat")

def clickSheep():
    global flag, myRespond, opponentRespond, imgIntended
    flag = True
    myRespond = "sheep"
    myChoiceLabel.config(image=sheepImg, width=220, height=250, bg="#82f937", highlightbackground="black",
                         highlightthickness=3)
    dogButton.config(bg="white")
    catButton.config(bg="white")
    for child in frame.winfo_children():
        child.configure(state="disabled")
    if opponentRespond != '':
        checkRespond()
        opponentChoiceLabel.config(image=imgIntended, width=220, height=250, bg="#f1fc30", highlightbackground="black",
                                   highlightthickness=3)
        checkResult()
    send("sheep")

label3 = Label(top, text="Choices :", font=("Arial", 12), bg="#dae0e8")
label3.place(x=50, y=330)

canvas = Canvas(top, width=520, height=5, bg="#0fb1f7", highlightbackground="lightblue")
canvas.place(x=50, y=355)
canvas.create_line(0, 5, 520, 5)

frame = Frame(top, width=520, height=100, bg="lightblue")
frame.place(x=50, y=370)

dogButton = Button(frame, image=dogImg, width=100, height=100, bg="#fdba3a", bd=3, command=clickDog)
dogButton.place(x=0, y=0)

catButton = Button(frame, image=catImg, width=100, height=100, bd=3, bg="#fdba3a", command=clickCat)
catButton.place(x=200, y=0)

sheepButton = Button(frame, image=sheepImg, width=100, height=100, bd=3, bg="#fdba3a", command=clickSheep)
sheepButton.place(x=400, y=0)

def handler():
    global opponentRespond
    while True:
        respond = s.recv(2048)
        respond = respond.decode('UTF-8')
        if respond == "dog":
            opponentChoiceLabel.config(text="he is ready", fg="black", width=19, height=11, bg="#f1fc30",
                                       highlightbackground="black", highlightthickness=3)
            opponentRespond = "dog"
            if flag:
                opponentChoiceLabel.config(image=dogImg, width=220, height=250, bg="#f1fc30",
                                           highlightbackground="black", highlightthickness=3)
                checkResult()

        elif respond == "cat":
            opponentChoiceLabel.config(text="he is ready", fg="black", width=19, height=11, bg="#f1fc30",
                                       highlightbackground="black", highlightthickness=3)
            opponentRespond = "cat"
            if flag:
                opponentChoiceLabel.config(image=catImg, width=220, height=250, bg="#f1fc30",
                                           highlightbackground="black", highlightthickness=3)
                checkResult()

        elif respond == "sheep":
            opponentChoiceLabel.config(text="he is ready", fg="black", width=19, height=11, bg="#f1fc30",
                                       highlightbackground="black", highlightthickness=3)
            opponentRespond = "sheep"
            if flag:
                opponentChoiceLabel.config(image=sheepImg, width=220, height=250, bg="#f1fc30",
                                           highlightbackground="black", highlightthickness=3)
                checkResult()

s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 6000
s.connect((host, port))

thread = Thread(target=handler)
thread.start()

def send(val):
    s.send(val.encode('UTF-8'))

top.mainloop()
