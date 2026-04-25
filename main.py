from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
import os

app = QApplication([])
main_win = QWidget()
main_win.resize(600, 300)
main_win.setWindowTitle('Easy editor')

kartinka = QLabel('Картинка')
btn_dir = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_rezkoct = QPushButton('Резкость')
btn_BG = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton('Сбросить фильтры')
list_notes = QListWidget()

line1 = QVBoxLayout()
line1.addWidget(btn_dir)
line1.addWidget(list_notes)

line2 = QHBoxLayout()
line2.addWidget(btn_left)
line2.addWidget(btn_right)
line2.addWidget(btn_mirror)
line2.addWidget(btn_rezkoct)
line2.addWidget(btn_BG)
line2.addWidget(btn_reset)
line2.addWidget(btn_save)

line3 = QVBoxLayout()
line3.addWidget(kartinka)
line3.addLayout(line2)

line4 = QHBoxLayout()
line4.addLayout(line1)
line4.addLayout(line3)

main_win.setLayout(line4)

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
               result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_notes.clear()
    for filename in filenames:
        list_notes.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.original_image = None  
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        ''' при загрузке запоминаем путь и имя файла '''
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()  

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = kartinka.width(), kartinka.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        kartinka.setPixmap(scaled_pixmap)
        kartinka.setVisible(True)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        return image_path  

    def do_bw(self):
        if self.image:
            self.image = self.image.convert('L')
            image_path = self.saveImage()
            self.showImage(image_path)

    def do_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90)
            image_path = self.saveImage()  
            self.showImage(image_path)

    def do_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270)
            image_path = self.saveImage()  
            self.showImage(image_path)

    def do_mirror(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            image_path = self.saveImage()  
            self.showImage(image_path)
    
    def do_sharped(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            image_path = self.saveImage()  
            self.showImage(image_path)

    def reset_filter(self):
        if self.image and self.original_image:
            self.image = self.original_image.copy()  
            image_path = os.path.join(self.dir, self.filename)
            self.showImage(image_path)

def ShowChosenImage():
    if list_notes.currentRow() >= 0 and workdir:
        filename = list_notes.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)

list_notes.currentRowChanged.connect(ShowChosenImage)

workimage = ImageProcessor()

# Подключаем кнопки
btn_BG.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_rezkoct.clicked.connect(workimage.do_sharped)
btn_reset.clicked.connect(workimage.reset_filter)


btn_save.clicked.connect(workimage.saveImage)

main_win.show()
app.exec()
