import numpy as np
from PIL import Image
from astropy.io import fits
import dbastrokay
import os



def flat_processing(database_file_path):
    ''''İşlem Adımları:

    Veritabanındaki tüm Flat Frame dosya yollarını al.
    Her bir Flat Frame için aşağıdaki işlemleri yap:
    Dosya yolu ve boyut bilgilerini al.
    .fits uzantılı dosyaları oku ve flat_frame_data değişkenine at.
    .png veya .jpg uzantılı dosyaları oku ve flat_frame_data değişkenine at.
    Flat Frame'i normalize et.
    Flat Frame'i kaydet.'''

    # Veritabanındaki Flat Frame dosya yollarını al
    flat_frames = dbastrokay.get_data('FlatFrame', database_file_path)

    # Flat Frame'leri topla ve normalize et
    master_flat = np.zeros((flat_frames[0][3], flat_frames[0][2]), dtype=np.float32)
    for flat_frame in flat_frames:
        # Dosya yolu ve boyut bilgilerini al
        file_path = flat_frame[1]
        file_size_width = flat_frame[2]
        file_size_height = flat_frame[3]

        # .fits uzantılı dosyaları oku
        if file_path.endswith('.fits'):
            with fits.open(file_path) as hdul:
                flat_frame_data = hdul[0].data.astype(np.float32)

        # .png veya .jpg uzantılı dosyaları oku
        else:
            with Image.open(file_path) as img:
                flat_frame_data = np.array(img).astype(np.float32)

        # Flat Frame'i normalize et
        flat_frame_normalized = flat_frame_data / np.mean(flat_frame_data)

        # Flat Frame'leri birleştir
        master_flat += flat_frame_normalized

    # Master Flat'i normalize et
    master_flat /= len(flat_frames)

    # Master Flat'i kaydet
    np.save("master_flat.npy", (dbastrokay.add_data('MasterFlat')))


def dark_processing(database_file_path):
    # Veritabanındaki Dark Frame dosya yollarını al
    dark_frames = dbastrokay.get_data('DarkFrame', database_file_path)

    # Dark Frame'leri işle
    for dark_frame in dark_frames:
        # Dosya yolu ve boyut bilgilerini al
        file_path = dark_frame[1]
        file_size_width = dark_frame[2]
        file_size_height = dark_frame[3]

        # .fits uzantılı dosyaları oku
        if file_path.endswith('.fits'):
            with fits.open(file_path) as hdul:
                dark_frame_data = hdul[0].data.astype(np.float32)

        # .png veya .jpg uzantılı dosyaları oku
        else:
            with Image.open(file_path) as img:
                dark_frame_data = np.array(img).astype(np.float32)

        # Dark Frame'i normalize et
        dark_frame_normalized = dark_frame_data / np.mean(dark_frame_data)

        # Normalized dark frame'i kaydet
        dark_frame_name = f"normalized_dark_{file_size_width}x{file_size_height}.npy"
        np.save(dark_frame_name, dark_frame_normalized)

    # Normalize edilmiş tüm dark frame'leri oku ve topla
    normalized_dark_frames = []
    for dark_frame in dark_frames:
        file_path = dark_frame[1]
        file_size_width = dark_frame[2]
        file_size_height = dark_frame[3]

        # Normalized dark frame'i yükle
        normalized_dark_frame_name = f"normalized_dark_{file_size_width}x{file_size_height}.npy"
        normalized_dark_frame = np.load(normalized_dark_frame_name)

        # Toplam listesine ekle
        normalized_dark_frames.append(normalized_dark_frame)

    # Normalize edilmiş tüm dark frame'leri topla
    master_dark_frame_normalized = np.mean(normalized_dark_frames, axis=0)

    # Master dark frame'i kaydet
    master_dark_frame_name = "master_dark_frame.npy"
    np.save(master_dark_frame_name, master_dark_frame_normalized)

