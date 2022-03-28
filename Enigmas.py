"""
Spy-Play-Game)))))
This program encodes messages for transmission in an open way.the checksum and the sender's mac 
are used. you need to create a document with a message and a document for encoding 2 files .txt
PyQt5 need
"""

import uuid
import re
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QFileDialog,QLabel
#UI module
cfilename = ''
mfilename = ''
class Inteface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mlbl = QLabel(self)
        self.mlbl.move(30, 20)
        global mfilename
        self.clbl = QLabel(self)
        self.clbl.move(150, 20)
        global cfilename
        self.slbl = QLabel(self)
        self.slbl.move(120, 140)
        btn1 = QPushButton("Message File", self)
        btn1.move(30, 50)
        btn2 = QPushButton("Coded File", self)
        btn2.move(150, 50)
        btn4 = QPushButton("scrambler", self)
        btn4.move(1, 110)
        btn5 = QPushButton("decoder", self)
        btn5.move(200, 110)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        btn4.clicked.connect(self.buttonClicked)
        btn5.clicked.connect(self.buttonClicked)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('ENIGMA')
        self.show()   
    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == "Message File":
            global mfilename
            mfilename = QFileDialog.getOpenFileName(self, 'Open Message File', '/home')[0]
            self.mlbl.setText(mfilename)  
        elif sender.text() == "Coded File":
            global cfilename
            cfilename = QFileDialog.getOpenFileName(self, 'Open Coded File', '/home')[0]
            self.clbl.setText(cfilename)
        elif sender.text() == "scrambler":
            Messag.mescoder(mfilename, cfilename)
            self.slbl.setText('Coded')
        elif sender.text() == "decoder":
            Messag.mesdecoder(mfilename, cfilename)
            self.slbl.setText('Decoded')
#Coding_message_module
class Messag(Inteface):  
    def __init__(self):
         super().__init__()
         self.fread()
         self.fwrite()
    def mescoder(mfilename, cfilename):
        targetreadfile = mfilename
        targetwritefile = cfilename
        textfile = Messag.fread(targetreadfile)
        hashi =  Messag.hashicode(textfile)
        keysum = Messag.keysumcode(hashi)
        mackey = Messag.maccode()
        record = (mackey + hashi + keysum)
        Messag.fwrite(targetwritefile, record)
       
    def mesdecoder(mfilename, cfilename):
        targetreadfile = cfilename
        targetwritefile = mfilename
        textfile = Messag.fread(targetreadfile)
        textfile = Messag.textfileclean(textfile)
        mac = Messag.macdecode(textfile)
        keysum = Messag.keysumdecode(textfile)
        textfile = Messag.textfilecut(textfile)
        if (Messag.checksumkey(textfile, keysum)):
            message = Messag.textfiledecode(textfile)  
            decodemassege = str('sendler mac:_' + mac + '_message:' + message)
            Messag.fwrite(targetwritefile, decodemassege)    
        else: 
            print('WARNING!!!File not full or was changed')
 #Read_from_file
    def fread(targetfile):
        with open(targetfile) as f:
             repfiletxt = (f.readlines())
             textfile = str(repfiletxt)
             f.close
             return textfile
 #Write_to_file
    def fwrite(targetfile, record):
        with open(targetfile, "w") as f:
                f.write(record)
                f.close()   
#MAC_addres_coding
    def maccode():
        mac = (''.join(re.findall('..', '%012x' % uuid.getnode())))
        macbin = bin(int.from_bytes(mac.encode('utf-8'), 'big'))[2:]
        mackey = '1' + macbin.zfill(99)
        return mackey
#Keysum_coding
    def keysumcode(hashi):
        hashiconsum = bin((list(hashi)).count('1'))[2:]
        keysum=hashiconsum.zfill(20)
        return keysum
#Body_massege_coding
    def hashicode(textfile)
        hashi = bin(int.from_bytes(textfile.encode('utf-8'), 'big'))[2:]  
        return hashi
#Cutfile
    def textfileclean(textfile):
        textfile = (textfile.replace('[', '').replace(']', '').replace("'", ''))
        return textfile
#MAC_addr_decoding
    def macdecode(textfile):
        mackeybin = textfile[1:100]
        mackey = (int(str(mackeybin), 2))
        mack = mackey.to_bytes((mackey.bit_length() + 7) // 8, 'big').decode()
        mac = mack[:2] + ':' + mack[2:4] + ':' + mack[4:6] + ':' + mack[6:8] + ':' + mack[8:10] + ':' + mack[10:]
        return mac
#Keysum_decoding
    def keysumdecode(textfile):
        messagelen = len(textfile)
        keysum = (int(str(textfile[(messagelen - 20) : messagelen]), 2))
        return keysum
#Cutfile
    def textfilecut(textfile):
        messagelen = (len(textfile))
        textfile = str(textfile[100 : messagelen - 20])
        textfile = '0b' + textfile
        return textfile
#Keysum_val
    def checksumkey(textfile, keysum):
        return(textfile.count('1') == keysum)
#Decode_budy
    def textfiledecode(textfile):
        messagebin = int(textfile, 2)
        message = messagebin.to_bytes((messagebin.bit_length() + 7) // 8, 'big').decode()
        return message


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Inteface()
    sys.exit(app.exec_())


