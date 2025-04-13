from Crypto.PublicKey import RSA

keyPair = RSA.generate(2048)
privKey = keyPair.exportKey()
pubKey = keyPair.publickey()

keyObj = RSA.importKey(privKey)

print("p=", keyObj.p)
print("q=", keyObj.q)
print("e=", keyObj.e)
print("d=", keyObj.d)

plainText = "This is encrypted by using RSA"
print("\n원문: %s"%plainText)

cipherText = pubKey.encrypt(plainText.encode(), 10)

print("\n암호화된 텍스트:",cipherText[0].hex())

key = RSA.importKey(privKey)
decryptText = privKey.decrypt(cipherText)
plainText = decryptText.decode()

print("복호화된 텍스트:", plainText)

