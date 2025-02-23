from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import psycopg2
import secrets
import datetime
import logging
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QMessageBox)

load_dotenv()

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_response_time(response):
    duration = time.time() - getattr(request, 'start_time', time.time())
    logging.info(f"Resposta enviada: {response.status} em {duration:.2f} segundos")
    return response

@app.before_request
def log_request_info():
    logging.info(f"Requisição recebida: {request.method} {request.url}")
    logging.info(f"Cabeçalhos: {dict(request.headers)}")
    if request.get_json():
        logging.info(f"Dados JSON: {request.get_json()}")

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "Servidor online!"})

# Endpoint para login com link do banco de dados
@app.route('/login', methods=['POST'])
def login():
    db_link = request.json.get('db_link')
    if not db_link:
        return jsonify({"success": False, "message": "Link do banco de dados não fornecido."}), 400
    try:
        conn = psycopg2.connect(db_link)
        conn.close()
        return jsonify({"success": True, "message": "Conexão bem-sucedida!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao conectar: {e}"}), 500

@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    logging.debug("Endpoint /generate_keys acessado.")
    # Obter o link do banco de dados da requisição
    db_link = request.json.get('db_link')
    if not db_link:
        return jsonify({"success": False, "message": "Link do banco de dados não fornecido."}), 400

    quantidade = request.json.get('quantidade', 1)
    duracao_dias = request.json.get('duracao_dias', 30)
    logging.debug(f"Quantidade solicitada: {quantidade}, Duração (dias): {duracao_dias}")

    if not isinstance(quantidade, int) or quantidade <= 0:
        logging.warning("Quantidade inválida fornecida.")
        return jsonify({"success": False, "message": "Quantidade inválida. Deve ser um número inteiro positivo."}), 400
    if not isinstance(duracao_dias, int) or duracao_dias <= 0:
        logging.warning("Duração inválida fornecida.")
        return jsonify({"success": False, "message": "Duração inválida. Deve ser um número inteiro positivo de dias."}), 400

    chaves_geradas = []
    try:
        conn = psycopg2.connect(db_link)
        cur = conn.cursor()
        for _ in range(quantidade):
            chave = secrets.token_urlsafe(32)
            data_expiracao = datetime.datetime.now() + datetime.timedelta(days=duracao_dias)
            cur.execute("INSERT INTO keys (chave, expira_em) VALUES (%s, %s)", (chave, data_expiracao))
            chaves_geradas.append({"chave": chave, "expira_em": data_expiracao.isoformat()})
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": f"{quantidade} chaves geradas com sucesso.", "chaves": chaves_geradas})
    except Exception as e:
        logging.error(f"Erro ao gerar chaves: {e}")
        return jsonify({"success": False, "message": f"Erro ao gerar chaves: {e}"}), 500

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    key = data.get('key')
    hwid = data.get('hwid')
    usuario = data.get('username')
    # Obter o link do banco de dados da requisição
    db_link = data.get('db_link')
    if not db_link:
        return jsonify({"success": False, "message": "Link do banco de dados não fornecido."}), 400

    if not key or not hwid or not usuario:
        return jsonify({"success": False, "message": "Dados incompletos fornecidos."}), 400

    try:
        conn = psycopg2.connect(db_link)
        cur = conn.cursor()
        cur.execute("SELECT id, expira_em, usada FROM keys WHERE chave = %s", (key,))
        chave_info = cur.fetchone()

        if not chave_info:
            return jsonify({"success": False, "message": "Chave de acesso inválida."}), 401

        chave_id, expira_em, usada = chave_info

        if usada or datetime.datetime.now() > expira_em:
            return jsonify({"success": False, "message": "Chave de acesso inválida ou expirada."}), 401

        cur.execute("INSERT INTO users (access_key, hwid, username, data_registro, data_expiracao) VALUES (%s, %s, %s, %s, %s)",
                    (key, hwid, usuario, datetime.datetime.now(), expira_em))
        cur.execute("UPDATE keys SET hwid = %s, usada = TRUE WHERE id = %s", (hwid, chave_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "Usuário registrado com sucesso!"})
    except Exception as e:
        logging.error(f"Erro ao registrar usuário: {e}")
        return jsonify({"success": False, "message": f"Erro ao registrar usuário: {e}"}), 500

@app.route('/validate_key', methods=['POST'])
def validate_key():
    data = request.get_json()
    chave = data.get('chave')
    usuario = data.get('key')  # Usando 'key' como 'usuario'
    hwid = data.get('hwid')
    # Obter o link do banco de dados da requisição
    db_link = data.get('db_link')
    if not db_link:
        return jsonify({"success": False, "message": "Link do banco de dados não fornecido."}), 400

    if chave == 'invalida':
        return jsonify({'error': 'Chave inválida'}), 400

    if not usuario or not hwid:
        return jsonify({"success": False, "message": "Dados incompletos fornecidos."}), 400

    try:
        conn = psycopg2.connect(db_link)
        cur = conn.cursor()
        cur.execute("SELECT data_expiracao FROM users WHERE username = %s AND hwid = %s", (usuario, hwid))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            data_expiracao_db = result[0]
            if datetime.datetime.now() <= data_expiracao_db:
                logging.info(f"Usuário '{usuario}' validado com sucesso.")
                return jsonify({"success": True, "message": "Chave/Usuário válido!"})
            else:
                logging.warning(f"Chave/Usuário '{usuario}' expirado.")
                return jsonify({"success": False, "message": "Chave/Usuário expirado."}), 401
        else:
            logging.warning(f"Tentativa de login inválida para usuário '{usuario}'.")
            return jsonify({"success": False, "message": "Usuário/Chave inválido ou não registrado para este HWID."}), 401
    except Exception as e:
        logging.error(f"Erro ao validar chave/usuário: {e}")
        return jsonify({"success": False, "message": f"Erro ao validar chave/usuário: {e}"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Erro não tratado: {str(e)}", exc_info=True)
    logging.error(f"Requisição que causou o erro: {request.method} {request.url}")
    return jsonify({"success": False, "message": "Erro interno do servidor."}), 500

# Interface Gráfica com PyQt5
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.db_link_label = QLabel("Link do Banco de Dados:")
        self.db_link_input = QLineEdit()
        self.login_button = QPushButton("Conectar")
        self.login_button.clicked.connect(self.handle_login)

        layout = QVBoxLayout()
        layout.addWidget(self.db_link_label)
        layout.addWidget(self.db_link_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def handle_login(self):
        db_link = self.db_link_input.text()
        if not db_link:
            QMessageBox.warning(self, "Aviso", "Por favor, insira o link do banco de dados.")
            return

        try:
            conn = psycopg2.connect(db_link)
            conn.close()
            QMessageBox.information(self, "Sucesso", "Conexão bem-sucedida!")
            # Aqui você pode iniciar sua aplicação principal após a conexão
            # ...
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar: {e}")

if __name__ == '__main__':
    app.run(debug=True)

    # Iniciar a interface gráfica
    app_gui = QApplication([])
    window = LoginWindow()
    window.show()
    app_gui.exec_()
