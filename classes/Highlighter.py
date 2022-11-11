from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QColor


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None, colors=None):
        super(Highlighter, self).__init__(parent)

        if colors is None or colors == {}:
            return

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QColor(colors["keyboard"]))

        keywordPatterns = colors["keyboardPattern"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                                  for pattern in keywordPatterns]

        selfFormat = QtGui.QTextCharFormat()
        selfFormat.setForeground(QColor("#8F4C61"))
        self.highlightingRules.append((QtCore.QRegExp("\\bself\\b"), selfFormat))
        print(5)
        numberFormat = QtGui.QTextCharFormat()
        numberFormat.setForeground(QColor(colors["number"]))
        self.highlightingRules.append((QtCore.QRegExp("\\b[0-9]+\\b"), numberFormat))

        classFormat = QtGui.QTextCharFormat()
        classFormat.setForeground(QColor(colors["class"]))
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                                       classFormat))

        classFormat = QtGui.QTextCharFormat()
        classFormat.setForeground(QColor(colors["class"]))
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Z][A-Za-z]+\\b"),
                                       classFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QColor(colors["quotation"]))
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                                       quotationFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QColor(colors["quotation"]))
        self.highlightingRules.append((QtCore.QRegExp("'.*'"),
                                       quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setForeground(QColor(colors["function"]))
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                                       functionFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QColor(colors["multiLineComment"]))
        self.highlightingRules.append((QtCore.QRegExp("#.*"), self.multiLineCommentFormat))
        self.highlightingRules.append((QtCore.QRegExp('""".*"""'), self.multiLineCommentFormat))


        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                           self.multiLineCommentFormat)

            startIndex = self.commentStartExpression.indexIn(text, startIndex + commentLength)
