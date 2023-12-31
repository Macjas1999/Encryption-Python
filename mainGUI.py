import tkinter as tk
from tkinter import *
import tkinter.messagebox 
from cryptography.fernet import Fernet


class Enctrypton:
    #   fernetObj
    #   messageAsString
    #   messageAsBytes
    #   keyAsBytes
    #   keyAsString
    #   encryptedAsBytes
    #   encryptedAsString
    #   decryptedAsBytes
    #   decryptedAsString
    
    def setMessage(self, message):
        if isinstance(message, str):
            self.messageAsString = message
            self.messageAsBytes = bytes(message, 'utf-8')
        elif isinstance(message, bytes):
            self.messageAsBytes = message
            self.messageAsString = message.decode('utf-8')

    def generateKey(self):
        self.keyAsBytes = Fernet.generate_key()
        self.keyAsString = self.keyAsBytes.decode('utf-8')
        self.fernetObj = Fernet(self.keyAsBytes)
    
    def setKey(self, key):
        if isinstance(key, str):
            self.keyAsString = key
            self.keyAsBytes = bytes(key, 'utf-8')
        elif isinstance(key, bytes):
            self.keyAsBytes = key
            self.keyAsString = key.decode('utf-8')
        self.fernetObj = Fernet(self.keyAsBytes)

    def getKey(self, format):  #format should be either 'b' for bytes or 's' for string
        match format:
            case 'b':
                return self.keyAsBytes
            case 's':   
                return self.keyAsString     

    def encryptCls(self):
        self.encryptedAsBytes = self.fernetObj.encrypt(self.messageAsBytes)
        self.encryptedAsString = self.encryptedAsBytes.decode('utf-8')

    def decryptCls(self):
        self.decryptedAsBytes = self.fernetObj.decrypt(self.messageAsBytes)
        self.decryptedAsString = self.decryptedAsBytes.decode('utf-8')

    def mixUp(self, keyDecoded, messageDecoded) -> str:
        slice1 = keyDecoded[0:11]
        slice2 = keyDecoded[11:22]
        slice3 = keyDecoded[22:33]
        slice4 = keyDecoded[33:44]
        return messageDecoded[0:11] + slice1 + messageDecoded[11:22] + slice2 + messageDecoded[22:33] + slice3 + messageDecoded[33:44] + slice4 + messageDecoded[44:]

    def unmixUp(self, received):
        key = received[11:22] + received[33:44] + received[55:66] + received[77:88]
        message = received[0:11] + received[22:33] + received[44:55] + received[66:77] + received[88:]
        self.setKey(key)
        self.setMessage(message)

    def __del__(self) -> None:
        return 0
    
