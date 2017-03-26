print("Hello, world")
DEFAULT_CAESAR_KEY = 3
DEFAULT_MONO_KEY = {
    'a':'q','b':'w','c':'e','d':'r','e':'t',
    'f':'y','g':'u','h':'i','i':'o','j':'p',
    'k':'a','l':'s','m':'d','n':'f','o':'g',
    'p':'h','q':'j','r':'k','s':'l','t':'z',
    'u':'x','v':'c','w':'v','x':'b','y':'n',
    'z':'m'
}
DEFAULT_VERNAM_KEY = "kmt"
DEFAULT_PLAYFAIR_KEY = "dpp"
DEFAULT_ROW_TRANS_KEY = [5,2,8,3,4,6,7,1]
DEFAULT_PRODUCT_KEY = {1:15,2:11,3:2,4:10,5:16,
                       6:3,7:7,8:14,9:4,10:12,
                       11:9,12:6,13:1,14:5,15:8,
                       16:13}
from abc import abstractclassmethod
class baseCiphering:
    dict = {'a':0,'b':1,'c':2,'d':3,'e':4,
            'f':5,'g':6,'h':7,'i':8,'j':9,
            'k':10,'l':11,'m':12,'n':13,'o':14,
            'p':15,'q':16,'r':17,'s':18,'t':19,
            'u':20,'v':21,'w':22,'x':23,'y':24,
            'z':25,'A':26,'B':27,'C':28,'D':29,
            'E':30,'F':31}
    rev_dict = {}
    def __init__(self, key):
        self.setKey(key)
        self.rev_dict = self.reverse_dict(self.dict)

    def reverse_dict(self, dictionary):
        result = {}
        for itm in dictionary.items():
            result[itm[1]] = itm[0]
        return result

    def setKey(self, key):
        self.key = key
    @abstractclassmethod
    def encrypting(self, plainText):
        pass

    @abstractclassmethod
    def decrypting(self, cyptherText):
        pass

class CaesarCipher(baseCiphering):
    def __init__(self, key = DEFAULT_CAESAR_KEY):
        super(CaesarCipher, self).__init__(key)
    def encrypting(self, plainText):
        num_list = []

        for a in plainText:
            num_list.append(self.dict[a])
        for a in range(0,len(num_list)):
            num_list[a] += self.key
            if num_list[a] >= 26:
                num_list[a] -= 26
            if num_list[a] < 0:
                num_list[a] += 26


        result = ""
        for a in num_list:
            result+=self.rev_dict[a]
        return result

    def decrypting(self, cyptherText):
        self.key = -self.key
        return self.encrypting(cyptherText)


class MonoalphabeticCipher(baseCiphering):
    def __init__(self,key = DEFAULT_MONO_KEY):
        super(MonoalphabeticCipher, self).__init__(key)
    def encrypting(self, plainText):
        result = ""
        for a in plainText:
            result += self.key[a]
        return result

    def decrypting(self, cyptherText):
        decryptingKey = self.reverse_dict(self.key)
        result = ""
        for a in cyptherText:
            result += decryptingKey[a]
        return result

