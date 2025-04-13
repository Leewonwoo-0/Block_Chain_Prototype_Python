import string

from Crypto.Cipher import AES
from Crypto import Random
import numpy as np

secretKey128 = b'0123456701234567'
secretKey192 = b'012345670123456701234567'
secretKey256 = b'01234567012345670123456701234567'

# CBC 모드에서는 왜 Plain text가 128-bit(16byte)의 배수가 돼야 하는가. 패딩 하는 이유
# > 데이타 블록을 암호화 하는 과정에서 16바이트를 기준으로 만들어졌기 때문에 해당 연산중 값이 없으면 오류를 반환하게 됨.

#128-bit key 사용
secretKey = secretKey128
Text = b'This is Plain Text. It will be encrypt using AES with CBC mode'
print("\n\n\n원문 : ",Text, end="")

n = len(Text)
print(len(Text))
if (n%16 != 0):
    n = 16 - (n%16)
    Text = Text + b"\0"*n
#ljust 정렬은 스트링만 지원하는데 utf-8 바이트 형식으로 인코딩하면 블록 크기가 안맞음.
#바이트 하나에 문자가 하나 들어가니까 16바이트 기준. 길이가 16으로 나눠지지 않으면 바이트 추가.
#ljust > 문자열을 정렬. L > 왼쪽 정렬 R 오른쪽 정렬. n만큼 정렬, 빈칸은 오른쪽 값으로 채우기. 다만 전부 널값으로 들어가서
#원래 마지막 값이 문항에서 널값이었을 때 오류가 발생할 수 있음.

#str왼쪽정렬 값추가가 아닌. 함수값을 Byte값으로 설정하고 빈자리 수만큼 Null값 넣어주기.


#iv를 왜 수신자한테 보내야되나?
#수신자 또한 암호화 AES(복호화 계산)을 해야함. 그러기 위해 난 함수를 이용하기 떄문에
#변수 선언을 해서 암호화 연산 변수를 만들어 준 것.
#해당 변수를 만들 때 iv값(initialization Vector)가 있어야지 체인 연결 초기값을 구할 수 있어서 필요?
#아니 근데 애초에 iv값이 무작위 비트열로 만들어지는데 이걸로 암호화를 하고 체인 형식으로 AES가 연결되서 암호화되는데
#iv값을 모르면 복호화 자체가 안되네. 그래서 연산자체 만들 때 필요한 것.

iv = Random.new().read(AES.block_size)
#numpy Numeriy Python의 준말으로 수학분야 관련된 통계나 연산작업시 사용하는 라이브러리
#과학계산 컴퓨팅과 수학적인 데이터분석에 필요한 기본적인 패키지 파이썬의 리스트와 유사하지만 메모리 효율성이 높아
#성능적인 측면에서 우위에 있음.

#암호화

ivcopy = np.copy(iv)

aes = AES.new(secretKey, AES.MODE_CBC, iv)

cipherText = aes.encrypt(Text)
# 바이트형식이 아니라는거 같은데. CBC형식으로 암호화 하는데 str 타입은 C 코드로 변환될 수 없습니다?
# 아니 애초에 코드가 좀 잘못된게 누가 바이트형식만 지원하는 AES_CBC 암호화 코드를 스트링만 지원하는 ljust를 써서 열을맞춰


print("\n\n\n암호문 : ",cipherText.hex(), end="")
#hex() > 16진수 변환

## 복호화
aes = AES.new(secretKey, AES.MODE_CBC, iv) # 왜 넘파이로 복사를 쳐한거임? a=b 하게되면 변수데이터값 두개저장인가? 포인터형식 데이터지정인가.
#np.copy 는 배열의 새로운 주소를 할당하여 복사하는 것. 즉 새로운 배열 생성
#a=b[] 일 경우 포인터 주소값을 저장하게 되기 때문. 파이썬 포인터 복습 필요.
#내가 알기론 변수 데이터값 지정인데.
#Text_2 = ("%(Text)s" %Text_2) 포맷은 지원안해주는듯? 개수지정이랑 같이 선언하는거 알아보긴 해야됨.
#len_Text =len(Text)
Text_2 = aes.decrypt(cipherText)

#Text_2 = Text_2 >= n*8 비트연산자는 bytes 랑 int가 지원을 안해주네
#Text_2 = Text_2 <= n*8

#문자열 길이설정으로 해결 할만하다.

Text_2 = Text_2[:len(Text_2)-n]
Text_2 = Text_2.decode()

print("\n\n\n복호화 값 :%s"%(Text_2) ,"\n문자열 길이=" ,len(Text_2), end="")


# 비트연산자 말고 좀 더 괜찮은 게 있을 것 같은데 흠
# >> 해결 (슬라이싱) [:]


# 문자열 > 바이트 (encode) 바이트 > 문자열 (decode)
# incode를 해준적 없는데? 그리고 AES 암호화는 비트형식만 계산이 가능한데
# 비트 형식으로 변환을 안함.

#바이트 연산에서 공간없는 쪽으로 밀리면 사라지나?

#Debug
#code21 1차 디버깅.
# 플레인 텍스트에 대한 연산코드가 하나 잘못됨.

#2차 디버깅
# ljust 는 str 정렬코드. AES 암호화 방식은 바이트 형식만 지원 Str으로 데이터 값 정렬해서 128로 맞춰도 바이트 형식이 아니라 안됨.
#애초에 Byte 형식으로 입력값 수정 > ljust 정렬말고 그냥 데이터 값을 16으로 나눈 나머지값 만큼 널 값을 추가함.
#바이트 형식 연산에 널 값을 추가한 것. 그래서 AES 암호화가 가능해짐.

#3차 디버깅
#복호화 출력값에 널값이 포함되어있음. 널 값을 제거 후 출력하기 위해. Format, 비트연산자, 슬라이싱.
#1. 포맷의 경우 변수를 넣어서 문자열의 크기를 맞추는걸 지원하지 않았음 > 실패
#2. 비트연산자. 바이트 크기를 빼서 연산하려고 했지만 바이트 형식과 인트(정수형) 형식은 지원하지 않음. 8bit = 1byte
#3. 슬라이싱을 통해 문자열(배열)의 크기를 설정하여 잘라낼 수 있었음. 슬라이싱 하면 문자열 길이도 감소함.
