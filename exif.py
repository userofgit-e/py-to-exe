import os 
from PIL import Image
import piexif

def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = piexif.load(img.info.get('exif', b''))
        formatted_data = {}

        # معلومات أساسية
        zeroth_ifd = exif_data["0th"]
        exif_ifd = exif_data["Exif"]
        gps_ifd = exif_data["GPS"]

        # اسم الكاميرا
        if piexif.ImageIFD.Make in zeroth_ifd:
            formatted_data['Camera Make'] = zeroth_ifd[piexif.ImageIFD.Make].decode()
        if piexif.ImageIFD.Model in zeroth_ifd:
            formatted_data['Camera Model'] = zeroth_ifd[piexif.ImageIFD.Model].decode()

        # وقت وتاريخ
        if piexif.ExifIFD.DateTimeOriginal in exif_ifd:
            formatted_data['Date Taken'] = exif_ifd[piexif.ExifIFD.DateTimeOriginal].decode()

        # إعدادات التصوير
        if piexif.ExifIFD.ExposureTime in exif_ifd:
            formatted_data['Exposure Time'] = str(exif_ifd[piexif.ExifIFD.ExposureTime])
        if piexif.ExifIFD.FNumber in exif_ifd:
            formatted_data['Aperture'] = f"f/{exif_ifd[piexif.ExifIFD.FNumber][0] / exif_ifd[piexif.ExifIFD.FNumber][1]}"
        if piexif.ExifIFD.ISOSpeedRatings in exif_ifd:
            formatted_data['ISO'] = exif_ifd[piexif.ExifIFD.ISOSpeedRatings]

        # الموقع الجغرافي
        if gps_ifd:
            def convert_to_degrees(value):
                d, m, s = value
                return d[0]/d[1] + m[0]/m[1]/60 + s[0]/s[1]/3600

            lat = convert_to_degrees(gps_ifd[piexif.GPSIFD.GPSLatitude])
            lat_ref = gps_ifd[piexif.GPSIFD.GPSLatitudeRef].decode()
            lon = convert_to_degrees(gps_ifd[piexif.GPSIFD.GPSLongitude])
            lon_ref = gps_ifd[piexif.GPSIFD.GPSLongitudeRef].decode()

            if lat_ref == 'S': lat = -lat
            if lon_ref == 'W': lon = -lon

            formatted_data['GPS Latitude'] = lat
            formatted_data['GPS Longitude'] = lon

        return formatted_data
    except Exception as e:
        return {"Error": str(e)}

def extract_from_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".jpg", ".jpeg")):
            path = os.path.join(directory_path, filename)
            print(f"--- {filename} ---")
            data = get_exif_data(path)
            for key, value in data.items():
                print(f"{key}: {value}")
            print()

# استخدام:
extract_from_directory("path/to/your/images")
