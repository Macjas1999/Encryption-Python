import tkinter as tk
import random
from cryptography.fernet import Fernet

#Logick
class Enctrypton:
    #essential methods
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

    #mixup part  
    def mixUpRandom(self, keyDecoded, messageDecoded) -> str:
        # Split the Fernet key into 4 fixed slices (11 chars each, total 44)
        slice1 = keyDecoded[0:11]
        slice2 = keyDecoded[11:22]
        slice3 = keyDecoded[22:33]
        slice4 = keyDecoded[33:44]

        # Choose 4 random insertion positions inside the message and sort them
        msg_len = len(messageDecoded)
        # Ensure we have room to insert 4 slices
        if msg_len < 5:
            raise ValueError("Message too short for random mix up.")

        self.sliceKey = sorted(random.sample(range(1, msg_len), 4))
        a, b, c, d = self.sliceKey

        # Interleave message segments with the 4 key slices
        return (
            messageDecoded[0:a] + slice1 +
            messageDecoded[a:b] + slice2 +
            messageDecoded[b:c] + slice3 +
            messageDecoded[c:d] + slice4 +
            messageDecoded[d:]
        )

    def unmixUpRandom(self, received, sliceKey) -> str:
        # sliceKey contains the 4 insertion positions used during mixUpRandom
        self.sliceKey = sorted(sliceKey)
        a, b, c, d = self.sliceKey

        # In the mixed string, each key slice is 11 chars long and shifts subsequent positions
        slice1 = received[a:a + 11]
        slice2 = received[b + 11:b + 22]
        slice3 = received[c + 22:c + 33]
        slice4 = received[d + 33:d + 44]
        key = slice1 + slice2 + slice3 + slice4

        # Rebuild original message by skipping the key slices
        message = (
            received[0:a] +
            received[a + 11:b + 11] +
            received[b + 22:c + 22] +
            received[c + 33:d + 33] +
            received[d + 44:]
        )

        self.setKey(key)
        self.setMessage(message)
        


    def __del__(self) -> None:
        return 0
########################################################
#GUI

class MainWindow:``

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._configure_window()

    def _configure_window(self) -> None:
        self.root.title("Cryptography tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()