def dark_flat_processing(database_file_path):
    """
    Veritabanındaki Flat Frame ve Dark Frame'leri kullanarak Dark Flat'i oluşturur.

    Parameters
    ----------
    database_file_path : str
        Veritabanı dosyasının yolu.

    Returns
    -------
    dark_flat : numpy.ndarray
        Oluşturulan Dark Flat verisi.
    """

    # Veritabanındaki Flat Frame dosya yollarını al
    flat_frames = dbastrokay.get_data('FlatFrame', database_file_path)

    # Veritabanındaki Dark Frame dosya yollarını al
    dark_frames = dbastrokay.get_data('DarkFrame', database_file_path)

    # Flat Frame'leri işle
    flat_data_list = []
    for flat_frame in flat_frames:
        # Dosya yolu ve boyut bilgilerini al
        file_path = flat_frame[1]
        file_size_width = flat_frame[2]
        file_size_height = flat_frame[3]

        # .fits uzantılı dosyaları oku
        if file_path.endswith('.fits'):
            with fits.open(file_path) as hdul:
                flat_frame_data = hdul[0].data.astype(np.float32)

        # .png veya .jpg uzantılı dosyaları oku
        else:
            with Image.open(file_path) as img:
                flat_frame_data = np.array(img).astype(np.float32)

        # Flat Frame'i normalize et
        flat_frame_normalized = flat_frame_data / np.mean(flat_frame_data)

        # Boyutları uyumlu hale getir
        flat_frame_resized = np.array(Image.fromarray(flat_frame_normalized).resize((file_size_width, file_size_height)))

        flat_data_list.append(flat_frame_resized)

    # Tüm Flat Frame'leri birleştir ve ortalamasını alarak Master Flat'i oluştur
    master_flat = np.mean(flat_data_list, axis=0)

    # Dark Frame'leri işle
    dark_data_list = []
    for dark_frame in dark_frames:
        # Dosya yolu ve boyut bilgilerini al
        file_path = dark_frame[1]
        file_size_width = dark_frame[2]
        file_size_height = dark_frame[3]

        # .fits uzantılı dosyaları oku
        if file_path.endswith('.fits'):
            with fits.open(file_path) as hdul:
                dark_frame_data = hdul[0].data.astype(np.float32)

        # .png veya .jpg uzantılı dosyaları oku
        else:
            with Image.open(file_path) as img:
                dark_frame_data = np.array(img).astype(np.float32)

        # Boyutları uyumlu hale getir
        dark_frame_resized = np.array(Image.fromarray(dark_frame_data).resize((file_size_width, file_size_height)))

        dark_data_list.append(dark_frame_resized)

    # Tüm Dark Frame'leri birleştir ve ortalamasını alarak Master Dark'ı oluştur
    master_dark = np.mean(dark_data_list, axis=0)


    # Master Flat'i Master Dark ile bölerek Dark Flat'i oluştur
    dark_flat = master_flat / master_dark

    # Dark Flat'i fits formatında kaydet
    hdu = fits.PrimaryHDU(dark_flat)
    hdu.writeto(output_path, overwrite=True)

    return dark_flat

def bias_processing(database_file_path, output_path):
    """
    Veritabanındaki Bias Frame'leri kullanarak Master Bias'i oluşturur ve fits formatında kaydeder.

    Parameters
    ----------
    database_file_path : str
        Veritabanı dosyasının yolu.
    output_path : str
        Kaydedilecek Master Bias dosyasının yolu.

    Returns
    -------
    master_bias : numpy.ndarray
        Oluşturulan Master Bias verisi.
    """

    # Veritabanındaki Bias Frame dosya yollarını al
    bias_frames = dbastrokay.get_data('BiasFrame', database_file_path)

    # Bias Frame'leri işle
    bias_data_list = []
    for bias_frame in bias_frames:
        # Dosya yolu ve boyut bilgilerini al
        file_path = bias_frame[1]
        file_size_width = bias_frame[2]
        file_size_height = bias_frame[3]

        # .fits uzantılı dosyaları oku
        if file_path.endswith('.fits'):
            with fits.open(file_path) as hdul:
                bias_frame_data = hdul[0].data.astype(np.float32)

        # .png veya .jpg uzantılı dosyaları oku
        else:
            with Image.open(file_path) as img:
                bias_frame_data = np.array(img).astype(np.float32)

        # Boyutları uyumlu hale getir
        bias_frame_resized = np.array(Image.fromarray(bias_frame_data).resize((file_size_width, file_size_height)))

        bias_data_list.append(bias_frame_resized)

    # Tüm Bias Frame'leri birleştir ve ortalamasını alarak Master Bias'i oluştur
    master_bias = np.mean(bias_data_list, axis=0)

    # Master Bias'i fits formatında kaydet
    hdu = fits.PrimaryHDU(master_bias)
    hdu.writeto(output_path, overwrite=True)

    return master_bias

