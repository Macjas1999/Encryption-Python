import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

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

        # Configure a modern ttk theme and styles
        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.style.configure(
            "TFrame",
            background="#111827",
        )
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 20, "bold"),
            foreground="#E5E7EB",
            background="#111827",
        )
        self.style.configure(
            "Body.TLabel",
            font=("Segoe UI", 11),
            foreground="#E5E7EB",
            background="#111827",
        )
        self.style.configure(
            "TButton",
            font=("Segoe UI", 11),
            padding=6,
            relief="flat",
        )
        # Primary accent button style (visible color change)
        self.style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            background="#2563EB",
            foreground="#F9FAFB",
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1D4ED8")],
            foreground=[("disabled", "#9CA3AF"), ("!disabled", "#F9FAFB")],
        )

        self._build_main_menu()

    def _configure_window(self) -> None:
        self.root.title("Cryptography tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.configure(bg="#111827")

    def _clear_window(self) -> None:
        # Remove all existing widgets from the root window
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_return_to_main_button(self) -> tk.Button:
        #helper to retur to the main menu from any view
        button = ttk.Button(self.root, text="Return", width=6, command=self._build_main_menu)
        button.place(x=10, y=10)
        button.lift()
        return button

##### Main menu #####
    def _build_main_menu(self) -> None:
        self._clear_window()

        frame = ttk.Frame(self.root)
        frame.pack(expand=True)

        title_label = ttk.Label(frame, text="Choose an action", style="Title.TLabel")
        title_label.pack(pady=40)

        # Button for "Mix Up Random" (mix key into encrypted message with random positions)
        mixup_button = ttk.Button(
            frame,
            text="Mix Up Random",
            command=self._show_mixup_view,
            style="Accent.TButton",
        )
        mixup_button.pack(pady=10)

        # Button for "Unmix Up Random" (reverse interleaving and extract original/key)
        unmixup_button = ttk.Button(
            frame,
            text="Unmix Up Random",
            command=self._show_unmixup_view,
            style="Accent.TButton",
        )
        unmixup_button.pack(pady=10)

        encrypt_button = ttk.Button(
            frame,
            text="Encrypt",
            command=self._show_encrypt_view,
            style="Accent.TButton",
        )
        encrypt_button.pack(pady=10)

        decrypt_button = ttk.Button(
            frame,
            text="Decrypt",
            command=self._show_decrypt_view,
            style="Accent.TButton",
        )
        decrypt_button.pack(pady=10)
########## Encrypt view #####
    def _show_encrypt_view(self) -> None:
        self._clear_window()

        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        label = ttk.Label(frame, text="Encryptions", style="Title.TLabel")
        label.pack(pady=40)

        # Input field for message to encrypt
        message_label = ttk.Label(frame, text="Message to encrypt:", style="Body.TLabel")
        message_label.pack(anchor="w", padx=40)

        self.encrypt_message_text = tk.Text(
            frame,
            height=8,
            width=60
        )
        self.encrypt_message_text.pack(padx=40, pady=10, fill="x")

        # Button to confirm encryption
        encrypt_button = ttk.Button(
            frame,
            text="Encrypt message",
            command=self._on_encrypt_click,
            style="Accent.TButton",
        )
        encrypt_button.pack(pady=(0, 20))

        key_label = ttk.Label(frame, text="Key generated", style="Body.TLabel")
        key_label.pack(anchor="w", padx=40)

        self.encrypt_key_text = tk.Text(
            frame,
            height=8,
            width=60,
            state=tk.DISABLED
        )
        self.encrypt_key_text.pack(padx=40, pady=10, fill="x")
        


        # Reusable return button
        self.return_to_main_button = self._create_return_to_main_button()

    def _on_encrypt_click(self) -> None:
        """Encrypt the text from encrypt_message_text and show result and key."""
        if not hasattr(self, "encrypt_message_text"):
            return

        message = self.encrypt_message_text.get("1.0", tk.END).strip()
        if not message:
            return

        # Use Enctrypton to generate key and encrypt the message
        self.encryption.setMessage(message)
        self.encryption.generateKey()
        self.encryption.encryptCls()

        encrypted_text = self.encryption.encryptedAsString
        key_text = self.encryption.getKey("s")

        # Show encrypted message in the same text widget
        self.encrypt_message_text.delete("1.0", tk.END)
        self.encrypt_message_text.insert("1.0", encrypted_text)

        # Show key in the key text widget (read-only)
        if hasattr(self, "encrypt_key_text"):
            self.encrypt_key_text.config(state=tk.NORMAL)
            self.encrypt_key_text.delete("1.0", tk.END)
            self.encrypt_key_text.insert("1.0", key_text)
            self.encrypt_key_text.config(state=tk.DISABLED)


########## Decrypt view ##########
    def _show_decrypt_view(self) -> None:
        self._clear_window()

        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        label = ttk.Label(frame, text="Decryption", style="Title.TLabel")
        label.pack(pady=40)

        # Input field for message to decrypt
        message_label = ttk.Label(frame, text="Message to decrypt:", style="Body.TLabel")
        message_label.pack(anchor="w", padx=40)

        self.decrypt_message_text = tk.Text(
            frame,
            height=8,
            width=60
        )
        self.decrypt_message_text.pack(padx=40, pady=10, fill="x")

        # Button to confirm decryption (initially disabled)
        self.decrypt_button = ttk.Button(
            frame,
            text="Decrypt message",
            state=tk.DISABLED,
            command=self._on_decrypt_click,
            style="Accent.TButton",
        )
        self.decrypt_button.pack(pady=(0, 10))

        # Input field for key used for decryption
        key_label = ttk.Label(frame, text="Key for decryption:", style="Body.TLabel")
        key_label.pack(anchor="w", padx=40)

        self.decrypt_key_text = tk.Text(
            frame,
            height=4,
            width=60
        )
        self.decrypt_key_text.pack(padx=40, pady=10, fill="x")

        # Enable/disable decrypt button based on both fields being filled
        self.decrypt_message_text.bind("<<Modified>>", self._on_decrypt_fields_modified)
        self.decrypt_key_text.bind("<<Modified>>", self._on_decrypt_fields_modified)

        # Reusable return button
        self.return_to_main_button = self._create_return_to_main_button()

    def _on_decrypt_fields_modified(self, event: tk.Event) -> None:
        # Reset modified flag so event keeps firing
        try:
            event.widget.edit_modified(False)
        except Exception:
            pass

        msg = ""
        key = ""
        if hasattr(self, "decrypt_message_text"):
            msg = self.decrypt_message_text.get("1.0", tk.END).strip()
        if hasattr(self, "decrypt_key_text"):
            key = self.decrypt_key_text.get("1.0", tk.END).strip()

        if hasattr(self, "decrypt_button"):
            new_state = tk.NORMAL if msg and key else tk.DISABLED
            self.decrypt_button.config(state=new_state)

    def _on_decrypt_click(self) -> None:
        """Decrypt the text from decrypt_message_text using the provided key."""
        if not (hasattr(self, "decrypt_message_text") and hasattr(self, "decrypt_key_text")):
            return

        encrypted_msg = self.decrypt_message_text.get("1.0", tk.END).strip()
        key = self.decrypt_key_text.get("1.0", tk.END).strip()
        if not encrypted_msg or not key:
            return

        try:
            self.encryption.setKey(key)
            self.encryption.setMessage(encrypted_msg)
            self.encryption.decryptCls()
            decrypted_text = self.encryption.decryptedAsString
        except Exception:
            decrypted_text = "Decryption failed. Check message and key."

        # Show decrypted message back in the message text widget
        self.decrypt_message_text.delete("1.0", tk.END)
        self.decrypt_message_text.insert("1.0", decrypted_text)

########## Mix Up Random view ##########
    def _show_mixup_view(self) -> None:
        """View that encrypts and mixes up a message, returning entangled text and slice key."""
        self._clear_window()

        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        label = ttk.Label(frame, text="Mix Up Random", style="Title.TLabel")
        label.pack(pady=40)

        message_label = ttk.Label(frame, text="Message to encrypt & mix:", style="Body.TLabel")
        message_label.pack(anchor="w", padx=40)

        self.mix_message_text = tk.Text(
            frame,
            height=8,
            width=60
        )
        self.mix_message_text.pack(padx=40, pady=10, fill="x")

        mix_button = ttk.Button(
            frame,
            text="Mix up message",
            command=self._on_mixup_click,
            style="Accent.TButton",
        )
        mix_button.pack(pady=(0, 20))

        slice_label = ttk.Label(frame, text="Slice key (4 numbers):", style="Body.TLabel")
        slice_label.pack(anchor="w", padx=40)

        self.mix_slice_text = tk.Text(
            frame,
            height=2,
            width=60,
            state=tk.DISABLED,
        )
        self.mix_slice_text.pack(padx=40, pady=10, fill="x")

        # Reusable return button
        self.return_to_main_button = self._create_return_to_main_button()

    def _on_mixup_click(self) -> None:
        """Encrypt and mix up the message, showing entangled text and slice key."""
        if not hasattr(self, "mix_message_text"):
            return

        message = self.mix_message_text.get("1.0", tk.END).strip()
        if not message:
            return

        # Follow CLI 'r' flow: generate key, encrypt, then mixUpRandom
        self.encryption.setMessage(message)
        self.encryption.generateKey()
        self.encryption.encryptCls()

        entangled = self.encryption.mixUpRandom(
            self.encryption.keyAsString,
            self.encryption.encryptedAsString,
        )
        slice_key = getattr(self.encryption, "sliceKey", None)

        # Show entangled message back in the message field
        self.mix_message_text.delete("1.0", tk.END)
        self.mix_message_text.insert("1.0", entangled)

        # Show slice key as four numbers, for later decryption
        if slice_key is not None and hasattr(self, "mix_slice_text"):
            self.mix_slice_text.config(state=tk.NORMAL)
            self.mix_slice_text.delete("1.0", tk.END)
            self.mix_slice_text.insert("1.0", " ".join(str(x) for x in slice_key))
            self.mix_slice_text.config(state=tk.DISABLED)

########## Unmix Up Random view #####
    def _show_unmixup_view(self) -> None:
        """View that takes entangled text and slice key, and decrypts."""
        self._clear_window()

        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        label = ttk.Label(frame, text="Unmix Up Random", style="Title.TLabel")
        label.pack(pady=40)

        message_label = ttk.Label(frame, text="Entangled message:", style="Body.TLabel")
        message_label.pack(anchor="w", padx=40)

        self.unmix_message_text = tk.Text(
            frame,
            height=8,
            width=60
        )
        self.unmix_message_text.pack(padx=40, pady=10, fill="x")

        slice_label = ttk.Label(
            frame,
            text="Slice key (4 numbers, space or comma separated):",
            style="Body.TLabel",
        )
        slice_label.pack(anchor="w", padx=40)

        self.unmix_slice_text = tk.Text(
            frame,
            height=2,
            width=60
        )
        self.unmix_slice_text.pack(padx=40, pady=10, fill="x")

        # Button to unmix and decrypt (initially disabled)
        self.unmix_button = ttk.Button(
            frame,
            text="Unmix & decrypt",
            state=tk.DISABLED,
            command=self._on_unmixup_click,
            style="Accent.TButton",
        )
        self.unmix_button.pack(pady=(0, 10))

        # Enable/disable button when fields change
        self.unmix_message_text.bind("<<Modified>>", self._on_unmix_fields_modified)
        self.unmix_slice_text.bind("<<Modified>>", self._on_unmix_fields_modified)

        # Reusable return button
        self.return_to_main_button = self._create_return_to_main_button()

    def _on_unmix_fields_modified(self, event: tk.Event) -> None:
        try:
            event.widget.edit_modified(False)
        except Exception:
            pass

        msg = ""
        slice_text = ""
        if hasattr(self, "unmix_message_text"):
            msg = self.unmix_message_text.get("1.0", tk.END).strip()
        if hasattr(self, "unmix_slice_text"):
            slice_text = self.unmix_slice_text.get("1.0", tk.END).strip()

        if hasattr(self, "unmix_button"):
            new_state = tk.NORMAL if msg and slice_text else tk.DISABLED
            self.unmix_button.config(state=new_state)

    def _on_unmixup_click(self) -> None:
        """Unmix the entangled message using the slice key, then decrypt."""
        if not (hasattr(self, "unmix_message_text") and hasattr(self, "unmix_slice_text")):
            return

        entangled = self.unmix_message_text.get("1.0", tk.END).strip()
        slice_text = self.unmix_slice_text.get("1.0", tk.END).strip()
        if not entangled or not slice_text:
            return

        # Parse up to 4 integers from slice_text
        parts = slice_text.replace(",", " ").split()
        try:
            slice_key = [int(p) for p in parts][:4]
        except ValueError:
            slice_key = []

        if len(slice_key) != 4:
            result = "Invalid slice key. Please provide four integers."
        else:
            try:
                self.encryption.unmixUpRandom(entangled, slice_key)
                self.encryption.decryptCls()
                result = self.encryption.decryptedAsString
            except Exception:
                result = "Unmix/decrypt failed. Check message and slice key."

        self.unmix_message_text.delete("1.0", tk.END)
        self.unmix_message_text.insert("1.0", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()