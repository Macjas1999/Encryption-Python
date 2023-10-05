from cryptography.fernet import Fernet


class Input:
    def __init__(self, input):
        self.buffer = input

    def getLen(self):
        return len(self.buffer)
    

key = Fernet.generate_key()
encObj = Fernet(key)

input = input("Message: ")
input = Input(input)

encrypted = encObj.encrypt(bytes(input.buffer, 'utf-8'))
print(input.getLen())
print(encrypted)
encObj.decrypt(encrypted)
