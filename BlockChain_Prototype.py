import time
import hashlib
import base64
import random

class NodeBlock:
    def __init__(self, index, time, data):
        self.index = index
        self.time = time
        self.data = data
        self.previousHash = 0
        self.nonce = 0
        self.usageTime = 0
        self.private_hash = 0
        self.difficulty = self.set_difficulty()
        self.chain_data = []
        self.hash = self.calHash()
        self.genessisBlock = self.CreateGenessis()

    def set_difficulty(self):
        self.difficulty = 3
        if self.usageTime < 20:
            self.difficulty += 1
        elif self.usageTime <= 0:
            self.difficulty = 3
        else:
            if (self.difficulty > 0):
                self.difficulty -= 1
        return self.difficulty

    def calHash(self):
        return hashlib.sha256(str(self.private_hash).encode() + str(self.data).encode() + str(self.index).encode()+
                              str(self.time).encode() + str(self.previousHash).encode() + str(self.nonce).encode()).hexdigest()

    def mine(self):
        self.nonce = 0
        self.difficulty = self.set_difficulty()
        self.previousHash = self.chain_data[len(self.chain_data)-1][0]

        start = time.time()
        res = ["0"] * self.difficulty
        result = "".join(res)
        while(str(self.hash)[:self.difficulty]!=result):
            self.nonce += 1
            self.hash = self.calHash()
        end = time.time()
        self.usageTime = end - start
        self.chain_data.append([0]*8)

        # hash, data 값의 해쉬값이 일치하다면 위의 해쉬값과 블록체인 연결 #mine 외의 유효성 검증 함수 만들어야될수도 제네시스 블럭 만드는거랑 연계되는 오류사항 봐야함.

        self.chain_data[len(self.chain_data)-1][0] = self.hash  # 제네시스 블럭에도 2차원 배열 선언해서 저장 해야되네
        self.chain_data[len(self.chain_data)-1][1] = self.private_hash
        self.chain_data[len(self.chain_data)-1][2] = self.data
        self.chain_data[len(self.chain_data)-1][3] = self.index
        self.chain_data[len(self.chain_data)-1][4] = self.time
        self.chain_data[len(self.chain_data)-1][5] = self.previousHash
        self.chain_data[len(self.chain_data)-1][6] = self.nonce
        self.chain_data[len(self.chain_data)-1][7] = 1 #1 utxo(un spend transaction)

        return self.hash

    def CreateGenessis(self):
        #제네시스 블럭을 자체적으로 생산하는게 맞지.
        self.index = 1
        self.time = time.time()
        self.data = 0
        self.previousHash = 0
        self.nonce = 0
        self.hash = hashlib.sha256(str(self.private_hash).encode() + str(self.data).encode() + str(self.index).encode() +
                                   str(self.time).encode() + str(self.previousHash).encode() +
                                   str(self.nonce).encode()).hexdigest()

        self.chain_data.append([0]*8)
        #self.chain_data += [[0]*8]
        # 제네시스 블럭 생성하는 거에서 클래스를 분류 해야되네, 메인 노드랑 채굴 클래스랑 다르게. 메인 비트코인 자체에 채굴 데이터를 입력할 수 있게 함수를 만들 수는 있는데 좀 복잡해질듯
        # 할 필요 없다 트랜잭션 양에 0으로 맞춰서 제네시스 블럭 생성하면됨.
        self.chain_data[len(self.chain_data) - 1][0] = self.hash  # 제네시스 블럭에도 2차원 배열 선언해서 저장 해야되네
        self.chain_data[len(self.chain_data) - 1][1] = self.private_hash
        self.chain_data[len(self.chain_data) - 1][2] = self.data
        self.chain_data[len(self.chain_data) - 1][3] = self.index
        self.chain_data[len(self.chain_data) - 1][4] = self.time
        self.chain_data[len(self.chain_data) - 1][5] = self.previousHash
        self.chain_data[len(self.chain_data) - 1][6] = self.nonce
        self.chain_data[len(self.chain_data) - 1][7] = 1  # 1 utxo(un spend transaction)
        return self.hash
    def New_utxo(self, Personal_key, data, nonce_1, nonce_2, time_1, time_2, hash_1, hash_2, private_hash):
        #개인키 암호화 - > 검증 PASS
        #송신자 트랜잭션 검증은 데이터 값만 최신화 해서 해쉬 암호화 해주면 됨.
        print("채굴자로 전달받은 트랜잭션 검증중. . .")

        Check_ad = base64.b64encode(bytes(Personal_key, 'utf-8'))
        Hash_result = hashlib.sha256()
        Hash_result.update(Check_ad)
        Personal_key = Hash_result.hexdigest()
        address_num = 0

        #코인 개인키 값 검증, 보유량 검증.
        print("개인키 검증. . .")
        for s in range(len(self.chain_data)):
        # (일단 개인키랑 공개키 주솟값이랑 일치함. 그렇단 뜻은 배열의 수가 잘못됐다는 뜻인데. 로테도 정확히 배열 수만큼 돌아감.
        #    personal_key encode 되고 아래 인코딩 된 값이랑  sha256 해쉬 암호화 16진수 변환하면 일치해야되는데
        #    일치하지 않는다는것은 일단 아래 str(chain_data 값이 제대로 입력이 안됐다는건데)
        #프리비오스 해쉬값이랑 일치하는지 확인하기 위해서 이렇게 확인 할 필요가 있네.
            address_data = hashlib.sha256(str(Personal_key).encode() +
                                          str(self.chain_data[len(self.chain_data) - (s + 1)][2]).encode() +
                                          str(self.chain_data[len(self.chain_data) - (s + 1)][3]).encode() +
                                          str(self.chain_data[len(self.chain_data) - (s + 1)][4]).encode() +
                                          str(self.chain_data[len(self.chain_data) - (s + 1)][5]).encode() +
                                          str(self.chain_data[len(self.chain_data) - (s + 1)][6]).encode()).hexdigest()
            if address_data == self.chain_data[len(self.chain_data)-(s+1)][0]:
                address_num = len(self.chain_data)-(s+1)
                break
            #for v in range(len(self.chain_data)):
            #    if address_data == self.chain_data[len(self.chain_data)-(v+1)][0]:
            #        address_num = len(self.chain_data)-(v+1)
        aa=0
        if address_num == 0:
            print("개인키 검증 실패")
        if address_num != 0:
            print("개인키 검증 성공")
            print("코인 보유량 검증. . .")
            if self.chain_data[address_num][2] >= float(data) + float(0.004):
                print("코인 보유량 검증 완료")
                aa = 1
        #트랜잭션 난이도 검증
        res = ["0"] * self.difficulty
        res = "".join(res)
        #채굴자 전달 트랜잭션 검증
        if aa == 1:
            self.index = len(self.chain_data)
            self.time = time_1
            self.data = float(self.chain_data[address_num][2]) - (float(data) + 0.004)
            self.previousHash = self.chain_data[len(self.chain_data)-1][0]
            self.nonce = nonce_1
            self.private_hash = Personal_key
            self.hash = self.calHash()

            if self.hash == hash_1 and self.hash[:self.difficulty] == res:
                    print("채굴자로 전달받은 송신자 트랜잭션 검증 완료")
                    self.chain_data.append([0] * 8)
                    self.chain_data[len(self.chain_data) - 1][0] = self.hash
                    self.chain_data[len(self.chain_data) - 1][1] = self.private_hash
                    self.chain_data[len(self.chain_data) - 1][2] = self.data
                    self.chain_data[len(self.chain_data) - 1][3] = self.index
                    self.chain_data[len(self.chain_data) - 1][4] = self.time
                    self.chain_data[len(self.chain_data) - 1][5] = self.previousHash
                    self.chain_data[len(self.chain_data) - 1][6] = self.nonce
                    self.chain_data[len(self.chain_data) - 1][7] = 1



                    print("송신자 트랜잭션 연결 완료")
                    address_num_recive = 0
                    self.private_hash = private_hash
                    self.index = len(self.chain_data)
                    self.time = time_2
                    self.previousHash = self.hash
                    self.nonce = nonce_2
                    for send in range(len(self.chain_data)):
                        if self.chain_data[len(self.chain_data)-(send+1)][1] == self.private_hash:
                            address_num_recive = len(self.chain_data)-(send+1)
                            break


