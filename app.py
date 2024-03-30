from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QKeyEvent, QTextCursor, QTextCharFormat, QColor, QClipboard, QGuiApplication
from PyQt5.QtCore import Qt
import sys
from spellCheck import correction

class MyGUI(QMainWindow):
    def __init__(self):
        self.fontSize = 18
        super(MyGUI, self).__init__()
        uic.loadUi('UI.ui', self)
        self.show()
        self.text_edit.textChanged.connect(self.text_edit_change)
        # Menonaktifkan event filter jika ada
        self.text_edit.installEventFilter(self)
        self.text_correction.installEventFilter(self)
        self.text_edit.setFontPointSize(self.fontSize)        

    def text_edit_change(self):
        self.text_edit.setFontPointSize(self.fontSize)
        # self.checkSpell()


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

    # while not cursor.isNull():
    #             cursor = document.find(word, cursor)
    #             if cursor.isNull():
    #                 break
    #             cursor.mergeCharFormat(wrong_format)                                          

def main():
    app = QApplication(sys.argv)
    window = MyGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
