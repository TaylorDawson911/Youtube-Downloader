# Importing necessary packages
import tkinter as tk
from tkinter import *
from pytube import YouTube
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import os
from tkinter.ttk import Progressbar
from pytube import Playlist

# Constants
lst = ['144p', '240p', '360p', '480p', '720p', '1080p', "audio"]
previousprogress = 0



# Defining CreateWidgets() function
# to create necessary tkinter widgets
def widgets():
    """ This function is used to create the tkinter widgets """
    global canvas, quality, video_options_frame, video_info_frame, video_info, bottom_frame, top_frame

    # Setting frames
    video_options_frame = Frame(root, bg="white")
    video_options_frame.grid(row=4,
                             column=0,
                             pady=0,
                             padx=0,
                             columnspan=3)

    video_info_frame = Frame(root, bg="white")
    video_info_frame.grid(row=3,
                          column=0,
                          pady=10,
                          padx=0,
                          columnspan=3)

    bottom_frame = Frame(root, bg="white")
    bottom_frame.grid(row=6,
                      column=0,
                      pady=10,
                      padx=0,
                      columnspan=3)

    top_frame = Frame(root, bg="white")
    top_frame.grid(row=2,
                   column=0,
                   pady=10,
                   padx=0,
                   columnspan=3)

    head_label = Label(top_frame, text="YouTube Video Downloader Using Tkinter",
                       padx=15,
                       pady=15,
                       font="SegoeUI 14",
                       fg="Black",
                       bg="white")
    head_label.pack(side=TOP, pady=10)

    link_label = Label(top_frame,
                       text="YouTube link :",
                       bg="white",
                       pady=5,
                       padx=5)
    link_label.pack(side=LEFT)

    root.linkText = Entry(top_frame,
                          width=35,
                          textvariable=video_Link,
                          font="Arial 14")
    root.linkText.pack(side=LEFT)

    get_video = Button(top_frame,
                       text="Get Video",
                       command=get_vid,
                       width=10,
                       bg="white",
                       pady=10,
                       padx=15,
                       relief=GROOVE,
                       font="Georgia, 13")
    get_video.pack(side=LEFT, padx=5)

    destination_label = Label(video_options_frame,
                              text="Set Video Options :",
                              bg="white",
                              pady=5,
                              padx=9)
    destination_label.pack(side=TOP)

    video_info = Label(video_info_frame,
                       text="Video Info:",
                       bg="white",
                       pady=5,
                       padx=9)

    video_info.pack(side=BOTTOM)

    browse_B = Button(video_options_frame,
                      text="Set File Path",
                      command=Browse,
                      width=10,
                      bg="white",
                      relief=GROOVE)
    browse_B.pack(side=LEFT)

    Download_B = Button(bottom_frame,
                        text="Download Video",
                        command=Download,
                        width=10,
                        bg="white",
                        pady=10,
                        padx=15,
                        relief=GROOVE,
                        font="Georgia, 13")
    Download_B.pack(side=BOTTOM, pady=5)


def get_vid():
    """ This function is used to get the video info """
    video_info.config(text="Getting Video Info")
    global lst
    url = video_Link.get()
    if "list" in url:
        playlist = Playlist(url)
        PlayListLinks = playlist.video_urls
        video_info.config(
            text=f"Playlist Detected\nNote: Once Download Started, Cannot Stop Unless Exited\nAmount Of Videos In "
                 f"Playlist: {len(PlayListLinks)}")

        return

    yt = YouTube(url)
    img_url = YouTube(url).thumbnail_url
    urllib.request.urlretrieve(img_url, "temp.png")
    image = Image.open("temp.png")
    image = image.resize((160, 120), Image.ANTIALIAS)  # Will probably need to remove this soon but i am very annoyed
    img2 = ImageTk.PhotoImage(image)
    panel.configure(image=img2)
    panel.image = img2
    os.remove("temp.png")

    resolution = [int(i.split("p")[0]) for i in
                  (list(dict.fromkeys([i.resolution for i in yt.streams if i.resolution])))]
    resolution.sort()

    quality['menu'].delete(0, 'end')

    for choice in resolution:
        choice = str(choice) + "p"
        quality['menu'].add_command(label=choice, command=tk._setit(var, choice))
    tempvar = "audio only"
    quality['menu'].add_command(label=tempvar, command=tk._setit(var, tempvar))
    info = f"Title\n{yt.title}" + "\n" + f"Channel\n{yt.author}" + "\n" + f"Video Length\n{(length := str(yt.length // 60))} minutes {yt.length % 60} seconds" + "\n" + f"Views\n{yt.views}"
    video_info.config(text=info)


