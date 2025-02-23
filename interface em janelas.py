import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, 
                            QVBoxLayout, QLabel, QMessageBox, QFrame, QProgressBar, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QMovie

class TelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MG Spoofer - Login')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0a0047,
                    stop: 0.5 #1a0058,
                    stop: 1 #380080
                );
                color: #00ff99;
            }
            QFrame {
                background: rgba(10, 10, 20, 180);
                border: 2px solid #ff00ff;
                border-radius: 20px;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #ff00ff;
                border-radius: 12px;
                background: rgba(20, 20, 40, 180);
                color: #00ff99;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #00ffff;
                background: rgba(30, 30, 50, 180);
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff00ff,
                    stop: 1 #00ffff
                );
                color: black;
                border: none;
                padding: 12px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00ffff,
                    stop: 1 #ff00ff
                );
            }
        ''')

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Logo ou Título
        titulo = QLabel('MG SPOOFER')
        titulo.setStyleSheet('''
            QLabel {
                color: #00b4ff;
                font-size: 32px;
                font-weight: bold;
                margin: 20px;
                text-shadow: 0 0 10px rgba(0, 180, 255, 0.7);
            }
        ''')
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel('Sistema de Autenticação')
        subtitulo.setStyleSheet('color: #808080; font-size: 14px;')
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        # Container para os campos
        container = QFrame()
        container.setStyleSheet('''
            QFrame {
                background: rgba(20, 20, 20, 180);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
            }
        ''')
        container_layout = QVBoxLayout()

        # Campo de usuário
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText('Usuário')
        self.usuario.setStyleSheet('''
            QLineEdit {
                padding: 12px;
                border: 2px solid #333333;
                border-radius: 6px;
                background-color: #2C2C2C;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #00b4ff;
            }
        ''')
        container_layout.addWidget(self.usuario)

        # Campo de senha
        self.senha = QLineEdit()
        self.senha.setPlaceholderText('Senha')
        self.senha.setEchoMode(QLineEdit.Password)
        self.senha.setStyleSheet(self.usuario.styleSheet())
        container_layout.addWidget(self.senha)

        # Botão de login
        self.btn_login = QPushButton('ENTRAR')
        self.btn_login.setStyleSheet('''
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00b4ff,
                    stop: 1 #0066ff
                );
                color: white;
                border: none;
                padding: 12px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #0066ff,
                    stop: 1 #00b4ff
                );
            }
        ''')
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.fazer_login)
        container_layout.addWidget(self.btn_login)

        # Adicione o botão registrar após o botão login
        self.btn_registrar = QPushButton('REGISTRAR')
        self.btn_registrar.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #00b4ff;
                border: 2px solid #00b4ff;
                padding: 12px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: rgba(0, 180, 255, 0.1);
            }
        ''')
        self.btn_registrar.setCursor(Qt.PointingHandCursor)
        self.btn_registrar.clicked.connect(self.registrar)
        container_layout.addWidget(self.btn_registrar)

        # Botão Discord
        self.btn_discord = QPushButton('DISCORD')
        self.btn_discord.setStyleSheet('''
            QPushButton {
                background: #5865F2;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #4752C4;
            }
        ''')
        self.btn_discord.setCursor(Qt.PointingHandCursor)
        self.btn_discord.clicked.connect(self.abrir_discord)
        container_layout.addWidget(self.btn_discord)

        container.setLayout(container_layout)
        layout.addWidget(container)

        # Adicionar espaçamento
        layout.addStretch()

        # Footer
        footer = QLabel('© 2024 MG Spoofer. Todos os direitos reservados.')
        footer.setStyleSheet('color: #808080; font-size: 12px;')
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.setLayout(layout)

        # Adicionar evento de Enter
        self.usuario.returnPressed.connect(self.fazer_login)
        self.senha.returnPressed.connect(self.fazer_login)

    def mostrar_carregamento(self):
        self.loading = QProgressBar()
        self.loading.setTextVisible(False)
        self.loading.setFixedHeight(3)  # Altura muito pequena para parecer uma linha
        self.loading.setStyleSheet('''
            QProgressBar {
                border: none;
                background: rgba(255, 255, 255, 0.1);
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff00ff,
                    stop: 1 #00ffff
                );
            }
        ''')
        self.loading.setRange(0, 0)  # Modo indeterminado
        self.layout().insertWidget(1, self.loading)

    def fazer_login(self):
        usuario = self.usuario.text()
        senha = self.senha.text()

        # Verifica se é admin
        is_admin = usuario == "adm1" and senha == "adm1"
        # Verifica se é usuário normal
        is_user = usuario == "test1" and senha == "test1"

        if is_admin or is_user:
            self.btn_login.setEnabled(False)
            self.btn_registrar.setEnabled(False)
            self.mostrar_carregamento()
            QTimer.singleShot(2000, lambda: self.abrir_tela_inicial(is_admin))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Erro')
            msg.setText('Usuário ou senha inválidos!')
            msg.setStyleSheet('''
                QMessageBox {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                QPushButton {
                    background: #00b4ff;
                    color: white;
                    border: none;
                    padding: 6px 20px;
                    border-radius: 8px;
                }
            ''')
            msg.exec_()

    def abrir_tela_inicial(self, is_admin):
        self.loading.deleteLater()
        self.tela_inicial = TelaInicial(is_admin)
        self.tela_inicial.show()
        self.close()

    def abrir_discord(self):
        import webbrowser
        webbrowser.open('https://discord.gg/seuservidor')  # Substitua com seu link do Discord

    def registrar(self):
        self.tela_registro = TelaRegistro()
        self.tela_registro.show()

class TelaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MG Spoofer - Registro')
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ff00ff,
                    stop: 0.5 #1a0058,
                    stop: 1 #00ffff
                );
            }
            QFrame {
                background: rgba(10, 10, 20, 180);
                border: 2px solid #00ffff;
                border-radius: 15px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ff00ff;
                border-radius: 8px;
                background: rgba(20, 20, 40, 180);
                color: #00ffff;
                font-size: 12px;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff00ff,
                    stop: 1 #00ffff
                );
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
        ''')
        
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel('REGISTRO')
        titulo.setStyleSheet('''
            color: #00ffff;
            font-size: 28px;
            font-weight: bold;
            margin: 20px;
            text-shadow: 0 0 10px #ff00ff;
        ''')
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Container
        container = QFrame()
        container_layout = QVBoxLayout()

        # Campos
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText('Usuário')
        self.senha = QLineEdit()
        self.senha.setPlaceholderText('Senha')
        self.senha.setEchoMode(QLineEdit.Password)
        self.key = QLineEdit()
        self.key.setPlaceholderText('Key de Ativação')

        container_layout.addWidget(self.usuario)
        container_layout.addWidget(self.senha)
        container_layout.addWidget(self.key)

        # Botão Registrar
        self.btn_confirmar = QPushButton('CONFIRMAR REGISTRO')
        self.btn_confirmar.clicked.connect(self.confirmar_registro)
        container_layout.addWidget(self.btn_confirmar)

        container.setLayout(container_layout)
        layout.addWidget(container)
        self.setLayout(layout)

    def confirmar_registro(self):
        usuario = self.usuario.text()
        senha = self.senha.text()
        key = self.key.text()

        # Lista de keys válidas (você pode modificar para sua própria validação)
        keys_validas = ['MGSP-2024', 'CYBER-2024', 'HACK-2024']

        if not all([usuario, senha, key]):
            self.mostrar_erro('Todos os campos são obrigatórios!')
            return

        if len(senha) < 3:
            self.mostrar_erro('A senha deve ter no mínimo 3 caracteres!')
            return

        if key not in keys_validas:
            self.mostrar_erro('Key de ativação inválida!')
            return

        # Se chegou aqui, registro bem sucedido
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Sucesso')
        msg.setText('Registro realizado com sucesso!')
        msg.setStyleSheet('''
            QMessageBox {
                background-color: #1a0058;
                color: #00ff99;
            }
            QPushButton {
                background: #ff00ff;
                color: black;
                border: none;
                padding: 6px 20px;
                border-radius: 8px;
            }
        ''')
        msg.exec_()
        self.close()

    def mostrar_erro(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Erro')
        msg.setText(mensagem)
        msg.setStyleSheet('''
            QMessageBox {
                background-color: #1a0058;
                color: #ff00ff;
            }
            QPushButton {
                background: #ff00ff;
                color: black;
                border: none;
                padding: 6px 20px;
                border-radius: 8px;
            }
        ''')
        msg.exec_()

class TelaInicial(QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MG Spoofer - Menu Principal')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0a0047,
                    stop: 0.5 #1a0058,
                    stop: 1 #380080
                );
            }
            QLabel {
                color: #00ffff;
                font-size: 32px;
                font-weight: bold;
                text-shadow: 0 0 10px #ff00ff;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff00ff,
                    stop: 1 #00ffff
                );
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00ffff,
                    stop: 1 #ff00ff
                );
            }
        ''')

        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel('MENU DO SPOOFER')
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Container para os botões
        container = QFrame()
        container.setStyleSheet('''
            QFrame {
                background: rgba(10, 10, 20, 180);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 20px;
            }
        ''')
        
        btn_layout = QVBoxLayout()

        # Botão Guia (agora primeiro)
        self.btn_guia = QPushButton('GUIA DE DESVINCULAÇÃO')
        self.btn_guia.clicked.connect(self.abrir_guia)
        btn_layout.addWidget(self.btn_guia)

        # Botão Spoofar (inicialmente desativado)
        self.btn_spoof = QPushButton('SPOOFAR COM 1 CLICK')
        self.btn_spoof.setEnabled(False)  # Começa desativado
        self.btn_spoof.setStyleSheet('''
            QPushButton:disabled {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #666666,
                    stop: 1 #888888
                );
                color: #CCCCCC;
            }
        ''')
        self.btn_spoof.clicked.connect(self.spoofar)
        btn_layout.addWidget(self.btn_spoof)

        # Botão Gerar Key (apenas para admin)
        if self.is_admin:
            self.btn_key = QPushButton('GERAR KEY')
            self.btn_key.setStyleSheet('''
                QPushButton {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #ff0000,
                        stop: 1 #ff00ff
                    );
                }
            ''')
            self.btn_key.clicked.connect(self.gerar_key)
            btn_layout.addWidget(self.btn_key)

        # Botão Sair
        self.btn_sair = QPushButton('SAIR')
        self.btn_sair.clicked.connect(self.sair)
        btn_layout.addWidget(self.btn_sair)

        container.setLayout(btn_layout)
        layout.addWidget(container)
        self.setLayout(layout)

    def spoofar(self):
        self.tela_spoofer = TelaSpoofer()
        self.tela_spoofer.show()

    def abrir_guia(self):
        self.tela_guia = TelaGuia(self)
        self.tela_guia.show()

    def gerar_key(self):
        import random
        import string
        
        key = 'MGSP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Key Gerada')
        msg.setText(f'Nova key gerada:\n{key}')
        msg.setStyleSheet('''
            QMessageBox {
                background-color: #1a0058;
                color: #00ff99;
            }
            QPushButton {
                background: #ff00ff;
                color: white;
                border: none;
                padding: 6px 20px;
                border-radius: 8px;
            }
        ''')
        msg.exec_()

    def sair(self):
        self.close()

