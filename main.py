from cryptography.fernet import Fernet
import random
 
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


while True:
    print('Choose what you want to do:\n\tTo encrypt message input \'e\'\n\tTo decrypt message input \'d\'\n\tTo exit input \'x\'')
    use = input()
    match use:
        case "e":
            mainEncryptionObj = Enctrypton()
            print('For encryption with separate key press \'s\' if you want to entangle key and message input \'e\' if you want to encrypt message with random slice key input \'r\'')
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
                case 'r':
                    mainEncryptionObj.generateKey()
                    inputObj = input("Message: ")
                    mainEncryptionObj.setMessage(inputObj)
                    mainEncryptionObj.encryptCls()
                    entangled = mainEncryptionObj.mixUpRandom(mainEncryptionObj.keyAsString, mainEncryptionObj.encryptedAsString)
                    print("Your encrypted message: \n" + entangled + "\n" + "Slice key: " + str(mainEncryptionObj.sliceKey) + "\n")

        case "d":
            mainEncryptionObj = Enctrypton()
            print('For decryption with separate key press \'s\' if you have one entangeled message input \'e\' if you have one entangeled message with random slice key input \'r\'')
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

                case 'r':
                    inputObj = input("Message: ")
                    sliceKey = []
                    for i in range(4):
                        sliceKey.append(int(input("Slice key: ")))
                    mainEncryptionObj.unmixUpRandom(inputObj, sliceKey)
                    mainEncryptionObj.decryptCls()
                    print("Your decrypted message: \n" + mainEncryptionObj.decryptedAsString + "\n")
                    mainEncryptionObj.__del__()

        case "x":
            break