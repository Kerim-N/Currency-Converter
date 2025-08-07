from PyQt6.QtWidgets import QWidget, QApplication 
import sys, time, requests 
import Currency_converter_form_main  # Import the UI form created in Qt Designer

# Main class for Currency Converter, inherits from QWidget and the UI form
class Currency_converter(QWidget, Currency_converter_form_main.Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)  # Set up the UI from the Designer file
        self.amount = 0  # Store the current conversion rate

        # Connect UI buttons and inputs to respective functions
        self.btn_reverse.clicked.connect(self.reverse)  # Swap currencies
        self.pushButton.clicked.connect(self.converte)  # Convert currencies
        self.lineEdit_from.textChanged.connect(self.calculate)  # Handle changes in "from" field
        self.lineEdit_to.textChanged.connect(self.calculate)    # Handle changes in "to" field
        self.comboBox_from.currentTextChanged.connect(self.converte)  # Update on currency change
        self.comboBox_to.currentTextChanged.connect(self.converte)

    # Function to convert currency using API
    def converte(self):
        try:
            # Try to get the input amount from user
            currency_from_amount = float(self.lineEdit_from.text())
        except:
            print("err3")  # Input is not a valid number

        # Get selected currency types from combo boxes
        currency_from_type = self.comboBox_from.currentText()
        currency_to_type = self.comboBox_to.currentText()

        # Prepare API request link (OANDA API for currency exchange rates)
        link = (
            "https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies?"
            "base=" + currency_from_type +
            "&quote=" + currency_to_type +
            ("&data_type=general_currency_pair&start_date=%d-%02d-%02d&end_date=%d-%02d-%02d"
             % (
                 time.localtime()[0], time.localtime()[1], time.localtime()[2] - 1,
                 time.localtime()[0], time.localtime()[1], time.localtime()[2]
             ))
        )
        print(link)  # For debugging

        # Request exchange rate data from API
        response = requests.get(link).json()

        # Get average_bid rate and store it
        self.amount = response["response"][0]["average_bid"]

        # Call calculate to update converted value
        self.calculate(currency_from_amount)

    # Function to calculate and update the converted amount
    def calculate(self, text):
        # If amount is not yet set, fetch it again
        if self.amount == 0:
            currency_from_type = self.comboBox_from.currentText()
            currency_to_type = self.comboBox_to.currentText()
            link = (
                "https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies?"
                "base=" + currency_from_type +
                "&quote=" + currency_to_type +
                ("&data_type=general_currency_pair&start_date=%d-%02d-%02d&end_date=%d-%02d-%02d"
                 % (
                     time.localtime()[0], time.localtime()[1], time.localtime()[2] - 1,
                     time.localtime()[0], time.localtime()[1], time.localtime()[2]
                 ))
            )
            print(link)  # For debugging
            response = requests.get(link).json()
            self.amount = response["response"][0]["average_bid"]

        try:
            # If the user is editing the "from" field
            if float(text) == float(self.lineEdit_from.text()):
                self.lineEdit_to.setText(str(float(text) * float(self.amount)))
            # If the user is editing the "to" field
            else:
                self.lineEdit_from.setText(str(float(text) / float(self.amount)))
        except:
            print("err1")  # Input conversion error

    # Function to reverse (swap) currencies
    def reverse(self):
        # Save current indices
        currency_from_type_index = self.comboBox_from.currentIndex()
        currency_to_type_index = self.comboBox_to.currentIndex()

        try:
            # Save amounts to restore after swap
            currency_from_amount = float(self.lineEdit_from.text())
            currency_to_amount = float(self.lineEdit_to.text())
        except:
            print("err2")  # Invalid number input

        # Swap currencies in combo boxes
        self.comboBox_from.setCurrentIndex(currency_to_type_index)
        self.comboBox_to.setCurrentIndex(currency_from_type_index)

        # Restore original amount (optional)
        self.lineEdit_from.setText(str(currency_from_amount))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Currency_converter()
    window.setWindowTitle("Currency converter")  # Set window title
    window.show()
    sys.exit(app.exec())  # Start the event loop
