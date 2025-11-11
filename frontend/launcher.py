import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel, QStackedWidget

class DifficultyPage(QWidget):
    def __init__(self, navigate_callback):
        super().__init__()
        self.navigate_callback = navigate_callback

        layout = QVBoxLayout()
        label = QLabel("Select Difficulty Level")
        layout.addWidget(label)

        # Buttons for difficulty
        beginner_btn = QPushButton("Beginner")
        beginner_btn.clicked.connect(lambda: self.navigate_callback("Beginner"))
        layout.addWidget(beginner_btn)

        intermediate_btn = QPushButton("Intermediate")
        intermediate_btn.clicked.connect(lambda: self.navigate_callback("Intermediate"))
        layout.addWidget(intermediate_btn)

        gaming_btn = QPushButton("Gaming")
        gaming_btn.clicked.connect(lambda: self.navigate_callback("Gaming"))
        layout.addWidget(gaming_btn)

        self.setLayout(layout)


class GestureMousePage(QWidget):
    def __init__(self, difficulty):
        super().__init__()
        self.difficulty = difficulty
        self.process = None

        layout = QVBoxLayout()
        self.label = QLabel(f"Gesture Mouse - {self.difficulty} Mode")
        layout.addWidget(self.label)

      
        self.start_button = QPushButton("Run Gesture Mouse")
        self.start_button.clicked.connect(self.run_gesture_mouse)
        layout.addWidget(self.start_button)

    
        self.stop_button = QPushButton("Stop Gesture Mouse")
        self.stop_button.clicked.connect(self.stop_gesture_mouse)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def run_gesture_mouse(self):
        if self.process is None:
        
            self.process = subprocess.Popen(["python", "../AI_virtual_Mouse.py"])
            self.label.setText(f"Gesture Mouse running - {self.difficulty} Mode")
        else:
            self.label.setText("Gesture Mouse is already running!")

    def stop_gesture_mouse(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.label.setText(f"Gesture Mouse stopped - {self.difficulty} Mode")
        else:
            self.label.setText("Gesture Mouse is not running.")


class MouseLauncher(QStackedWidget):
    def __init__(self):
        super().__init__()

         
        self.difficulty_page = DifficultyPage(self.navigate_to_gesture)
        self.addWidget(self.difficulty_page)
 
        self.gesture_page = None

        self.setWindowTitle("Gesture Mouse Launcher")
        self.setGeometry(100, 100, 300, 250)

    def navigate_to_gesture(self, difficulty):
     
        self.gesture_page = GestureMousePage(difficulty)
        self.addWidget(self.gesture_page)
        self.setCurrentWidget(self.gesture_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseLauncher()
    window.show()
    sys.exit(app.exec_())
