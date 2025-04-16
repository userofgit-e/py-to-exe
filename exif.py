import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    return decimal_degrees * (-1 if direction in ["S", "W"] else 1)


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
    # Default to terminal output unless "--file" is passed
    save_to_file = "--file" in sys.argv

    if save_to_file:
        sys.stdout = open("exif_output.txt", "w")

    # Use file dialog if no files are passed via CLI
