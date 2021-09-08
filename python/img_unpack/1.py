import os


filebin = open('./2.bin','rb')
filewrite = open('./img.txt','w')

size = os.path.getsize('./2.bin')

img_list = list()
x=0
y=199

for i in range(size):
    #print(str(filebin.read(1))[4:6])
    img_16 = str(bin(ord(filebin.read(1))))[2:11]#很奇怪但是能用的东西
    while len(img_16)<8:
        img_16 = '0' + img_16
    #img_16 = hex(str(filebin.read(1))[4:6])
    print(img_16)
    j=0
    while j<=7:
        filewrite.write(str(img_16)[j]+',')
        j+=1
        #img_list = list()
        #counter=0
        x+=1
        if x>319:
            filewrite.write('\n')
            y-=1
            x=0

filebin.close()
filewrite.close()