# Adicione esta nova classe após a TelaInicial
class TelaSpoofer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MG Spoofer - Processo')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0a0047,
                    stop: 0.5 #1a0058,
                    stop: 1 #380080
                );
            }
            QLabel {
                color: #00ffff;
                font-size: 14px;
                margin: 5px;
            }
            QProgressBar {
                border: 2px solid #00ffff;
                border-radius: 5px;
                text-align: center;
                background-color: rgba(10, 10, 20, 180);
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #ff00ff,
                    stop: 1 #00ffff
                );
            }
        ''')

        layout = QVBoxLayout()
        
        # Container principal
        container = QFrame()
        container.setStyleSheet('''
            QFrame {
                background: rgba(10, 10, 20, 180);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 20px;
            }
        ''')
        
        container_layout = QVBoxLayout()

        # Título do processo
        self.titulo = QLabel('PROCESSO DE SPOOFING')
        self.titulo.setStyleSheet('font-size: 24px; font-weight: bold; text-align: center;')
        self.titulo.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.titulo)

        # Labels para as etapas
        self.etapas = [
            'Iniciando processo de spoofing...',
            'Verificando sistema...',
            'Limpando registros...',
            'Alterando identificadores...',
            'Finalizando processo...'
        ]
        
        self.labels = []
        for etapa in self.etapas:
            label = QLabel(f'⌛ {etapa}')
            label.setStyleSheet('color: #808080;')  # Inicialmente cinza
            self.labels.append(label)
            container_layout.addWidget(label)

        # Loading circular
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        container_layout.addWidget(self.progress)

        container.setLayout(container_layout)
        layout.addWidget(container)
        self.setLayout(layout)

        # Iniciar processo
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_process)
        self.timer.start(1000)  # Atualiza a cada segundo
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

    def update_process(self):
        if self.current_step < len(self.labels):
            # Atualiza o ícone e a cor do label atual
            self.labels[self.current_step].setStyleSheet('color: #00ffff;')
            self.labels[self.current_step].setText(f'✓ {self.etapas[self.current_step]}')
            self.progress.setValue((self.current_step + 1) * 20)
            self.current_step += 1
            
            if self.current_step == len(self.labels):
                QTimer.singleShot(1000, self.finish_process)

    def finish_process(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Sucesso')
        msg.setText('Processo de spoofing concluído com sucesso!')
        msg.setStyleSheet('''
            QMessageBox {
                background-color: #1a0058;
                color: #00ff99;
            }
            QPushButton {
                background: #ff00ff;
                color: white;
                border: none;
                padding: 6px 20px;
                border-radius: 8px;
            }
        ''')
        msg.exec_()
        self.close()

# Adicione esta nova classe após TelaSpoofer
class TelaGuia(QWidget):
    def __init__(self, tela_inicial):
        super().__init__()
        self.tela_inicial = tela_inicial
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MG Spoofer - Guia')
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0a0047,
                    stop: 0.5 #1a0058,
                    stop: 1 #380080
                );
            }
            QLabel {
                color: #00ffff;
                font-size: 14px;
                margin: 5px;
            }
            QCheckBox {
                color: #00ffff;
                font-size: 14px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #00ffff;
                border-radius: 5px;
                background: rgba(10, 10, 20, 180);
            }
            QCheckBox::indicator:checked {
                background: #ff00ff;
            }
        ''')

        layout = QVBoxLayout()
        
        # Container principal
        container = QFrame()
        container.setStyleSheet('''
            QFrame {
                background: rgba(10, 10, 20, 180);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 20px;
            }
        ''')
        
        container_layout = QVBoxLayout()

        # Título
        titulo = QLabel('GUIA DE DESVINCULAÇÃO')
        titulo.setStyleSheet('font-size: 24px; font-weight: bold;')
        titulo.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(titulo)

        # Texto do guia
        guia_texto = QLabel('''
            🔹 Passo 1: Faça backup dos seus dados importantes
            🔹 Passo 2: Desligue o antivírus
            🔹 Passo 3: Execute o programa como administrador
            🔹 Passo 4: Aguarde o processo completar
            🔹 Passo 5: Reinicie o computador
            
            ⚠️ ATENÇÃO: Este processo é irreversível!
        ''')
        guia_texto.setWordWrap(True)
        guia_texto.setStyleSheet('font-size: 16px; padding: 20px;')
        container_layout.addWidget(guia_texto)

        # Checkbox de confirmação
        self.checkbox = QCheckBox('Li e concordo com os termos acima')
        self.checkbox.stateChanged.connect(self.ativar_spoof)
        container_layout.addWidget(self.checkbox)

        container.setLayout(container_layout)
        layout.addWidget(container)
        self.setLayout(layout)

    def ativar_spoof(self, state):
        # Ativa o botão de spoof na tela inicial
        self.tela_inicial.btn_spoof.setEnabled(state == Qt.Checked)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    tela = TelaLogin()
    tela.show()
    sys.exit(app.exec_())