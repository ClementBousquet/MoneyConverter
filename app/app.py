from PySide2 import QtWidgets
import currency_converter

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.setup_connections()

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.combo_devisesFrom = QtWidgets.QComboBox()
        self.spin_montant = QtWidgets.QSpinBox()
        self.combo_devisesTo = QtWidgets.QComboBox()
        self.spin_montantConv = QtWidgets.QSpinBox()
        self.button_invert = QtWidgets.QPushButton("Convertir")
        self.layout.addWidget(self.combo_devisesFrom)
        self.layout.addWidget(self.spin_montant)
        self.layout.addWidget(self.combo_devisesTo)
        self.layout.addWidget(self.spin_montantConv)
        self.layout.addWidget(self.button_invert)


    def set_default_values(self):
        self.combo_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.combo_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.combo_devisesFrom.setCurrentText("EUR")
        self.combo_devisesTo.setCurrentText("EUR")

        self.spin_montant.setRange(1, 1000000000)
        self.spin_montantConv.setRange(1, 1000000000)
        self.spin_montant.setValue(100)
        self.spin_montantConv.setValue(100)


    def setup_connections(self):
        self.combo_devisesFrom.activated.connect(self.compute)
        self.combo_devisesTo.activated.connect(self.compute)
        self.spin_montant.valueChanged.connect(self.compute)
        self.button_invert.clicked.connect(self.inverser_devise)


    def setup_css(self):
        self.setStyleSheet("""
        background-color: rgb(30, 30 ,30);
        color: rgb(240, 240, 240);
        border: none;
        """)


    def compute(self):
        montant = self.spin_montant.value()
        deviseFrom = self.combo_devisesFrom.currentText()
        deviseTo = self.combo_devisesTo.currentText()
        try:
            res = self.c.convert(montant, deviseFrom, deviseTo)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion a échoué.")
        else:
            self.spin_montantConv.setValue(res)


    def inverser_devise(self):
        deviseFrom = self.combo_devisesFrom.currentText()
        deviseTo = self.combo_devisesTo.currentText()

        self.combo_devisesFrom.setCurrentText(deviseTo)
        self.combo_devisesTo.setCurrentText(deviseFrom)

        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()