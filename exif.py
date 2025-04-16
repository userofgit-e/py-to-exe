from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys
import tkinter as tk
from tkinter import filedialog


def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction in ["S", "W"]:
        decimal_degrees *= -1
    return decimal_degrees


def create_google_maps_url(gps_coords):
    lat = convert_decimal_degrees(*gps_coords["lat"], gps_coords["lat_ref"])
    lon = convert_decimal_degrees(*gps_coords["lon"], gps_coords["lon_ref"])
    return f"https://maps.google.com/?q={lat},{lon}"


def extract_exif_data(file_path):
    gps_coords = {}
    try:
        image = Image.open(file_path)
        print(f"\n{'='*20} {file_path} {'='*20}")
        if image._getexif() is None:
            print("No EXIF data found.")
            return
        for tag, value in image._getexif().items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for key, val in value.items():
                    readable_key = GPSTAGS.get(key, key)
                    print(f"{readable_key} - {val}")
                    if readable_key == "GPSLatitude":
                        gps_coords["lat"] = val
                    elif readable_key == "GPSLongitude":
                        gps_coords["lon"] = val
                    elif readable_key == "GPSLatitudeRef":
                        gps_coords["lat_ref"] = val
                    elif readable_key == "GPSLongitudeRef":
                        gps_coords["lon_ref"] = val
            else:
                print(f"{tag_name} - {value}")

        if gps_coords:
            print("Google Maps URL:", create_google_maps_url(gps_coords))

    except Exception as e:
        print(f"Error reading {file_path}: {e}")


def main():
    # Ask for output destination
    output_choice = input("Output destination:\n1 - File\n2 - Terminal\nEnter choice: ").strip()
    if output_choice == "1":
        sys.stdout = open("exif_output.txt", "w")

    # Use a file dialog to choose images
    tk.Tk().withdraw()
    files = filedialog.askopenfilenames(title="Select image files", filetypes=[("Image Files", "*.jpg *.jpeg *.tiff")])

    if not files:
        print("No files selected.")
        return

    for file in files:
        extract_exif_data(file)

    if output_choice == "1":
        sys.stdout.close()


if __name__ == "__main__":
    main()
