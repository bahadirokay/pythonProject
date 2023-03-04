from PIL import Image
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QLabel, QListWidget
from test_ui import Ui_AstrOkay
import os
import dbastrokay
from astropy.io import fits

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.listWidget = QListWidget(self)
        self.ui = Ui_AstrOkay()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        # Create the database
        dbastrokay.create_database()


        # Connect the signals to the appropriate slots
        self.ui.pushButton_2.clicked.connect(self.flat_frames)
        self.ui.pushButton.clicked.connect(self.light_frame)
        self.ui.pushButton_3.clicked.connect(self.dark_frames)
        self.ui.pushButton_4.clicked.connect(self.darkflat_frames)
        self.ui.pushButton_5.clicked.connect(self.bias_frames)
        self.ui.pushButton_16.clicked.connect(self.mother_frames)
        self.ui.pushButton_20.clicked.connect(self.masterflat_frames)
        self.ui.pushButton_21.clicked.connect(self.masterdark_frames)
        self.ui.pushButton_32.clicked.connect(self.masterflat_frames)
        self.ui.pushButton_33.clicked.connect(self.masterbias_frames)

    def list_files(self):
        self.listWidget.clear()
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG')):
                self.listWidget.addItem(file)


    def light_frame(self):
        pass

    def flat_frames(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder', '/')
        if folder_path:
            self.folder_path = folder_path
            images = os.listdir(self.folder_path)
            for image in images:
                if image.endswith((".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG", ".fits")):
                    file_path = os.path.join(folder_path, image)
                    file_info = (image, file_path)
                    if image.endswith(".fits"):
                        file_size_width = fits.getval(file_path, 'NAXIS1')
                        file_size_height = fits.getval(file_path, 'NAXIS2')
                        file_info += (file_size_width, file_size_height)
                    else:
                        with Image.open(file_path) as img:
                            flat_frame = np.array(img)
                        file_info += (flat_frame.shape[1], flat_frame.shape[0])
                    if self.ui.pushButton_2.isChecked():
                        dbastrokay.add_data('FlatFrame', file_info)
                        flat_frames_count = len(dbastrokay.get_data('FlatFrame'))
                        self.ui.lcdNumber_2.display(flat_frames_count)
                    else:
                        print("Flat frames not checked, skipping file: ", file_info[0])

    def dark_frames(self):
        pass
    def darkflat_frames(self):
        pass
    def bias_frames(self):
        pass
    def mother_frames(self):
        pass
    def masterdarkflat_frames(self):
        pass
    def masterdark_frames(self):
        pass
    def masterflat_frames(self):
        pass
    def masterbias_frames(self):
        pass



if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()




