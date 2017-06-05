import sys
import os
import argparse
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Application(QWidget):
    def __init__(self, parent=None):
        super(Application, self).__init__(parent)

        image_label = QLabel("Image(s):")
        self.files_line = QLineEdit()
        self.files_button = QPushButton("&Browse...")

        files_layout = QHBoxLayout()
        files_layout.addWidget(image_label)
        files_layout.addWidget(self.files_line)
        files_layout.addWidget(self.files_button)

        self.files_button.clicked.connect(self.browse)

        width_label = QLabel("Max width:")
        height_label = QLabel("Max height:")

        self.width_line = QLineEdit()
        self.height_line = QLineEdit()

        resize_button = QPushButton("&Resize")
        resize_button.clicked.connect(self.resize)

        dimensions_layout = QHBoxLayout()
        dimensions_layout.addWidget(width_label)
        dimensions_layout.addWidget(self.width_line)
        dimensions_layout.addWidget(height_label)
        dimensions_layout.addWidget(self.height_line)
        dimensions_layout.addWidget(resize_button)

        mainLayout = QGridLayout()
        mainLayout.addLayout(files_layout, 0, 0)
        mainLayout.addLayout(dimensions_layout, 1, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle("Resize image(s)")

    def browse(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select image(s)", "",
                                                "Images (*.jpg *.bmp *.png)")
        self.files_line.setText(';'.join(files))

    def resize(self):
        files = self.files_line.text().split(';')
        files = [path for path in files if len(path) > 0]

        if not files:
            self.show_warning("Choose images to resize!")
        elif not all((os.path.exists(path) or path == '') for path in files):
            self.show_warning("Incorrect path!")
        elif not (self.width_line.text() and self.height_line.text()):
            self.show_warning("Set maximum width and height!")
        elif not (self.width_line.text().isdecimal() and self.height_line.text().isdecimal()):
            self.show_warning("Width and height must be positive integer numbers!")
        else:
            try:
                main(self.width_line.text(), self.height_line.text(), files)
                self.show_info("Successfully resized images!")
            except:
                self.show_warning("Error while resizing images!")

    def show_warning(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.exec_()

    def show_info(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec_()

def main(max_width, max_height, paths):
    for path in paths:
        file = open(path, 'rb')
        img = Image.open(file)

        width, height = img.size
        ratio = min(float(max_width)/width, float(max_height)/height)
        new_width = int(ratio * width)
        new_height = int(ratio * height)

        img = img.resize((new_width, new_height))

        filename, extension = os.path.splitext(path)
        new_path = filename + '_resized' + extension
        img.save(new_path)

        file.close()


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('width', nargs='?', default='-1')
    arg_parser.add_argument('height', nargs='?', default='-1')
    arg_parser.add_argument('image_path', nargs='*')
    args = arg_parser.parse_args()

    if args.width != '-1' and not args.image_path:
        print("error: no image path")
        sys.exit(1)

    return args.width, args.height, args.image_path


if __name__ == '__main__':
    max_width, max_height, paths = parse_args()

    if max_width != '-1':
        main(max_width, max_height, paths)
    else:
        app = QApplication(sys.argv)

        window = Application()
        window.setGeometry(500, 400, 500, 100)
        window.show()

        sys.exit(app.exec_())
