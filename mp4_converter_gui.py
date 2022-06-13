# mp4_converter_gui.py

import cv2
import glob
import os
import shutil
import PySimpleGUI as sg

from PIL import Image

file_types = [("MP4 (*.mp4)", "*.mp4"), ("All files (*.*)", "*.*")]

#conversion des videos en  Frame

def convert_mp4_to_jpgs(C:\Users\mohamedsori.alhousse\Music\videos\4Keus Feat. Niska - M.D(480P).mp4):
    video_capture = cv2.VideoCapture(C:\Users\mohamedsori.alhousse\Music\videos\4Keus Feat. Niska - M.D(480P).mp4)
    still_reading, image = video_capture.read()
    frame_count = 0
    if os.path.exists("C:\Users\mohamedsori.alhousse\Music\mes gifts")
        shutil.rmtree("C:\Users\mohamedsori.alhousse\Music\mes gifts")
    try:
        os.mkdir("C:\Users\mohamedsori.alhousse\Music\mes gifts")
    except IOError:
        sg.popup("Error occurred creating output folder")
        return

    while still_reading:
        cv2.imwrite(f"C:\Users\mohamedsori.alhousse\Music\mes gifts/frame_{frame_count:05d}.jpg", image)

        # lis l'image suivante

        still_reading, image = video_capture.read()
        frame_count += 1

        #Effectue la transformation en gift

def make_gif(gif_path, frame_folder="C:\Users\mohamedsori.alhousse\Music\mes gifts"):
    images = glob.glob(f"{C:\Users\mohamedsori.alhousse\Music\mes gifts}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(gif_path, format="GIF", append_images=frames,save_all=True, duration=50, loop=0)

# Mise en place de l'interface graphique

def main():
    layout = [
        [
            sg.Text("MP4 File"),
            sg.Input(size=(25, 1), key="-FILENAME-", disabled=True),
            sg.FileBrowse(file_types=file_types),
        ],
        [
            sg.Text("GIF File Save Location"),
            sg.Input(size=(25, 1), key="-C:\Users\mohamedsori.alhousse\Music\mes gifts-", disabled=True),
            sg.SaveAs(file_types=file_types),

        ],
        [sg.Button("Convert to GIF")],
    ]

    window = sg.Window("MP4 to GIF Converter", layout)

    while True:
        event, values = window.read()
        mp4_path = values["-C:\Users\mohamedsori.alhousse\Music\videos\4Keus Feat. Niska - M.D(480P).mp4-"]
        gif_path = values["-C:\Users\mohamedsori.alhousse\Music\mes gifts-"]
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event in ["Convert to GIF"]:
            if mp4_path and gif_path:
                convert_mp4_to_jpgs(mp4_path)
                make_gif(gif_path)
                sg.popup(f"GIF created: {C:\Users\mohamedsori.alhousse\Music\mes gifts}")

    window.close()


if __name__ == "__main__":
    main()