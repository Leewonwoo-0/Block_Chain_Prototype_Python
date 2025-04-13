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
#의문점 1. cipherText는 왜 0번째 배열로 출력하는 것 인가?
#    생각. 텍스트를 암호화 할 때 RSA 규칙성을 가지고 배열을 통해 연산하기 때문.
#의문점 2. 암호화된 텍스트는 encode 되고 암호화 됐으니 바이트 형식인가?
#    생각. RSA암호화가 지원하는 형식으로 데이터를 입력하기 위해 encode() 한 것이기에 바이트로 전환해준 것.
#의문점 3. 암호화 하는데 10은 무슨값?
# 모르겠음; 그냥 내 생각으로 설명을 하면 암호화 할 때 연산횟수 이런거 아닐까?

print("\n암호화된 텍스트:",cipherText[0].hex())

key = RSA.importKey(privKey)
decryptText = privKey.decrypt(cipherText)
plainText = decryptText.decode()

print("복호화된 텍스트:", plainText)