# difficulty 값에 일치하는 난이도값으로 생성했는지 확인 필요
                    if address_num_recive == 0:
                        self.data = data
                        self.hash = self.calHash()
                        if self.hash == hash_2 and self.hash[:self.difficulty] == res:
                            print("O.수신자 트랜잭션 검증 완료")
                            self.chain_data.append([0] * 8)
                            self.chain_data[len(self.chain_data) - 1][0] = self.hash
                            self.chain_data[len(self.chain_data) - 1][1] = self.private_hash
                            self.chain_data[len(self.chain_data) - 1][2] = self.data
                            self.chain_data[len(self.chain_data) - 1][3] = self.index
                            self.chain_data[len(self.chain_data) - 1][4] = self.time
                            self.chain_data[len(self.chain_data) - 1][5] = self.private_hash
                            self.chain_data[len(self.chain_data) - 1][6] = self.nonce
                            self.chain_data[len(self.chain_data) - 1][7] = 1


                            print("O.수신자 트랜잭션 생성 완료")
                    if address_num_recive != 0:
                        if self.private_hash == self.chain_data[address_num_recive][1]:
                            self.data = float(self.chain_data[address_num_recive][2]) + float(data)
                            self.hash = self.calHash()
                            if self.hash == hash_2 and self.hash[:self.difficulty] == res:
                                print("N.수신자 트랜잭션 검증 완료")
                                self.chain_data.append([0] * 8)
                                self.chain_data[len(self.chain_data) - 1][0] = self.hash
                                self.chain_data[len(self.chain_data) - 1][1] = self.private_hash
                                self.chain_data[len(self.chain_data) - 1][2] = self.data
                                self.chain_data[len(self.chain_data) - 1][3] = self.index
                                self.chain_data[len(self.chain_data) - 1][4] = self.time
                                self.chain_data[len(self.chain_data) - 1][5] = self.previousHash
                                self.chain_data[len(self.chain_data) - 1][6] = self.nonce
                                self.chain_data[len(self.chain_data) - 1][7] = 1

                                print("N수신자 트랜잭션 생성 완료")

        #hash_address = self.chain_data[array_num][0]
        #eco = self.chain_data[array_num][1]
        #send_address_num = 0
        #for a in range(len(self.chain_data)):
        #    if self.chain_data[len(self.chain_data)-(a+1)] == send_address:
        #        send_address_num = len(self.chain_data)-(a+1)

        #if send_address_num == 0:
        #    self.index = len(self.chain_data)+1
        #    self.time = time.time()
        #    self.data = recive_data
        #    self.mine()
        #        #새로운 트랜잭션 생성
        #else:

        # data 검증하는 과정 생략하니까 데이터 값을 못받아오네. 이거 검증과정 만들어야겠네.
        # 일단 만들고 오류 수정하고 만들자.

        #검증 절차에서 원래 데이터 값에서 바뀌는 데이터 값을 저장. New_utxo에 둘다 받아와야되네.
        #UTXO 생성, 추가 절차.

        #전송자는 그냥 coin_data - fee 해서 만들면 되는데
        #수신자는 UTXO 찾아서 넣어야되는데

        #UTXO 찾아서 1인거 찾아서 풀기엔 보안성이 떨어짐.
    def New_transaction(self, personal_address):
        Check_ad = base64.b64encode(bytes(personal_address,('utf-8')))
        Hash_result = hashlib.sha256()
        Hash_result.update(Check_ad)
        Check_ad = Hash_result.hexdigest()
        print("입력한 개발보상 개인키에 대한 공개키 주솟값: ", Check_ad)
        ck = 0
        for aaa in range(len(self.chain_data)-1):
            if self.chain_data[len(self.chain_data)-(aaa+1)][1] == Check_ad:
                ck = 1
                break

        if ck == 0:
            self.index = len(self.chain_data)
            self.time = time.time()
            self.data = random.randint(1,100)
            self.previousHash = self.chain_data[len(self.chain_data)-1][0]
            self.nonce = 0
            self.private_hash = Check_ad
            Check_ad = hashlib.sha256(str(self.private_hash).encode() + str(self.data).encode() +
                                      str(self.index).encode() + str(self.time).encode() +
                                      str(self.previousHash).encode() + str(self.nonce).encode()).hexdigest()
            print("입력한 개발보상 개인키에 대한 체인 주솟값: ", Check_ad)
            self.chain_data.append([0]*8)
            self.chain_data[len(self.chain_data) - 1][0] = Check_ad
            self.chain_data[len(self.chain_data) - 1][1] = self.private_hash
            self.chain_data[len(self.chain_data) - 1][2] = self.data
            self.chain_data[len(self.chain_data) - 1][3] = self.index
            self.chain_data[len(self.chain_data) - 1][4] = self.time
            self.chain_data[len(self.chain_data) - 1][5] = self.previousHash
            self.chain_data[len(self.chain_data) - 1][6] = self.nonce
            self.chain_data[len(self.chain_data) - 1][7] = 1
        if ck == 1:
            print("이미 생성된 개인키 값이므로 새로운 개발 보상 트랜잭션 생성이 불가능합니다.")