class PlayFairCipher(baseCiphering):
    def __init__(self, key = DEFAULT_PLAYFAIR_KEY):
        super(PlayFairCipher, self).__init__(key)

    dict_ch_to_coord = {}
    dict_coord_to_ch = {}
    def generateCipherMatrix(self):
        mat = []
        temp = []
        for a in self.key:
            temp.append(self.dict[a])
        decimalKey = []
        for a in temp:
            if not a in decimalKey:
                decimalKey.append(a)
        resultInLine = []
        for a in decimalKey:
            resultInLine.append(self.rev_dict[a])
        for a in range(0,26):
            if (not a in decimalKey)and(not a == self.dict['j']):
                resultInLine.append(self.rev_dict[a])
        if not len(resultInLine) ==25:
            return
        for a in range(0,5):
            mat.append([])
            for b in range(0,5):
                mat[a].append(resultInLine[a*5 + b])
        for a in range(0,5):
            for b in range(0,5):
                self.dict_ch_to_coord[mat[a][b]] = (a,b)
                self.dict_coord_to_ch[(a,b)] = mat[a][b]

    def devide(self, text):
        result_tmp = []
        for a in text:
            result_tmp.append(a)
        a = 0
        while True:
            if a >= len(result_tmp) -1:break
            if result_tmp[a] == result_tmp[a+1]:
                result_tmp.insert(a+1,'x')
            a += 2

        if not len(result_tmp) % 2 == 0:
            result_tmp.append('x')
        return result_tmp

    ENCRPTING_TYPE = 1
    DECRPTING_TYPE = -1
    def replace(self,text,actionType):
        if not len(text) % 2 == 0:
            return
        result = []
        for a in range(0, len(text)-1,2):
            temp = self.compareCoor(text[a],text[a+1])
            if temp == self.SQUARE_TYPE:
                result.append(self.dict_coord_to_ch[(
                    self.dict_ch_to_coord[text[a]][0],
                    self.dict_ch_to_coord[text[a+1]][1]
                )])
                result.append(self.dict_coord_to_ch[(
                    self.dict_ch_to_coord[text[a+1]][0],
                    self.dict_ch_to_coord[text[a]][1]
                )])
            elif temp == self.SAME_ROW_TYPE:
                tmpCol = self.dict_ch_to_coord[text[a]][1] + actionType
                if tmpCol > 4:
                    tmpCol -= 5
                elif tmpCol < 0:
                    tmpCol += 5
                result.append(self.dict_coord_to_ch[(
                    self.dict_ch_to_coord[text[a]][0],
                    tmpCol
                )])
                tmpCol = self.dict_ch_to_coord[text[a+1]][1] + actionType
                if tmpCol > 4:
                    tmpCol-=5
                elif tmpCol <0:
                    tmpCol += 5
                result.append(self.dict_coord_to_ch[(
                    self.dict_ch_to_coord[text[a+1]][0],
                    tmpCol
                )])
            elif temp == self.SAME_COL_TYPE:
                tmpRow = self.dict_ch_to_coord[text[a]][0] + actionType
                if tmpRow >4:
                    tmpRow -= 5
                elif tmpRow < 0:
                    tmpRow += 5
                result.append(self.dict_coord_to_ch[(
                    tmpRow,
                    self.dict_ch_to_coord[text[a]][1]
                )])
                tmpRow = self.dict_ch_to_coord[text[a+1]][0] + actionType
                if tmpRow >4:
                    tmpRow -= 5
                elif tmpRow < 0:
                    tmpRow += 5
                result.append(self.dict_coord_to_ch[(
                    tmpRow,
                    self.dict_ch_to_coord[text[a+1]][1]
                )])
        return result

    SQUARE_TYPE = 1
    SAME_ROW_TYPE = 2
    SAME_COL_TYPE = 3
    def compareCoor(self, ch1,ch2):
        coord1 = self.dict_ch_to_coord[ch1]
        coord2 = self.dict_ch_to_coord[ch2]
        if (not coord1[0] == coord2[0]) and (not coord1[1] == coord2[1]):
            return self.SQUARE_TYPE
        if (not coord1[0] == coord2[0]) and (coord1[1] == coord2[1]):
            return self.SAME_COL_TYPE
        if (coord1[0] == coord2[0]) and (not coord1[1] == coord2[1]):
            return self.SAME_ROW_TYPE


    def encrypting(self, plainText):
        self.generateCipherMatrix()
        handledText = []
        for a in range(0,len(plainText)):
            if not plainText[a] == 'j':
                handledText.append(plainText[a])
            elif plainText[a] == 'j':
                handledText.append('i')
        handledText = self.devide(handledText)
        handledText = self.replace(handledText, actionType=self.ENCRPTING_TYPE)
        resultStr = ""
        for a in handledText:
            resultStr += a
        return resultStr

    def decrypting(self, cyptherText):
        self.generateCipherMatrix()
        handledText = self.devide(cyptherText)
        handledText = self.replace(handledText, actionType=self.DECRPTING_TYPE)
        index = 0
        while True:
            if index < 0 or index >= len(handledText):
                break
            if (handledText[index] == 'x'):
                if index == 0:
                    pass
                elif index == len(handledText)-1:
                    handledText.pop(index)
                else :
                    if handledText[index-1] == handledText[index+1]:
                        handledText.pop(index)
            index += 1
        resultStr = ""
        for a in handledText:
            resultStr += a
        return resultStr

