import tkinter as tk
from tkinter import *
from cryptography.fernet import Fernet


class Input:
    def __init__(self, input) -> None:
        self.buffer = input

    def getLen(self):
        return len(self.buffer)
    
    def __del__(self) -> None:
        return 0
    
class Enctrypton:
    def setMessage(self, message):
        self.message = message

    def generateKey(self):
        self.key = Fernet.generate_key()
        self.fernetObj = Fernet(self.key)
    
    def setKey(self, key):
        self.key = key
        self.fernetObj = Fernet(self.key)

    def getKey(self):
        return self.key
    
    def getKeyDecoded(self) -> str:
        return self.key.decode('utf-8')

    def decodeEncrypted(self) -> str:
        self.encryptedDecoded = self.encrypted.decode('utf-8')
        return self.encryptedDecoded
    
    def encryptCls(self):
        self.encrypted = self.fernetObj.encrypt(bytes(self.message, 'utf-8'))
        #return self.encrypted

    def decryptCls(self):
        self.decrypted = self.fernetObj.decrypt(self.message)
        #return self.decrypted

    def mixUp(self, keyDecoded, messageDecoded) -> str:
        slice1 = keyDecoded[0:11]
        slice2 = keyDecoded[11:22]
        slice3 = keyDecoded[22:33]
        slice4 = keyDecoded[33:44]
        return messageDecoded[0:11] + slice1 + messageDecoded[11:22] + slice2 + messageDecoded[22:33] + slice3 + messageDecoded[33:44] + slice4 + messageDecoded[44:]

    def unmixUp(self, received):
        key = received[11:22] + received[33:44] + received[55:66] + received[77:88]
        message = received[0:11] + received[22:33] + received[44:55] + received[66:77] + received[88:]
        key = bytes(key, 'utf-8')
        message = bytes(message, 'utf-8')
        self.setKey(key)
        self.setMessage(message)

    def __del__(self) -> None:
        return 0
#Tkinter handling    
def handleNewKeyEncrypt():
    mainEncryptionObj.generateKey()

    label3 = tk.Label(root, text='Generated key:',font=('helvetica', 20))
    label1.destroy()
    canvas1.create_window(385, 70, window=label3)
    entry1 = tk.Text(root, wrap='word', width=60, height=2 ,font=('helvetica', 12)) 
    canvas1.create_window(385, 180, window=entry1)
    entry1.insert('1.0', mainEncryptionObj.getKeyDecoded())

    button1.destroy()
    button2.destroy()
    button3.destroy()
    button4.destroy()
    buttonGo = tk.Button(text='Click to enter your message', command=lambda: [inputFromTextfield(), label3.destroy(), buttonGo.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
    canvas1.create_window(215, 140, window=buttonGo)
    # label3.destroy()
    # entry1.destroy()

def inputFromTextfield():
    label3 = tk.Label(root, text='Enter your message here:',font=('helvetica', 20))
    buttonSubmit = tk.Button(text='Submit', command=lambda: [displayEncryptedText(), label3.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
    canvas1.create_window(150, 140, window=buttonSubmit)
    canvas1.create_window(385, 70, window=label3)
    entry1 = tk.Text(root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
    canvas1.create_window(385, 180, window=entry1)
    msg = entry1.get(index1='1.0')
    mainEncryptionObj.setMessage(msg)
    entry1.destroy()

def displayEncryptedText():
    entry1 = tk.Text(root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
    canvas1.create_window(385, 180, window=entry1)
    mainEncryptionObj.encryptCls()
    entry1.insert('1.0', mainEncryptionObj.decodeEncrypted())




root= tk.Tk()
#root.geometry("800x800")
mainEncryptionObj = Enctrypton()

canvas1 = tk.Canvas(root, width=800, height=800, relief='raised')
canvas1.grid()

label1 = tk.Label(root, text='Choose what you want to do')
label1.config(font=('helvetica', 20))
canvas1.create_window(385, 70, window=label1)

button1 = tk.Button(text='Generate new key and encrypt', command=handleNewKeyEncrypt, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(170, 140, window=button1)

button2 = tk.Button(text='Input key and encrypt', command=handleNewKeyEncrypt, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(340, 140, window=button2)

button3 = tk.Button(text='Decrypt with key', command=handleNewKeyEncrypt, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(470, 140, window=button3)

button4 = tk.Button(text='Decrypt single message', command=handleNewKeyEncrypt, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(610, 140, window=button4)

# label3 = tk.Label(root, text='Enter your key',font=('helvetica', 20))
# canvas1.create_window(385, 70, window=label3)
# entry1 = tk.Entry(root,width=40 ,font=('helvetica', 20)) 
# canvas1.create_window(385, 140, window=entry1)

def get_square_root():
    x1 = entry1.get()
    
    label3 = tk.Label(root, text='The Square Root of ' + x1 + ' is:', font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)
    
    label4 = tk.Label(root, text=float(x1)**0.5, font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 230, window=label4)
    
#button1 = tk.Button(text='Get the Square Root', command=get_square_root, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
#canvas1.create_window(200, 180, window=button1)

root.mainloop()