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


while True:
    print('Choose what you want to do:\n\tTo encrypt message input \'e\'\n\tTo decrypt message input \'d\'\n\tTo exit input \'x\'')
    use = input()
    match use:
        case "e":
            mainEncryptionObj = Enctrypton()
            print('For encryption with separate key press \'s\' if you want to entangle key and message input \'e\'')
            method = input()
            match method:
                case 's':
                    hasKey = input("If you want to generate new key input \'gen\', or if you have key copy it below:\n")
                    if(hasKey == "gen"):
                        mainEncryptionObj.generateKey()
                        print("Your key is: " + mainEncryptionObj.getKey('s'))
                        inputObj = input("Message: ")
                        mainEncryptionObj.setMessage(inputObj)
                        mainEncryptionObj.encryptCls()
                        print("Your encrypted message: \n" + mainEncryptionObj.encryptedAsString + "\n")
                        mainEncryptionObj.__del__()

                    elif(len(hasKey) == 44):
                        mainEncryptionObj.setKey(hasKey)
                        print('Key has been set correctly')
                        inputObj = input("Message: ")
                        mainEncryptionObj.setMessage(inputObj)
                        mainEncryptionObj.encryptCls()
                        print("Your encrypted message: \n" + mainEncryptionObj.encryptedAsString + "\n")
                        mainEncryptionObj.__del__()

                    else:
                        print("Input is incorrect\n")
                case 'e':
                    mainEncryptionObj.generateKey()
                    inputObj = input("Message: ")
                    mainEncryptionObj.setMessage(inputObj)
                    mainEncryptionObj.encryptCls()
                    entangled = mainEncryptionObj.mixUp(mainEncryptionObj.keyAsString, mainEncryptionObj.encryptedAsString)
                    print("Your encrypted message: \n" + entangled + "\n")

        case "d":
            mainEncryptionObj = Enctrypton()
            print('For decryption with separate key press \'s\' if you have one entangeled message input \'e\'')
            method = input()
            match method:
                case 's':
                    hasKey = input("Enter your key: ")
                    mainEncryptionObj.setKey(hasKey)
                    print('Key has been set correctly')
                    inputObj = input("Message: ")
                    mainEncryptionObj.setMessage(inputObj)
                    mainEncryptionObj.decryptCls()
                    print("Your decrypted message: \n" + mainEncryptionObj.decryptedAsString + "\n")
                    mainEncryptionObj.__del__()

                case 'e':
                    inputObj = input("Message: ")
                    mainEncryptionObj.unmixUp(inputObj)
                    mainEncryptionObj.decryptCls()
                    print("Your decrypted message: \n" + mainEncryptionObj.decryptedAsString + "\n")
                    mainEncryptionObj.__del__()

        case "x":
            break