class Mine:
    def __init__(self, time, data, Privacy_key, difficulty, chain_data,transaction_address, private_hash):
        self.time = time
        self.data = data
        self.difficulty = difficulty
        self.chain_data = chain_data
        self.transaction_address = transaction_address
        self.Check_Privacy_key = Privacy_key
        self.index = 0
        self.nonce = 0
        self.hash_result = 0
        self.Previous_Hash = 0
        self.hash_1 = 0
        self.hash_2 = 0
        self.send_data = 0
        self.array_num = 0
        self.nonce_1 = 0
        self.nonce_2 = 0
        self.time_1 = 0
        self.time_2 = 0
        self.private_hash = 0
        self.recive_data = 0
        self.private_hash_2 = private_hash
        self.hash = self.calHash()
    #       self.get_Chain()
    #       chain_data[num][0]

    #    def get_Chain(self):
    #        self.Previous_Hash =
    #        #센드 어드레스값의 previous 해쉬값.
    def calHash(self):
        return hashlib.sha256(str(self.private_hash).encode() + str(self.data).encode() +
                              str(self.index).encode() + str(self.time).encode()+ str(self.Previous_Hash).encode() +
                              str(self.nonce).encode()).hexdigest()

    def mine(self):
        #난이도에 따른 검증절차 필요함. 메인노드에서. 근데 난이도가 지속적으로 최신화 되고있나? 함수선언이? 그게 아님.#수정완료
        res = ["0"] * self.difficulty
        result = "".join(res)
        #데이터 값 입력
        #hash_address = self.chain_data[array_num][0]
        #eco = self.chain_data[array_num][1]
        #send_address_num = 0
        #for aa in range(len(self.chain_data)):
        #    if self.chain_data[len(self.chain_data) - (aa + 1)] == send_address:
        #        send_address_num = len(self.chain_data) - (aa + 1)
        #        break
        #if send_address_num == 0:
        #    self.index = len(self.chain_data)
        #    self.time  = time.time()
        #    self.hash = 1
        #    while (str(self.hash)[:self.difficulty] != result):
        #        self.nonce += 1
        #        self.hash = self.calHash()
        #    self.hash = hashlib.sha256(str(self.hash).encode + str(self.chain_data[len(self.chain_data)]).encode).hexdigest()
        #위에 꺼까진 받는사람 트랜잭션 해쉬 생성.

        #송신자 트랜잭션 생성
        self.index = len(self.chain_data)
        self.time = time.time()
        self.time_1 = self.time
        self.recive_data = self.data
        self.data = float(self.chain_data[self.array_num][2]) - (float(self.data) + 0.004)
        self.nonce = 0
        self.Previous_Hash = self.chain_data[len(self.chain_data)-1][0]
        self.private_hash = self.chain_data[self.array_num][1]
        self.hash = self.calHash()
        print("채굴 시작. . .")
        while self.hash[:self.difficulty] != result:
            self.nonce += 1
            self.hash = self.calHash()
            #print(self.hash)
        self.hash_1 = self.hash
        self.nonce_1 = self.nonce
        print("송신자 트랜잭션 생성 성공. \n")
        #수신자 트랜잭션 생성
        self.Previous_Hash = self.hash
        self.index = len(self.chain_data)+1
        self.time = time.time()
        self.time_2 = self.time
        self.private_hash = self.private_hash_2
        self.nonce = 0
        for bb in range(len(self.chain_data)):
            if self.chain_data[len(self.chain_data)-(bb+1)][1] == self.private_hash:
                self.hash_2 = len(self.chain_data)-(bb+1)
                break


        send_address_num = self.hash_2
        if send_address_num == 0:
            print("신규 지갑으로의 코인 전송")
            #지갑 X
            self.data = self.recive_data
            self.hash_2 = self.calHash()
            while self.hash_2[:self.difficulty] != result:
                self.nonce += 1
                self.hash_2 = self.calHash()
            self.nonce_2 = self.nonce
            print("신규 지갑으로의 트랜잭션 생성 성공 \n")
        if send_address_num != 0:
            #지갑 O
            print("트랜잭션 지갑으로의 코인 전송")
            self.data = float(self.recive_data) + float(self.chain_data[send_address_num][2])
            self.hash_2 = self.calHash()
            while self.hash_2[:self.difficulty] != result:
                self.nonce += 1
                self.hash_2 = self.calHash()
            self.nonce_2 = self.nonce
            print("수신자 트랜잭션 생성 성공. \n")

        # difficulty 선언이 트랜잭션 붙이면 달라질텐데.
        # difficulty 를 설정해주는 코드를 선언해서 다음 트랜잭션에 다시 받아 올 필요가 있네.
        # 그러려면 자체적인 노드에서의 트랜잭션 시간에 대한 활성화를 시켜야함.
        # 노드 자체에서 시간 활성화, 트랜잭션 생성시간 받아오고
        # 트랜잭션 생성 시간에 따른 블럭 난이도 설정. + 하지만 이 트랜잭션은 하나를 만드는거니까
        # 기존 비트코인은 머클트리 구조니까 이렇게 만들고 머클트리 형식으로 변환 시켜보자 그게 맞다.


        #수신자 array num 구해서 신규 트랜잭션인지, 기존에 보유량이 있는지 찾고 데이터에 입력.
        # 해쉬값이랑 데이터 값 둘다 저장 후 해쉬값 생성된 걸로 메인노드에 전송.
        #메인노드는 전송된 결과값을 2차적 검증 절차(직접해슁 후 결과값 비교 (전자서명)) 이후
        #블록체인 내부에 연결. 끝



    #        else:
    #            self.index = len(self.chain_data)
    #            self.time = time.time()
    #            self.data = self.data + self.chain_data[send_address_num][1]
    #            self.hash = 1
    #            while (str(self.hash)[:self.difficulty] != result):
    #                self.nonce += 1
    #                self.hash = self.calHash()
    #            self.hash = hashlib.sha256(str(self.hash).encode + str(self.chain_data[len(self.chain_data)]).encode).hexdigest()
    #저장 전 검증절차 도입해야함. 메인노드로 채굴자의 전송이 있을 때 검증과정이 있어야 하기 때문.
    def Check_address(self): # 주소, 개수 검증
        Check_ad = base64.b64encode(bytes(self.Check_Privacy_key, ('utf-8')))
        Hash_result = hashlib.sha256()
        Hash_result.update(Check_ad)
        self.Check_Privacy_key = Hash_result.hexdigest()
        for s in range(len(self.chain_data)):
            if self.chain_data[len(self.chain_data)-(s+1)
            ][1] == self.Check_Privacy_key:
                self.array_num = len(self.chain_data)-(s+1)
                break

        # previous hash 구하는 연산 해야되네 직접연산해야되나?
        # 1. for문 데이터 직접연산
        self.check = 0
        if self.array_num != 0:
            print("#################################################")
            print("입력한 개인키에 대한 공개키 주소값: ", self.Check_Privacy_key)
            print("공개키 일치 트랜잭션 확인 index:", self.chain_data[self.array_num][3])
            self.check = 1
            if self.chain_data[self.array_num][2] >= float(self.data) + 0.004:
                self.check = 2
                if self.chain_data[self.array_num][7] == 1:
                    self.check = 3

        if self.array_num == 0:
            print("개인키 검증 실패")
        if self.check == 1:
            print("코인 보유량 부족")
        if self.check == 2:
            print("UTXO검증 실패")
        if self.check == 3:
            print("개인키 검증 성공")
            self.mine()


