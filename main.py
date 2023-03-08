#Fotoğrafları açmak için gerekli kütüphane PILLOW
from PIL import Image
#png, jpg uzantılı resimleri ölçeklendirmek için ve ölçülerini okumak için Numpy
import numpy as np
#Arayüz, Tasarım ile alakalı kütüphane PyQt6(Pencere, Buton, kutucuklar vs işlemler için gerekli)
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QLabel, QListWidget, \
    QMessageBox, QDialog, QCheckBox

import processing
#Arayüzün bulunduğu py dosyası ve sınıfı
from test_ui import Ui_AstrOkay
#Dosya yolları ve listeleme ile ve değişiklikleri ile iligli kütüphane
import os
#Veritabanımınızın olduğu python dosyası
import dbastrokay
#Fits uzantılı resimleri okumak, ölçmek ve işlemek için kullanılan kütüphane
from astropy.io import fits
#Buton işlevlerini tanımlamak için oluşturduğum fonksiyonları barındıran python dosyası.
import buttons
from processing import flat_processing, dark_processing, dark_flat_processing, light_frame_processing, bias_processing


"""Uygulamayının çalışmasını, tasarımda bulunan işlevlerin etkinliğini sağlayan sınıf."""
class MyMainWindow(QMainWindow):
    """# test_ui.py dosyasında bulunan dosyaları almak için oluşturulan sınıf"""
    def __init__(self):
        # self parametresi kullanan fonksiyonları çekiyoruz
        super().__init__()
        self.listWidget = QListWidget(self)
        self.ui = Ui_AstrOkay()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        #Database oluştur. (Gerekli fonksiyonlar dbastrokay.py'da)
        dbastrokay.create_database()
        #Frame Fonksiyonların buton ataması(buttons.py)
        buttons.frame_button(self)
        #Program açıldığında LCD numararalı güncelle.
        buttons.lcd(self)
        #Clean butunların buton ataması
        buttons.clean_button(self)
        #Start Project Butonunun ataması
        buttons.start_button(self)



    """Bu fonkisyonda yazılan yorum satırlar diğer Frame fonksiyonu için de geçerlidir.
            Uygulamada LigtFrame Butonuna tıkladığında işlem yapılacak fonksiyon."""
    def light_frames(self):
        #Butona tıkladığında Klasör seçmek için açılır pencere ata
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder', '/')
        # Klasör yolunu bul ve listele, resimleri seç, ölç, dosya yolu ve adıyla veritabanına gönder.
        #Klasör seçilirse...
        if folder_path:
            #Klasör yolunu bul.
            self.folder_path = folder_path
            # Klasördeki veriler listele.(Dosya adı vs)
            images = os.listdir(self.folder_path)
            #Klasörde resim varsa...
            for image in images:
                #İstediğimi uzantıları ayıklama
                if image.endswith((".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG", ".fits")):
                    #Belirlediğimiz resim uzantıları varsa dosya yolunu ilgili değişkene ekle
                    file_path = os.path.join(folder_path, image)
                    #resim yüksekliği ve genişliğini daha sonra eklemek için bir değişken oluştur.
                    file_info = (image, file_path)
                    # Fits uzantılı resimlerin yükseklik ve genişliğini ölç (astropy)
                    if image.endswith(".fits"):
                        #dosya yolu bilinen fits uzantılı resimleri yükseliğini ve genişliğini ölç
                        file_size_width = fits.getval(file_path, 'NAXIS1')
                        file_size_height = fits.getval(file_path, 'NAXIS2')
                        #Ölçülen veriyi yukarda oluşturduğun değişkene ekle
                        file_info += (file_size_width, file_size_height)
                        # 4 veri içeren değişkendekindeki bilgileri veritabanına gönder.(db bilgileri - dbastrokay.py)
                        dbastrokay.add_data('LightFrame', file_info)
                    #png ve diğer resimleri...
                    else:
                        #Pillow kütüphanesi ile fotoğrafı açıyoruz.
                        with Image.open(file_path) as img:
                            #Numpy Kütüphanesi ile fotoğrafı ölç. ve veritabanına gönder
                            light_frame = np.array(img)
                            file_info += (light_frame.shape[1], light_frame.shape[0])
                            #Veritabanına veriyi gönder(Veritabanı fonkisyonları dbastrokay.py dosyasında)
                            dbastrokay.add_data('LightFrame', file_info)
                    # Lcd butonu veri girişinden sonra güncelle.(Detay buttons.py'da)
                    buttons.lcd(self)

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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('FlatFrame', file_info)
                            buttons.lcd(self)

    def dark_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('DarkFrame', file_info)
                            buttons.lcd(self)

    def darkflat_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('DarkFlatFrame', file_info)
                            buttons.lcd(self)

    def bias_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('BiasFrame', file_info)
                            buttons.lcd(self)

    def mother_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('MotherFrame', file_info)
                            buttons.lcd(self)

    def master_darkflat_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('MasterDarkFlatFrame', file_info)
                            buttons.lcd(self)

    def master_dark_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('MasterDarkFrame', file_info)
                            buttons.lcd(self)

    def master_flat_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('MasterFlatFrame', file_info)
                            buttons.lcd(self)

    def master_bias_frames(self):
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
                            frame = np.array(img)
                            file_info += (frame.shape[1], frame.shape[0])
                            dbastrokay.add_data('MasterBiasFrame', file_info)
                    buttons.lcd(self)



    """Bu fonkisyondaki yorum satırı diğer delete fonkisyonı içinde geçerlidir."""
    #Clean butonu ile veri sil.
    def delete_light(self):
        #Light Frame alanındaki clean butonuna basıldığında database'deki ilgili veriyi sil.
        dbastrokay.delete_table('LightFrame')
        #Lcd butonunu veri silme işleminden sonra güncelle.
        buttons.lcd(self)
    def delete_flat(self):
        dbastrokay.delete_table('FlatFrame')
        buttons.lcd(self)
    def delete_dark(self):
        dbastrokay.delete_table('DarkFrame')
        buttons.lcd(self)
    def delete_darkflat(self):
        dbastrokay.delete_table('DarkFlatFrame')
        buttons.lcd(self)
    def delete_bias(self):
        dbastrokay.delete_table('BiasFrame')
        buttons.lcd(self)
    def delete_mother(self):
        dbastrokay.delete_table('MotherFrame')
        buttons.lcd(self)
    def delete_masterflat(self):
        dbastrokay.delete_table('MasterFlatFrame')
        buttons.lcd(self)
    def delete_masterdark(self):
        dbastrokay.delete_table('MasterDarkFrame')
        buttons.lcd(self)
    def delete_masterdarkflat(self):
        dbastrokay.delete_table('MasterDarkFlatFrame')
        buttons.lcd(self)
    def delete_masterbias(self):
        dbastrokay.delete_table('MasterBiasFrame')
        buttons.lcd(self)


    def start_button(self):
        processing.dark_processing()
        processing.flat_processing()
        processing.bias_processing()
        processing.dark_flat_processing()
        processing.light_frame_processing()

    """Henüz işlevi yok."""
    def list_files(self):
        self.listWidget.clear()
        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG')):
                self.listWidget.addItem(file)

    """Henüz işlevi yok."""
    def showEvent(self, event):
        super().showEvent(event)
        buttons.lcd(self)

    """Program kapatıldığında Çıkmak istediğine emin misin sorusunu sorar"""

    def closeEvent(self, event):
        # Mesaj kutusunda çıkmak isteyip istemediğini soran kutucuk aç.
        reply = QMessageBox.question(self, 'Message', 'Do you want to exit by saving the data?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        # Cevap evet ise databasedeki tüm veriyi sil.
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.accept()
            dbastrokay.delete_db()

    """Programın görsel olarak çalıştır"""
if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()


