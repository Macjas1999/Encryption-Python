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


while True:
    print('Choose what you want to do:\n\tTo encrypt message input \'e\'\n\tTo decrypt message input \'d\'\n\tTo exit input \'x\'')
    use = input()
    match use:
        case "e":
            mainEncryptionObj = Enctrypton()
            hasKey = input("If you want to generate new key input \'gen\', or if you have key copy it below:\n")
            if(hasKey == "gen"):
                mainEncryptionObj.generateKey()
                print(mainEncryptionObj.getKeyDecoded())
                print(len(mainEncryptionObj.getKeyDecoded()))
                inputObj = Input(input("Message: "))
                mainEncryptionObj.setMessage(inputObj.buffer)
                mainEncryptionObj.encryptCls()
                print(mainEncryptionObj.decodeEncrypted())
                print(len(mainEncryptionObj.decodeEncrypted()))
                part1 = mainEncryptionObj.getKeyDecoded()
                part2 = mainEncryptionObj.decodeEncrypted()
                toSend = mainEncryptionObj.mixUp(part1, part2)
                print(toSend)
                mainEncryptionObj.__del__()

            elif(len(hasKey) == 44):
                mainEncryptionObj.setKey(bytes(hasKey, 'utf-8'))
                print('Key has been set correctly')
                inputObj = Input(input("Message: "))
                mainEncryptionObj.setMessage(inputObj.buffer)
                mainEncryptionObj.encryptCls()
                print(mainEncryptionObj.decodeEncrypted())
                #print(len(mainEncryptionObj.decodeEncrypted()))
                mainEncryptionObj.__del__()

            else:
                print("Input is incorrect\n")

        case "d":
            mainEncryptionObj = Enctrypton()
            inputObj = Input(input("Message: "))
            mainEncryptionObj.unmixUp(inputObj.buffer)
            mainEncryptionObj.decryptCls()
            print(mainEncryptionObj.decrypted)

        case "x":
            break


# inputObj = Input(input("Message: "))
# encryprionObj = Enctrypton(inputObj.buffer)
# encryprionObj.generateKey()
# encMessage = encryprionObj.encryptCls()
# print(encMessage)

# decryptionObj = Enctrypton(encMessage)
# decryptionObj.setKey(encryprionObj.getKey())
# decMessage = decryptionObj.decryptCls()
# print(decMessage)



# #Testing code. Temporary
# key = Fernet.generate_key()
# encObj = Fernet(key)

# input = input("Message: ")
# input = Input(input)

# encrypted = encObj.encrypt(bytes(input.buffer, 'utf-8'))
# print(input.getLen())
# print(encrypted)
# encObj.decrypt(encrypted)