#        for aa in range(len(self.chain_data)): # 이중 if문으로 줄일 수 있지않나?
#            if self.chain_data[len(self.chain_data)-(aa+1)][0] == self.transaction_address:
#                self.check = 1
#                if self.chain_data[len(self.chain_data)-(aa+1)][1] >= float(self.data) + 0.004:
#                    #if self.chain_data[len(self.chain_data)-a][1] >= self.transaction:
#                    self.check = 2
#                    if self.chain_data[len(self.chain_data) - (aa+1)][2] == 1:
#                        self.check = 3
#                        self.array_num = len(self.chain_data) - (aa+1)
#                        break
            #UTXO 검증
            #if self.chain_data[len(self.chain_data)-a][3] = 1:
            #if self.chain_data[len(self.chain_data)-a][3] = 0:

            # hash 값 만들고 previous hash랑 합쳐서 해쉬로 검증 근데 그러면
            #previous hash랑 합쳐진 블록의 주솟값이랑 검증해야되는데
            #트랜잭션 만들기 함수 선언 a= self.함수이름 함수에선 리턴값으로 배열 리턴
            #리턴된 배열값 노드 함수 선언? 노드 검증절차 > 난이도값 일치시 추가

            #make utxo 함수에선 previous 함수랑 전송 데이터값에 따른 새로운 코인 보유량
            #배열에 저장해서 트랜잭션 두개 만들기.
            #그 후 배열값 리턴(이중포인터 나중에 사용해보기)
            #리턴한 배열값에 따른 메인노드의 검증과정 이후 연결

            #    self.chain_data[len(self.chain_data)-a][3] = 1
    #def makeUTXO(self, array_num):

