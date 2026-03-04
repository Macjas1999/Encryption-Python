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

class MainWindow:

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.encryption = Enctrypton()
        self._configure_window()
        self._build_main_menu()

    def _configure_window(self) -> None:
        self.root.title("Cryptography tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

    def _clear_window(self) -> None:
        # Remove all existing widgets from the root window
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_return_to_main_button(self) -> tk.Button:
        #helper to retur to the main menu from any view
        button = tk.Button(
            self.root,
            text="Return",
            width=3,
            height=2,
            command=self._build_main_menu,
        )
        button.place(x=10, y=10)
        button.lift()
        return button

##### Main menu #####
    def _build_main_menu(self) -> None:
        self._clear_window()

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        title_label = tk.Label(
            frame,
            text="Choose an action",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=40)

        encrypt_button = tk.Button(
            frame,
            text="Encrypt",
            width=20,
            height=2,
            command=self._show_encrypt_view
        )
        encrypt_button.pack(pady=10)

        decrypt_button = tk.Button(
            frame,
            text="Decrypt",
            width=20,
            height=2,
            command=self._show_decrypt_view
        )
        decrypt_button.pack(pady=10)
########## Encrypt view #####
    def _show_encrypt_view(self) -> None:
        self._clear_window()

        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        label = tk.Label(
            frame,
            text="Encryptions",
            font=("Arial", 20, "bold")
        )
        label.pack(pady=40)

        # Input field for message to encrypt
        message_label = tk.Label(
            frame,
            text="Message to encrypt:",
            font=("Arial", 12)
        )
        message_label.pack(anchor="w", padx=40)

        self.encrypt_message_text = tk.Text(
            frame,
            height=8,
            width=60
        )
        self.encrypt_message_text.pack(padx=40, pady=10, fill="x")

        # Reusable return button
        self.return_to_main_button = self._create_return_to_main_button()


########## Decrypt view #####
    def _show_decrypt_view(self) -> None:
        self._clear_window()

        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        label = tk.Label(
            frame,
            text="Decryption",
            font=("Arial", 20, "bold")
        )
        label.pack(pady=40)

        # Input field for message to decrypt
        message_label = tk.Label(
            frame,
            text="Message to decrypt:",
            font=("Arial", 12)
        )
        message_label.pack(anchor="w", padx=40)

        self.decrypt_message_text = tk.Text(
            frame,
            height=8,
            width=60
        )
        self.decrypt_message_text.pack(padx=40, pady=10, fill="x")

        # Reusable return button
        self.return_to_main_button = self._create_return_to_main_button()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()