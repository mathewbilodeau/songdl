import os
import re
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from tkinter import ttk

import music_tag
import pafy
from googlesearch import lucky


class Songdl(tk.Tk):
    # Class variables / constants
    REQUIRED_FIELD_DEFAULT = "Required"
    RECOMMENDED_FIELD_DEFAULT = "Recommended"
    OPTIONAL_FIELD_DEFAULT = "Optional"
    GENRES = ("Alternative", "Anime", "Blues", "Children's", "Classical", "Comedy", "Commercial", "Country", "Dance",
              "Easy Listening", "Electronic", "Enka", "French Pop", "Folk", "German Pop", "Fitness/Workout",
              "Hip-Hop/Rap", "Holiday", "Indie Pop", "Industrial", "Inspirational", "Instrumental", "J-Pop", "Jazz",
              "K-Pop", "Karaoke", "Kayokyoku", "Latin", "Metal", "New Age", "Opera", "Pop", "Post-Disco", "Progressive",
              "R&B/Soul", "Reggae", "Rock", "Singer/Songwriter", "Soundtrack", "Spoken Word", "Tex-Mex/Tejano", "Vocal",
              "World")

    # Static methods
    @staticmethod
    def find_youtube_url_for_song(title, artist):
        """Using the argument strings, title and artist, builds a query string and returns a single URL result from the
        lucky method of googlesearch. The query filters out all results that are not from youtube.com. title cannot be
        an empty string. artist may be empty, but the resulting URL will be more accurate if it is not. Returns a
        string containing the URL."""
        if not title:
            raise ValueError("Title cannot be empty string.")
        query = title + " " + artist + " site:youtube.com"
        return lucky(query)

    @staticmethod
    def download_audio_from_youtube_video(url, file_path):
        """Using the argument strings, url and file_path, downloads the audio of the YouTube video in m4a format and
         places the file in the given file path. The URL must contain "www.youtube." and "/watch?v=" as these tokens
         guarantee that the URL is of a YouTube video. A string containing the file path of the new file is returned.
         The file name is the YouTube video title, and is filtered by a regular expression to remove characters which
         Windows, Mac, and Linux operating systems do not allow in file names."""
        if "www.youtube." not in url or "/watch?v=" not in url:
            raise ValueError("Provided URL not a YouTube video.")
        video = pafy.new(url)
        m4a_streams = video.m4astreams
        audio = m4a_streams[0]
        audio.download(file_path)
        print(video.title)
        print(file_path)
        print(file_path + os.path.sep + re.sub("[^\\w_.)( -]", "_", video.title) + ".m4a")
        return file_path + os.path.sep + re.sub("[^\\w_.)( -]", "_", video.title) + ".m4a"

    @staticmethod
    def update_metadata(file_path, title="", contributing_artists="", album_artist="", album="", year="",
                        track_number="", genre=""):
        """The argument strings are metadata tokens. Only the file_path argument is required. All other arguments
        default to empty strings and the metadata will not change. The dictionary containing the metadata expects
        year and track number to be integers, so those will be ignored if they are empty strings. Does not return
        anything."""
        song = music_tag.load_file(file_path)
        song["title"] = title
        song["artist"] = contributing_artists
        song["album artist"] = album_artist
        song["album"] = album
        if year:
            song["year"] = year
        if track_number:
            song["track number"] = track_number
        song["genre"] = genre
        song.save()

    def __init__(self):
        super().__init__()

        # Instantiate the main frame
        self.frame = ttk.Frame(self)

        # String variables
        self.information_string_variable = tk.StringVar()
        self.title_string_variable = tk.StringVar()
        self.artist_string_variable = tk.StringVar()
        self.contributing_artists_string_variable = tk.StringVar()
        self.album_string_variable = tk.StringVar()
        self.year_string_variable = tk.StringVar()
        self.track_number_string_variable = tk.StringVar()
        self.genre_string_variable = tk.StringVar()
        self.file_path_string_variable = tk.StringVar()

        # Row 0
        ttk.Label(self.frame, textvariable=self.information_string_variable).grid(column=0, row=0, columnspan=2)

        # Row 1
        ttk.Label(self.frame, text="Title").grid(column=0, row=1)
        ttk.Entry(self.frame, width=45, textvariable=self.title_string_variable).grid(column=1, row=1)

        # Row 2
        ttk.Label(self.frame, text="Album Artist").grid(column=0, row=2)
        ttk.Entry(self.frame, width=45, textvariable=self.artist_string_variable).grid(column=1, row=2)

        # Row 3
        ttk.Label(self.frame, text="Contributing Artists").grid(column=0, row=3)
        ttk.Entry(self.frame, width=45, textvariable=self.contributing_artists_string_variable).grid(column=1, row=3)

        # Row 4
        ttk.Label(self.frame, text="Album").grid(column=0, row=4)
        ttk.Entry(self.frame, width=45, textvariable=self.album_string_variable).grid(column=1, row=4)

        # Row 5
        year_list = [year for year in range(datetime.now().year - 50, datetime.now().year + 1)]
        ttk.Label(self.frame, text="Year").grid(column=0, row=5)
        ttk.Combobox(self.frame, textvariable=self.year_string_variable, values=year_list).grid(column=1, row=5)

        # Row 6
        track_number_list = [number for number in range(1, 51)]
        ttk.Label(self.frame, text="Track Number").grid(column=0, row=6)
        ttk.Combobox(self.frame, textvariable=self.track_number_string_variable, values=track_number_list).grid(
            column=1, row=6)

        # Row 7
        ttk.Label(self.frame, text="Genre").grid(column=0, row=7)
        ttk.Combobox(self.frame, textvariable=self.genre_string_variable, values=self.GENRES).grid(column=1, row=7)

        # Row 8
        ttk.Label(self.frame, text="File Path").grid(column=0, row=8)
        ttk.Entry(self.frame, width=45, textvariable=self.file_path_string_variable).grid(column=1, row=8, columnspan=2)

        # Row 9
        ttk.Label(self.frame, text="OR").grid(column=0, row=9)
        self.browse_button = ttk.Button(self.frame, width=20, text="Browse", command=self.browse_files)
        self.browse_button.grid(column=1, row=9)

        # Row 10
        self.download_button = ttk.Button(self.frame, width=20, text="Download",
                                          command=self.download_song_and_update_metadata)
        self.download_button.grid(column=1, row=10)

        # Row 11
        self.clear_fields_button = ttk.Button(self.frame, width=20, text="Clear Fields",
                                              command=self.revert_text_fields)
        self.clear_fields_button.grid(column=1, row=11)

        # Configuration
        for child in self.frame.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # Find path to music directory
        self.music_directory_path = os.path.join(os.path.expanduser("~"), "Music")

        # Initialize string variables
        self.revert_text_fields()

        # Place the frame
        self.frame.grid(column=0, row=0)

    def browse_files(self):
        folder_selected = filedialog.askdirectory()
        self.file_path_string_variable.set(folder_selected)

    def download_song_and_update_metadata(self):
        url = self.find_youtube_url_for_song(self.title_string_variable.get(), self.artist_string_variable.get())
        self.information_string_variable.set(url)
        full_file_path = self.download_audio_from_youtube_video(url, file_path=self.file_path_string_variable.get())
        # self.update_metadata(full_file_path,
        #                      title=self.title_string_variable.get().replace(self.REQUIRED_FIELD_DEFAULT, ""),
        #                      contributing_artists=self.contributing_artists_string_variable.get().replace(
        #                          self.RECOMMENDED_FIELD_DEFAULT, ""),
        #                      album_artist=self.artist_string_variable.get().replace(self.RECOMMENDED_FIELD_DEFAULT, ""),
        #                      album=self.album_string_variable.get().replace(self.OPTIONAL_FIELD_DEFAULT, ""),
        #                      year=self.year_string_variable.get().replace(self.OPTIONAL_FIELD_DEFAULT, ""),
        #                      track_number=self.track_number_string_variable.get().replace(self.OPTIONAL_FIELD_DEFAULT,
        #                                                                                   ""),
        #                      genre=self.genre_string_variable.get().replace(self.OPTIONAL_FIELD_DEFAULT, ""))

    def revert_text_fields(self):
        self.information_string_variable.set("Fill in the below fields and then press download.")
        self.title_string_variable.set(self.REQUIRED_FIELD_DEFAULT)
        self.artist_string_variable.set(self.RECOMMENDED_FIELD_DEFAULT)
        self.contributing_artists_string_variable.set(self.RECOMMENDED_FIELD_DEFAULT)
        self.album_string_variable.set(self.OPTIONAL_FIELD_DEFAULT)
        self.year_string_variable.set(self.OPTIONAL_FIELD_DEFAULT)
        self.track_number_string_variable.set(self.OPTIONAL_FIELD_DEFAULT)
        self.genre_string_variable.set(self.OPTIONAL_FIELD_DEFAULT)
        self.file_path_string_variable.set(self.music_directory_path)

    def run_application(self):
        self.title("YouTube Audio Downloader")
        self.resizable(0, 0)
        self.mainloop()


def main():
    application = Songdl()
    application.run_application()


if __name__ == "__main__":
    main()
