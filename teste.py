import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap, QMovie
from PyQt5.QtCore import Qt

class BancoDeDadosAnimado(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('Banco de Dados Animado')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.movie = QMovie('banco_de_dados.gif')  # substitua por seu próprio arquivo gif
        self.label.setMovie(self.movie)
        self.movie.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    banco_de_dados_animado = BancoDeDadosAnimado()
    banco_de_dados_animado.show()
    sys.exit(app.exec_())