#        save_utxo = [] 배열로 할 수 있는데 포인터 사용해야되서 최적화된 방법은 아닌듯? 이건 컴퓨터 구조학 보고 최적화 시켜야될듯.
#time, data, send_address,Privacy_key, difficulty
        #여기서 마이닝 작업하고, 넌스값 + 주솟값 + 번호에 따른 해쉬값이 일치하는지 확인 후 붙이는 검증과정

        #self.Check_Privacy_key # 주솟값
        #if self.chain_data[array_num][1] >= self.data + 0.004:#0.004는 기본 수수료
        #    self.mine()
        #if self.chain_data[array_num][1] <  self.data + 0.004:
        #    print("보유 코인 개수 부족")
            #New_utxo 함수에선 트랜잭션 번호와, 수신자 트랜잭션 주소, 전송량

            # 사실 여기서 root 권한 느낌으로 함수선언에 추가할 수 있으면 안되는데 전송 개념이 아니니까
            # 아니네 애초에 New_utxo 함수 선언 자체가 검증 위해서 선언하는거니까 Miner 클래스에서 함수선언 권한을
            # New_utxo만 가능하게 하면 되네


            #Utxo_2 = a.New_utxo(self.chain_data[array_num][0], self.recive_data) # 수신자
            #아니다 a가 메인이니까 a의 특정 함수 선언을 통해 연쇄적 함수선언이 되게 해서 검증과정 거친 후에 a의 배열에 추가되야되네.

        # index, time, data
        # index, time, data, transaction, difficulty

