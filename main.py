from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
import sys
import math

class CalculadoraiPhone(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora iPhone")
        self.setFixedSize(400, 550)
        self.setStyleSheet("background-color: #000000;")
        self.initUI()
        
        # Variáveis para controle de cálculo
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False

    def initUI(self):
        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet(
            "background-color: #000000; color: white; font-size: 36px; border: none; padding: 10px;"
        )
        self.display.setReadOnly(True)
        self.display.setText("0")

        # Layout principal
        vbox = QVBoxLayout()
        vbox.addWidget(self.display)

        # Botões estilo iPhone
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout()
        grid.setSpacing(8)  # Espaçamento entre botões
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                button = QPushButton(btn_text)
                
                # Estilo para botões de operação
                if btn_text in ['C', '±', '%', '÷', '×', '-', '+', '=']:
                    button.setStyleSheet(
                        "QPushButton {background-color: #FF9500; color:white; border-radius: 35px; font-size:24px; font-weight: bold;}"
                        "QPushButton:hover {background-color: #FFB347;}"
                        "QPushButton:pressed {background-color: #E68A00;}"
                    )
                # Estilo para botões numéricos
                else:
                    button.setStyleSheet(
                        "QPushButton {background-color: #505050; color:white; border-radius: 35px; font-size:24px;}"
                        "QPushButton:hover {background-color: #707070;}"
                        "QPushButton:pressed {background-color: #909090;}"
                    )

                # Ajustar botão 0 para ser maior (duas colunas)
                if btn_text == '0':
                    button.setFixedSize(160, 70)
                    grid.addWidget(button, i, j, 1, 2)
                else:
                    button.setFixedSize(70, 70)
                    grid.addWidget(button, i, j)

                button.clicked.connect(self.on_click)

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def on_click(self):
        sender = self.sender().text()
        current = self.display.text()
        
        # Botões numéricos
        if sender.isdigit():
            if self.waiting_for_operand:
                self.display.setText(sender)
                self.waiting_for_operand = False
            else:
                self.display.setText(current if current != "0" else "" + sender)
        
        # Ponto decimal
        elif sender == '.':
            if self.waiting_for_operand:
                self.display.setText("0.")
                self.waiting_for_operand = False
            elif '.' not in current:
                self.display.setText(current + '.')
        
        # Operações
        elif sender in ['+', '-', '×', '÷']:
            if not self.waiting_for_operand:
                if self.first_operand is None:
                    self.first_operand = float(current)
                else:
                    self.calculate_result()
                self.operator = sender
                self.waiting_for_operand = True
        
        # Igual
        elif sender == '=':
            if self.operator is not None and not self.waiting_for_operand:
                self.calculate_result()
                self.operator = None
                self.waiting_for_operand = True
        
        # Limpar
        elif sender == 'C':
            self.display.setText("0")
            self.first_operand = None
            self.operator = None
            self.waiting_for_operand = False
        
        # Trocar sinal
        elif sender == '±':
            value = float(current)
            self.display.setText(str(-value))
        
        # Porcentagem
        elif sender == '%':
            value = float(current)
            self.display.setText(str(value / 100))
        
        # Atualizar display
        self.display.setFocus()

    def calculate_result(self):
        second_operand = float(self.display.text())
        
        try:
            if self.operator == '+':
                result = self.first_operand + second_operand
            elif self.operator == '-':
                result = self.first_operand - second_operand
            elif self.operator == '×':
                result = self.first_operand * second_operand
            elif self.operator == '÷':
                if second_operand == 0:
                    self.display.setText("Erro")
                    return
                result = self.first_operand / second_operand
            
            # Formatar resultado
            if result.is_integer():
                self.display.setText(str(int(result)))
            else:
                self.display.setText(f"{result:.10g}".replace(".", ","))
            
            self.first_operand = result
        except:
            self.display.setText("Erro")
            self.first_operand = None
            self.operator = None
            self.waiting_for_operand = False

    def keyPressEvent(self, event):
        key = event.text()
        key_code = event.key()
        
        # Números e operações
        if key in '0123456789.+-*/':
            if key == '*':
                self.on_click_by_key('×')
            elif key == '/':
                self.on_click_by_key('÷')
            else:
                self.on_click_by_key(key)
        
        # Enter para igual
        elif key_code == Qt.Key_Return or key_code == Qt.Key_Enter:
            self.on_click_by_key('=')
        
        # Escape para limpar
        elif key_code == Qt.Key_Escape:
            self.on_click_by_key('C')
        
        # Backspace para apagar
        elif key_code == Qt.Key_Backspace:
            current = self.display.text()
            if len(current) > 1:
                self.display.setText(current[:-1])
            else:
                self.display.setText("0")
        
        # Sinais especiais
        elif key == '%':
            self.on_click_by_key('%')
        elif key == '±' or key_code == Qt.Key_F2:
            self.on_click_by_key('±')

    def on_click_by_key(self, key):
        # Simular clique do botão
        class TempSender:
            def __init__(self, text):
                self._text = text
            def text(self):
                return self._text
        
        # Encontrar o botão correspondente e simular clique
        for child in self.findChildren(QPushButton):
            if child.text() == key:
                self.sender = lambda: TempSender(key)
                self.on_click()
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = CalculadoraiPhone()
    calc.show()
    sys.exit(app.exec_())