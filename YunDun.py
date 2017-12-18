#-*-coding:utf-8-*-
class YunDun(object):
    def __init__(self):
        pass

    def get_cookie(self,ri,oo,s):
        RI = ri
        oo = eval(oo)
        qo = int(s[0])
        while qo>=int(s[4]):
            oo[qo]=(-oo[qo])&0xff
            oo[qo]=(((oo[qo]>>int(s[1]))|((oo[qo]<<int(s[2]))&0xff))-int(s[3]))&0xff
            qo -= 1
        qo = int(s[5])
        while qo>=int(s[7]):

            oo[qo] = (oo[qo] - oo[qo - int(s[6])]) & 0xff
            qo-=1

        qo =int(s[8])
        for qo in range(0,int(s[9])):
            oo[qo] = ((((((oo[qo] + int(s[10])) & 0xff) + int(s[11])) & 0xff) << int(s[12])) & 0xff) | (((((oo[qo] + int(s[13])) & 0xff) + int(s[14])) & 0xff) >> int(s[15]))

        po =""
        for qo in range(1,len(oo)-1):
            if (qo % int(s[18])):
                po +=chr(oo[qo]^int(RI))
        # print(po)
        cookie = po.split(";",1)[0].split("=")[-1]
        return cookie