a = NodeBlock(1, time.time(), 0)
while 1:
    select = int(input("\n블록체인 명령어 \n1. 블록체인 확인 2. 코인 송신 3. 개발 보상 트랜잭션 생성 4. 종료\n 입력 : "))

    if select == 1:
        for aa in range(len(a.chain_data)):
            print("\nindex =", aa)
            for bb in range (8):
                print(a.chain_data[aa][bb])

    if select == 2:
        Personal_key = input("\n개인키 입력:")
        transaction_address = input("\n개인키 트랜잭션 주소 입력:")
        data = input("\n보낼 코인 개수 입력:")
        private_hash = input("\n보낼 코인 지갑 공개키 주소 입력:")
        b = Mine(time.time(), data, Personal_key, a.set_difficulty(),
                 a.chain_data, transaction_address, private_hash)
        b.Check_address()
        transaction_send = b.hash
        transaction_recive = b.hash_2
        if b.check == 3:
            a.New_utxo(Personal_key, b.recive_data, b.nonce_1, b.nonce_2,
                       b.time_1, b.time_2, b.hash_1, b.hash_2, private_hash)
            #함수 여러번 선언하면 difficult 값이 달라야 하고 메인노드에서 일치성 확인해야됨.
            #근데 채굴자 노드가 애초에 다른사람들한테 트랜잭션 값 전달받아서 하는 구조지
            #이게 함수로 다른 구조로 만들 수 있나?
            #디피컬트 설정함수를 선언하면 지속적으로 최신화 데이터를 넣을 수 있음.
            #근데 다만 메인노드에 디피컬티 검증노드를 구현해야함.

            #개발 보상 데이터 해쉬 개인키 중첩 안되게 설정해야함. 메인노드 권한에서 생성하는 거라 막을수가 없다.
            #이것도 개인키 중첩되면 생성 x 로 막을 수 있긴함. # 수정 완료

            #한번 사용한 해쉬 트랜잭션의 재사용 여부를 공개키 가 있으면 확인해서 못하도록 해야함.
            #아니면 실제로 배열7번 UTXO 여부를 바꿔주던가
            #검증절차에서 제일 최근값의 공개키 주소에 암호화된 해쉬가 있으면 for문 종료하는 것으로 해결.

            #개인키 트랜잭션 검증오류 수정/ 개발 보상 트랜잭션 생성에서 생성되는거 오류 찾기(해결 : 이차원 배열값 지정 안해줌)
            #개인키 트랜잭션 검증은 필요가 없네. 개인키에 암호화된 구조로 찾으면 되니까.
            #개인키 기반으로 서칭하는게 훨씬 더 간단해보이는데 약간 알고리즘보단 키의 안전성에 보안성을 높여야되니까.
            #기반 해쉬를 통해 서칭하는게 나을 수 있나?
            #수신자 트랜잭션이라 개인키로 서칭하는게 맞지않나 싶음
            #애초에 해쉬값으로 서치하면 그냥 귀찮음. 값도 하나 더 받아야되고 수정 완료
            #UTXO 최신화 시켜주면 좋겠네

    if select == 3:
        data = str(input("생성할 개인키 값을 입력해주세요: "))
        a.New_transaction(data)

    if select == 4:
        break