#Tkinter handling  
class windowHandling():

    def __init__(self, root) -> None:
        self.root = root

        self.mainCanvasHeight = 600
        self.mainCanvasWidth = 800

        self.returnButtonX = 600
        self.returnButtonY = 135

        self.aboveTextButton = 135

        self.topLabelX = 385
        self.topLabelY = 70

    def initScreen(self):        
        self.mainEncryptionObj = Enctrypton()

        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()

        label1 = tk.Label(self.root, text='Choose what you want to do')
        label1.config(font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label1)
        button1 = tk.Button(text='Generate new key and encrypt', command=lambda: [self.handleNewKeyEncrypt(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(170, 140, window=button1)
        button2 = tk.Button(text='Input key and encrypt', command=lambda: [self.handleHasAKey(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(340, 140, window=button2)
        button3 = tk.Button(text='Decrypt with key', command=lambda: [self.decryptMainInput('k'), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(470, 140, window=button3)
        button4 = tk.Button(text='Decrypt single message', command=lambda: [self.decryptMainInput('t'), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(610, 140, window=button4)

    def isKeyCorrect(self, input, mode):
        match mode:
            case 'e':
                try:
                    self.mainEncryptionObj.setKey(input)
                    self.inputFromTextfieldEncryption()
                except:
                    tkinter.messagebox.showerror(title="Warning", message="Input is not a valid key")
                    self.initScreen()
            case 'd':
                try:
                    self.mainEncryptionObj.setKey(input)
                    self.inputFromTextfieldDecryption()
                except:
                    tkinter.messagebox.showerror(title="Warning", message="Input is not a valid key")
                    self.initScreen()
##Encryption
    def handleHasAKey(self):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()

        label3 = tk.Label(self.root, text='Input your key:',font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)

        entry1 = tk.Text(root, wrap='word', width=60, height=2 ,font=('helvetica', 12)) 
        canvasThis.create_window(385, 170, window=entry1)
        entry1.config(state=NORMAL)

        buttonGo = tk.Button(text='Click to enter your message', command=lambda: [self.isKeyCorrect(entry1.get('1.0', 'end'), 'e'),
                                                                                  entry1.delete('1.0', 'end'),
                                                                                  canvasThis.destroy()],
                                                                                  bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(210, self.aboveTextButton, window=buttonGo)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)


    def handleNewKeyEncrypt(self):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()

        self.mainEncryptionObj.generateKey()
        label3 = tk.Label(self.root, text='Generated key:',font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)
        
        entry1 = tk.Text(self.root, wrap='word', width=60, height=2 ,font=('helvetica', 12)) 
        canvasThis.create_window(385, 170, window=entry1)
        entry1.insert('1.0', self.mainEncryptionObj.getKey('s'))

        buttonGo = tk.Button(text='Click to enter your message', command=lambda: [self.inputFromTextfieldEncryption(),
                                                                                  canvasThis.destroy()], 
                                                                                  bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(210, self.aboveTextButton, window=buttonGo)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)

    def inputFromTextfieldEncryption(self):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()
        
        label3 = tk.Label(root, text='Enter your message here:',font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)

        entry1 = tk.Text(root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
        canvasThis.create_window(385, 240, window=entry1)
        entry1.config(state=NORMAL)
        buttonSubmit = tk.Button(text='Submit', command=lambda: [self.mainEncryptionObj.setMessage(entry1.get('1.0', 'end')),
                                                                 entry1.delete('1.0', 'end'),
                                                                 canvasThis.destroy(),
                                                                 self.displayEncryptedText('s')], 
                                                                 bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(150, self.aboveTextButton, window=buttonSubmit)

        buttonEntangle = tk.Button(text='Entangle', command=lambda: [self.mainEncryptionObj.setMessage(entry1.get('1.0', 'end')),
                                                                    entry1.delete('1.0', 'end'), 
                                                                    canvasThis.destroy(),
                                                                    self.displayEncryptedText('e')],
                                                                    bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(220, self.aboveTextButton, window=buttonEntangle)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)

    def displayEncryptedText(self, mode):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()

        label3 = tk.Label(root, text='Your message has been encrypted:',font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)
    
        match mode:
            case 's':
                entry1 = tk.Text(self.root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
                canvasThis.create_window(385, 240, window=entry1)
                self.mainEncryptionObj.encryptCls()
                entry1.insert('1.0', self.mainEncryptionObj.encryptedAsString)
            case 'e':
                entry1 = tk.Text(self.root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
                canvasThis.create_window(385, 240, window=entry1)
                self.mainEncryptionObj.encryptCls()
                entangled = self.mainEncryptionObj.mixUp(self.mainEncryptionObj.keyAsString, self.mainEncryptionObj.encryptedAsString)
                entry1.insert('1.0', entangled)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)
##Decryption
    def decryptMainInput(self, mode):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()

        match mode:
            case 'k':
                label3 = tk.Label(self.root, text='Input your key:',font=('helvetica', 20))
                canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)

                entry1 = tk.Text(root, wrap='word', width=60, height=2, font=('helvetica', 12)) 
                canvasThis.create_window(385, 170, window=entry1)
                entry1.config(state=NORMAL)

                buttonGo = tk.Button(text='Click to enter message to be decoded', command=lambda: [self.isKeyCorrect(entry1.get('1.0', 'end'), 'd'),
                                                                                          entry1.delete('1.0', 'end'),
                                                                                          canvasThis.destroy()],
                                                                                          bg='blue', fg='white', font=('helvetica', 9, 'bold'))
                canvasThis.create_window(240, self.aboveTextButton, window=buttonGo)
            case 't':
                label3 = tk.Label(self.root, text='Input your message:',font=('helvetica', 20))
                canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)

                entry1 = tk.Text(root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
                canvasThis.create_window(385, 240, window=entry1)
                entry1.config(state=NORMAL)
        
                buttonGo = tk.Button(text='Submit', command=lambda: [self.mainEncryptionObj.unmixUp(entry1.get('1.0', 'end')),
                                                                    entry1.delete('1.0', 'end'),
                                                                    canvasThis.destroy(),
                                                                    self.displayDecryptedText()],
                                                                    bg='blue', fg='white', font=('helvetica', 9, 'bold'))
                canvasThis.create_window(150, self.aboveTextButton, window=buttonGo)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)
    
    def inputFromTextfieldDecryption(self):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()
        
        label3 = tk.Label(root, text='Enter your message here:',font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)

        entry1 = tk.Text(root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
        canvasThis.create_window(385, 240, window=entry1)
        entry1.config(state=NORMAL)
        buttonSubmit = tk.Button(text='Submit', command=lambda: [self.mainEncryptionObj.setMessage(entry1.get('1.0', 'end')),
                                                                 entry1.delete('1.0', 'end'),
                                                                 canvasThis.destroy(),
                                                                 self.displayDecryptedText()], 
                                                                 bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(150, self.aboveTextButton, window=buttonSubmit)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)

    def displayDecryptedText(self):
        canvasThis = tk.Canvas(self.root, width=self.mainCanvasWidth, height=self.mainCanvasHeight, relief='raised')
        canvasThis.grid()

        label3 = tk.Label(root, text='Your message has been decrypted:',font=('helvetica', 20))
        canvasThis.create_window(self.topLabelX, self.topLabelY, window=label3)

        entry1 = tk.Text(self.root, wrap='word', width=60, height=10 ,font=('helvetica', 12)) 
        canvasThis.create_window(385, 240, window=entry1)
        self.mainEncryptionObj.decryptCls()
        entry1.insert('1.0', self.mainEncryptionObj.decryptedAsString)

        buttonReturn = tk.Button(text='Return to menu', command=lambda: [self.initScreen(), canvasThis.destroy()], bg='blue', fg='white', font=('helvetica', 9, 'bold'))
        canvasThis.create_window(self.returnButtonX, self.returnButtonY, window=buttonReturn)

#Mainloot
root= tk.Tk()
root.title('Cryptography tool')        
window = windowHandling(root)
window.initScreen()
root.mainloop()