from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from security import SecurityManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MIM Secret Diary")
        self.setMinimumSize(800, 600)
        
        # Initialize security
        self.security = SecurityManager()
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        # Add UI elements
        self.title_label = QLabel("Welcome to MIM Secret Diary")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Write your thoughts here...")
        self.layout.addWidget(self.text_editor)
        
        self.save_button = QPushButton("Save Entry")
        self.layout.addWidget(self.save_button)
        
        # Connect signals
        self.save_button.clicked.connect(self.save_entry)
        
    def save_entry(self):
        content = self.text_editor.toPlainText()
        # TODO: Implement save functionality
        print("Entry saved:", content)