# Defining Browse() to select a
# destination folder to save the video

def Browse():
    # Presenting user with a pop-up for
    # directory selection. initialdir
    # argument is optional Retrieving the
    # user-input destination directory and
    # storing it in downloadDirectory
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")

    # Displaying the directory in the directory
    # textbox
    download_Path.set(download_Directory)


# Defining Download() to download the video

def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        bar['value'] = liveprogress
        root.update()
        print(liveprogress)


def Download():
    bar['value'] = 0
    root.update()
    if "list" in video_Link.get():
        url = video_Link.get()
        playlist = Playlist(url)
        PlayListLinks = playlist.video_urls
        for i, link in enumerate(PlayListLinks):
            yt = YouTube(link)
            if var.get() == "audio":
                video = yt.streams.filter(only_audio=True).first()
                downloaded_file = video.download()
                base, ext = os.path.splitext(downloaded_file)

                new_file = base + '.mp3'
                if os.path.exists(new_file):
                    print("File already exists")
                else:
                    os.rename(downloaded_file, new_file)

            else:
                d_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                    'resolution').desc().first()
                d_video.download()

            print(i + 1, ' Video is Downloaded.')
            bar['value'] += 100 / len(PlayListLinks)
            root.update()

        return

    # getting user-input Youtube Link
    if var.get() == "audio only":
        video = YouTube(video_Link.get()).streams.filter(only_audio=True).first()
        downloaded_file = video.download()
        base, ext = os.path.splitext(downloaded_file)

        new_file = base + '.mp3'
        os.rename(downloaded_file, new_file)
    else:

        yt = YouTube(video_Link.get())
        resolution = var.get()
        yt.register_on_progress_callback(on_progress)
        yt.streams.filter(res=resolution).first().download()

    # select the optimal location for
    # saving file's
    download_Folder = download_Path.get()

    # Creating object of YouTube()

    # Displaying the message
    messagebox.showinfo("SUCCESSFULLY",
                        "DOWNLOADED AND SAVED IN\n"
                        + download_Folder)


def clock():
    root.after(1000, clock)


def main(arg):
    global video_Link, root, download_Path, panel, quality, var, bar
    # Creating object of tk class
    root = tk.Tk()
    var = tk.StringVar(root)

    # Setting the title, background color
    # and size of the tkinter window and
    # disabling the resizing property
    root.geometry("615x600")
    root.resizable(False, False)
    root.title("YouTube Video Downloader")
    root.config(background="white")

    # Creating the tkinter Variables
    video_Link = StringVar()
    download_Path = StringVar()
    widgets()

    quality = OptionMenu(video_options_frame, var, *lst, )

    quality.pack(side=LEFT, padx=5)

    img = ImageTk.PhotoImage(Image.open("Placeholder.png"))
    panel = tk.Label(video_info_frame, image=img, width=160, height=120)

    panel.pack(side=BOTTOM, padx=5)

    thumbnail = Label(video_info_frame,
                      text="Thumbnail",
                      bg="white",
                      pady=5,
                      padx=9)

    thumbnail.pack(side=TOP)

    bar = Progressbar(bottom_frame, orient=HORIZONTAL, length=300)
    bar.pack(side=TOP)

    # Calling the Widgets() function

    # Defining infinite loop to run
    # application
    clock()
    root.mainloop()


from threading import Thread

if __name__ == "__main__":
    thread = Thread(target=main, args=(12,))

    thread.start()
