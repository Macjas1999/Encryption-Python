import tkinter as tk
from tkinter import *
from tkinter import ttk
from cryptography.fernet import Fernet

class Input:
    def __init__(self, input) -> None:
        self.buffer = input

    def getLen(self):
        return len(self.buffer)

    def __del__(self) -> None:
        return 0

class Encryption:
    def __init__(self):
        self.message = ""
        self.key = None
        self.fernetObj = None
        self.encrypted = None
        self.decrypted = None

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

    def decryptCls(self):
        self.decrypted = self.fernetObj.decrypt(self.encrypted)

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

class WindowHandling():
    def __init__(self, root) -> None:
        self.root = root
        self.canvas1 = tk.Canvas(self.root, width=800, height=800, relief='raised')
        self.canvas1.grid()
        self.mainEncryptionObj = Encryption()

        self.style = ttk.Style()
        self.style.configure("TButton", foreground="white", background="blue")

    def initScreen(self):
        self.label1 = ttk.Label(self.root, text='Choose what you want to do')
        self.label1.config(font=('helvetica', 20))
        self.canvas1.create_window(385, 70, window=self.label1)

        self.button1 = ttk.Button(text='Generate new key and encrypt', command=self.handleNewKeyEncrypt, style="TButton")
        #self.button1 = ttk.Button(text='Generate new key and encrypt', command=self.handleNewKeyEncrypt, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(170, 140, window=self.button1)

        self.button2 = ttk.Button(text='Input key and encrypt', command=self.handleInputKeyEncrypt, style="TButton")
        #self.button2 = ttk.Button(text='Input key and encrypt', command=self.handleInputKeyEncrypt, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(340, 140, window=self.button2)

        self.button3 = ttk.Button(text='Decrypt with key', command=self.handleDecryptWithKey, style="TButton")
        #self.button3 = ttk.Button(text='Decrypt with key', command=self.handleDecryptWithKey, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(470, 140, window=self.button3)

        self.button4 = ttk.Button(text='Decrypt single message', command=self.handleDecryptSingleMessage, style="TButton")
        #self.button4 = ttk.Button(text='Decrypt single message', command=self.handleDecryptSingleMessage, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(610, 140, window=self.button4)

    def handleNewKeyEncrypt(self):
        self.mainEncryptionObj.generateKey()

        self.label3 = tk.Label(self.root, text='Generated key:', font=('helvetica', 20))
        self.canvas1.create_window(385, 70, window=self.label3)
        self.entry1 = tk.Text(self.root, wrap='word', width=60, height=2, font=('helvetica', 12))
        self.canvas1.create_window(385, 180, window=self.entry1)
        self.entry1.insert('1.0', self.mainEncryptionObj.getKeyDecoded())

        self.button1.grid_forget()
        self.button2.grid_forget()
        self.button3.grid_forget()
        self.button4.grid_forget()
        self.buttonGo = tk.Button(text='Click to enter your message', command=self.inputFromTextfield, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(215, 140, window=self.buttonGo)

    def inputFromTextfield(self):
        self.label3 = tk.Label(self.root, text='Enter your message here:', font=('helvetica', 20))
        self.canvas1.create_window(385, 70, window=self.label3)
        self.entry1 = tk.Text(self.root, wrap='word', width=60, height=10, font=('helvetica', 12))
        self.canvas1.create_window(385, 180, window=self.entry1)
        msg = self.entry1.get("1.0", "end-1c")
        self.mainEncryptionObj.setMessage(msg)
        self.buttonSubmit = tk.Button(text='Submit', command=lambda: [self.displayEncryptedText(), self.label3.destroy(), self.buttonSubmit.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(150, 70, window=self.buttonSubmit)

    def displayEncryptedText(self):
        self.entry1 = tk.Text(self.root, wrap='word', width=60, height=10, font=('helvetica', 12))
        self.canvas1.create_window(385, 180, window=self.entry1)
        self.mainEncryptionObj.encryptCls()
        self.entry1.insert('1.0', self.mainEncryptionObj.decodeEncrypted())
        self.buttonReturn = tk.Button(text='Return to menu', command=self.returnToMenu, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        self.canvas1.create_window(550, 70, window=self.buttonReturn)

    def handleInputKeyEncrypt(self):
        # Implement the logic for handling input key and encryption
        pass

    def handleDecryptWithKey(self):
        # Implement the logic for decrypting with a key
        pass

    def handleDecryptSingleMessage(self):
        # Implement the logic for decrypting a single message
        pass

    def returnToMenu(self):
        self.entry1.delete('1.0', END)
        self.buttonReturn.destroy()

root= tk.Tk()        
window = WindowHandling(root)
window.initScreen()
root.mainloop()
       
