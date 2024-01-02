import sys
import random
from openai import OpenAI


from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

OPEN_API_KEY = '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'  # 替换为你的 OpenAI API 密钥
client = OpenAI(api_key=OPEN_API_KEY)

class DesktopPet(QWidget):
    def __init__(self, image_files):
        super().__init__()
        self.image_files = image_files
        self.fly_image = QPixmap('fly.png')  # 加载飞行姿态的图像
        self.initUI()
        self.change_image()

    def initUI(self):
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label.mouseMoveEvent = self.on_drag
        self.label.mouseReleaseEvent = self.on_release
        self.label.mousePressEvent = self.on_pet_click

    def on_pet_click(self, event):
        self.send_message_to_gpt("你好")

    def send_message_to_gpt(self, message):
        try:
            response = client.chat.completions.create(model="gpt-4-vision-preview",  # 替换为你的模型 ID
            messages=[{"role":"system", "content": message}],
            max_tokens=50)
            gpt_response = response.choices[0].message.content
            print(gpt_response)
            QMessageBox.information(self, "GPT Response", gpt_response)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def on_drag(self, event):
        self.label.setPixmap(self.fly_image)
        self.move(event.globalPos() - self.drag_position)
        event.accept()

    def on_release(self, event):
        self.change_image()

    def on_press(self, event):
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def change_image(self):
        image_path = random.choice(self.image_files)
        self.label.setPixmap(QPixmap(image_path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_paths = ['stand.png', 'turn.png', 'fly.png']
    ex = DesktopPet(image_paths)
    ex.show()
    sys.exit(app.exec_())