#Hash_result = hashlib.sha256()
#Hash_result.update(Check_ad)
#Personal_key = Hash_result.hexdigests()
#형식으로 출력.

#암호화 연산에선
#Personal_key = str(Personal_key).encode 로 2진수데이터 인코딩


#트래잭션 송신시 트랜잭션 검증절차 걸쳐야함. 중복 안되게
#입력받은 트랜잭션 기반으로 검색 X 입력받은 개인키 기반으로 최근 트랜잭션 추적시스템

#완성 후 피드백
#1. 설계 미숙
#  설계 후 개발 도중 좀 더 디테일 하게 설계하고 작업했어야 되는 부분들이 있었음.
#2. 컴퓨팅적 사고 부족
#  CPU 레지스터의 메모리 할당구조와 데이터 용량 최적화 방식의 구현이 부족한 부분이 많았음.
#  추후 연산기능별 효율을 반영하여 구현하면 좀 더 효율적인 알고리즘이 구현 가능 할 것이라 생각.
#3. 타원곡선암호화 알고리즘 미사용
#  수학적 내용이 안배운 부분이 많고 복잡하여 패스했는데, 공부하고 만들었으면 금방 했을 것 같음.
#4. 전문적 프로젝트 구현 환경의 미숙
#  혼자 프로젝트를 생각하고 구현하다 보니, 체계화된 구현 방식보단 창의성에 기반한 결과값이 나온 것 같음. 큰 문제는 없는듯함.
