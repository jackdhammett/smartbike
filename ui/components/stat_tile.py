from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatTile(QWidget):
    def __init__(self, label_text, value_text):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel(label_text)
        self.label.setObjectName("stat_label")

        self.value = QLabel(value_text)
        self.value.setObjectName("stat_value")

        layout.addWidget(self.label)
        layout.addWidget(self.value)

        self.setLayout(layout)

    def update_value(self, text):
        self.value.setText(text)
