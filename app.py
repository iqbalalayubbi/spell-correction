from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QKeyEvent, QTextCursor, QTextCharFormat, QColor, QClipboard, QGuiApplication
from PyQt5.QtCore import Qt, QTimer
import sys
import os
from spellCheck import correction

class MyGUI(QMainWindow):
    def __init__(self):
        self.fontSize = 18
        uiPath = resource_path('UI.ui')
        super(MyGUI, self).__init__()
        uic.loadUi(uiPath, self)
        self.show()

        # event handlers
        self.text_edit.textChanged.connect(self.text_edit_change)
        self.copy_btn.clicked.connect(self.copyText)
        self.check_btn.clicked.connect(self.checkSpell)

        # Menonaktifkan event filter jika ada
        self.text_edit.installEventFilter(self)
        self.text_correction.installEventFilter(self)
        self.text_edit.setFontPointSize(self.fontSize)                
        
    def copyText(self):
        clipboard = QApplication.clipboard()
        wordCorrect = self.text_correction.toPlainText()
        textCopy = clipboard.setText(wordCorrect)

        self.copy_btn.setText("teks berhasil disalin")
        self.defaultStyle = self.copy_btn.styleSheet()
        self.copy_btn.setStyleSheet("background-color: #37a36a; color:white; height:50;font-weight:500;")
  
        # set timer
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.resetCopyBtn)

    def checkSpell(self):
        self.checkSpell()
        pass

    def text_edit_change(self):
        self.text_edit.setFontPointSize(self.fontSize)

    def resetCopyBtn(self):    
        self.timer.stop()
        self.copy_btn.setStyleSheet(self.defaultStyle)
        self.copy_btn.setText("Salin Teks")
        

    def close_notification(self):
        print("nutup")
        self.notification.close()
        self.timer.stop()  

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress:
            self.keyPressEvent(event)
        if event.type() == QKeyEvent.KeyRelease:
            if event.key() == Qt.Key.Key_Space:
                self.checkSpell()
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent):
            # print("Key Pressed:", event.text())
            pass

    def checkSpell(self):
        words = self.text_edit.toPlainText()
        words = words.split()
        allWord = []

        document = self.text_edit.document()
        cursor = QTextCursor(document)
        cursor.movePosition(QTextCursor.Start)
        # wrong formatting
        wrong_format = QTextCharFormat()
        wrong_format.setFontPointSize(self.fontSize)
        wrong_format.setForeground(QColor('red'))
        # correct formatting
        correct_format = QTextCharFormat()
        correct_format.setFontPointSize(self.fontSize)
        correct_format.setForeground(QColor('black'))

        correctionWords = []

        for word in words:
            correctWord = correction(word)
            allWord.append(correctWord)

            if (word != correctWord):                                        
                wrongWord = {
                    "word": word,
                    "isCorrect": False,
                    "correct" : correctWord
                }
                correctionWords.append(wrongWord)
            else:
                correctWord = {
                    "word": word,
                    "isCorrect": True,
                    "correct" : word
                }
                correctionWords.append(correctWord)

        self.text_correction.setText(' '.join(allWord))        
        
        for word in correctionWords:            
            if word["isCorrect"]:
                cursor = document.find(word["word"], cursor)
                cursor.mergeCharFormat(correct_format)
            else:
                cursor = document.find(word["word"], cursor)
                cursor.mergeCharFormat(wrong_format)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path) 

def main():
    app = QApplication(sys.argv)
    window = MyGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
