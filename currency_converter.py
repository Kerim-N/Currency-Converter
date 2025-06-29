from PyQt6.QtWidgets import QWidget, QApplication
import sys, time, requests
import Currency_converter_form_main

class Currency_converter(QWidget, Currency_converter_form_main.Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.amount = 0
        
        self.btn_reverse.clicked.connect(self.reverse)
        self.pushButton.clicked.connect(self.converte)
        self.lineEdit_from.textChanged.connect(self.calculate)
        self.lineEdit_to.textChanged.connect(self.calculate)
        self.comboBox_from.currentTextChanged.connect(self.converte)
        self.comboBox_to.currentTextChanged.connect(self.converte)
        
    def converte(self):
        try:
            currency_from_amount = float(self.lineEdit_from.text())
        except:
            print("err3")
        currency_from_type = self.comboBox_from.currentText()
        currency_to_type = self.comboBox_to.currentText()    
        link = "https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies?base="+currency_from_type+"&quote="+currency_to_type+("&data_type=general_currency_pair&start_date=%d-%02d-%02d&end_date=%d-%02d-%02d" % (time.localtime()[0],time.localtime()[1],time.localtime()[2]-1,time.localtime()[0],time.localtime()[1],time.localtime()[2]))
        print(link)
        response = requests.get(link).json()
        self.amount = response["response"][0]["average_bid"]
        self.calculate(currency_from_amount)
        
    def calculate(self, text):
        if self.amount == 0:
            currency_from_type = self.comboBox_from.currentText()
            currency_to_type = self.comboBox_to.currentText()
            link = "https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies?base="+currency_from_type+"&quote="+currency_to_type+("&data_type=general_currency_pair&start_date=%d-%02d-%02d&end_date=%d-%02d-%02d" % (time.localtime()[0],time.localtime()[1],time.localtime()[2]-1,time.localtime()[0],time.localtime()[1],time.localtime()[2]))
            print(link)
            response = requests.get(link).json()
            self.amount = response["response"][0]["average_bid"]
        try:
            if float(text) == float(self.lineEdit_from.text()):
                self.lineEdit_to.setText(str(float(text) * float(self.amount)))
            else:
                self.lineEdit_from.setText(str(float(text) / float(self.amount)))
        except:
            print("err1")
            
    def reverse(self):
        currency_from_type_index = self.comboBox_from.currentIndex()
        currency_to_type_index = self.comboBox_to.currentIndex()
        try:
            currency_from_amount = float(self.lineEdit_from.text())
            currency_to_amount = float(self.lineEdit_to.text())
        except:
            print("err2")
        self.comboBox_from.setCurrentIndex(currency_to_type_index)
        self.comboBox_to.setCurrentIndex(currency_from_type_index)
        self.lineEdit_from.setText(str(currency_from_amount))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Currency_converter()
    window.setWindowTitle("Currency converter")
    window.show()
    sys.exit(app.exec())