def light_frame_processing(database_file_path, output_path):
    """
    Veritabanındaki Light Frame'leri işleyerek, Master Dark, Master Flat, Dark Flat ve Master Bias kullanarak işlenmiş
    verileri kaydeder.

    Parameters
    ----------
    database_file_path : str
        Veritabanı dosyasının yolu.
    output_path : str
        İşlenmiş verilerin kaydedileceği klasörün yolu.

    Returns
    -------
    processed_data : list
        İşlenmiş verilerin dosya yollarını içeren bir liste.
    """

    # Veritabanından LightFrame'leri al
    light_frames = dbastrokay.get_data('LightFrame', database_file_path)

    processed_data = []

    # Master Dark'ı al
    master_dark_file_path = dbastrokay.get_master_file_path('DarkFrame', database_file_path)
    with fits.open(master_dark_file_path) as hdul:
        master_dark = hdul[0].data.astype(np.float32)

    # Master Flat'ı al
    master_flat_file_path = dbastrokay.get_master_file_path('FlatFrame', database_file_path)
    with fits.open(master_flat_file_path) as hdul:
        master_flat = hdul[0].data.astype(np.float32)

    # Dark Flat'ı al
    dark_flat_file_path = os.path.join(output_path, 'dark_flat.fits')
    with fits.open(dark_flat_file_path) as hdul:
        dark_flat = hdul[0].data.astype(np.float32)

    # Master Bias'ı al
    master_bias_file_path = dbastrokay.get_master_file_path('BiasFrame', database_file_path)
    with fits.open(master_bias_file_path) as hdul:
        master_bias = hdul[0].data.astype(np.float32)

    # LightFrame'leri işle
    for light_frame in light_frames:
        # Dosya yolu ve boyut bilgilerini al
        file_path = light_frame[1]
        file_size_width = light_frame[2]
        file_size_height = light_frame[3]

        # .fit uzantılı dosyaları oku
        if file_path.endswith('.fit'):
            with fits.open(file_path) as hdul:
                light_frame_data = hdul[0].data.astype(np.float32)

        # .png, .jpg gibi resim dosyaları oku
        else:
            image = Image.open(file_path)
            light_frame_data = np.array(image).astype(np.float32)

        # Dark Frame'i çıkar
        light_frame_data -= master_dark

        # Flat Field'ı uygula
        light_frame_data -= master_bias
        light_frame_data /= master_flat
        light_frame_data *= np.median(master_flat)

        # Dark Flat'ı uygula
        light_frame_data /= dark_flat

        # 0-1 arasına normalize et
        light_frame_data /= np.max(light_frame_data)

        # İşlenmiş veriyi kaydet
        file_name = os.path.basename(file_path)
        output_file_path = os.path.join(output_path, 'processed_'+file_name)

        # Eğer dosya .fits uzantılı ise
        if file_path.endswith('.fits'):
            hdul[0].data = light_frame_data
            hdul.writeto(output_file_path, overwrite=True)
        else:
            # Resim dosyaları için kayıt işlemi
            im = Image.fromarray(light_frame_data.astype('uint8'))
            im.save(output_file_path)

        # İşlenmiş verinin dosya yolunu listeye ekle
        processed_data.append(output_file_path)

        return processed_data