class VernamCipher(baseCiphering):
    def __init__(self,key = DEFAULT_VERNAM_KEY):
        super(VernamCipher, self).__init__(key)
    def XOR(self,stream1,stream2):
        if len(stream1) != len(stream2):
            return
        result = []
        for a in range(0, len(stream1)):
            if stream1[a] == stream2[a]:
                result.append(0)
            else: result.append(1)
        return result
    def decimalToBinaryList(self,decimalInput):
        tempStr = bin(decimalInput)
        resultLst = []
        for a in range(2,len(tempStr)):
            resultLst.append(tempStr[a])
        while True:
            if len(resultLst)<5:
                resultLst.insert(0,'0')
            else: break
        return resultLst

    def generateKeyStream(self, plainText):
        result = list(self.key)
        result.extend(list(plainText))
        result = result[:len(plainText)]
        return result

    def handle(self,inputx,inputy):
        x = self.dict[inputx]
        y = self.dict[inputy]
        tempLst = (self.XOR(self.decimalToBinaryList(x),self.decimalToBinaryList(y)))
        tempStr = ""
        for idx in tempLst:
            tempStr += str(idx)
        return self.rev_dict[int(tempStr,2)]

    def encrypting(self, plainText):
        result = ""
        keyStream = self.generateKeyStream(plainText)
        for a in range(0, len(plainText)):
            result+=str(self.handle(keyStream[a],plainText[a]))
        return result

    def decrypting(self, cyptherText):
        result = ""
        keyStream = []
        for a in self.key:
            keyStream.append(a)
        for a in range(0,len(cyptherText)):
            result += str(self.handle(keyStream[a],cyptherText[a]))
            keyStream.append(result[a])
        return result

class RowTransportation(baseCiphering):
    def __init__(self,key = DEFAULT_ROW_TRANS_KEY):
        super(RowTransportation, self).__init__(key)


    def generateKeyPad(self):
        reverse_key = {}
        for a in range(0,len(self.key)):
            reverse_key[int(self.key[a])] = a
        return reverse_key
    def encrypting(self, plainText):
        rows = []
        for a in range(0, len(self.key)):
            rows.append([])
        for a in range(0,len(plainText)):
            rows[a%len(self.key)].append(plainText[a])
        reverse_key = self.generateKeyPad()
        result = []
        for a in sorted(reverse_key.keys()):
            result.extend(rows[reverse_key[a]])
        resultStr = ""
        for a in result:
            resultStr += a
        return resultStr
    def decrypting(self, cyptherText):
        rowLength = []
        extra = len(cyptherText)%len(self.key)
        mainPart = int(len(cyptherText)/len(self.key))
        for a in range(0,len(self.key)):
            rowLength.append(mainPart)
            if(a < extra):
                rowLength[a] +=1
        reverse_key = self.generateKeyPad()
        rows = []
        for a in range(0, len(self.key)):
            rows.append([])

        c = 0
        for a in range(0, len(self.key)):
            for b in range(0, rowLength[reverse_key[a+1]]):
                rows[reverse_key[a+1]].append(cyptherText[c])
                c += 1
        result = ""
        for a in range(0,mainPart):
            for b in range(0,len(self.key)):
                result += rows[b][a]
        if extra != 0:
            for b in range(0, extra):
                result += rows[b][mainPart]
        return result

class ProductCipher(baseCiphering):
    def __init__(self,key=DEFAULT_PRODUCT_KEY):
        super(ProductCipher, self).__init__(key)
    def encrypting(self, plainText):
        reversePad = self.reverse_dict(self.key)
        result = self.transport(plainText,reversePad)
        return result

    def transport(self,source,keyPad):
        result = ""
        for a in range(0,len(source)):
            result += source[keyPad[a+1]-1]
        return result
    def decrypting(self, cyptherText):
        return self.transport(cyptherText,self.key)

TESTSTRING = "sentfrommyiphone"

def test(cipherMachine, str):
    print(type(cipherMachine))
    a = cipherMachine.encrypting(str)
    print(a)
    print(cipherMachine.decrypting(a))

lst = []
lst.append(CaesarCipher())
lst.append(MonoalphabeticCipher())
lst.append(PlayFairCipher())
lst.append(VernamCipher())
lst.append(RowTransportation())
lst.append(ProductCipher())
for a in lst:
    test(a, TESTSTRING)