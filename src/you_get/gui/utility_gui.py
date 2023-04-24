from multiprocessing import Value
import tkinter as tk
from tkinter import ttk
import subprocess


class YouGetGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("you-get")
        self.root.geometry("450x100")
        self.root.resizable(False, False)

        self.options_dict = {
            0: ("-i", "Print extracted information"),
            1: ("-u", "Print extracted information with URLs"),
            2: ("--json", "Print extracted URLs in JSON format"),
            3: ("--no-caption", "Do not download captions (subtitles, lyrics, danmaku)"),
            4: ("--postfix", "Postfix downloaded files with unique identifiers"),
            5: ("-f", "Force overwriting existing files"),
            6: ("--skip-existing-file-size-check", "Skip existing file without checking file size"),
            7: ("-F STREAM_ID", "Set video format to STREAM_ID"),
            8: ("-O FILE", "Set output filename"),
            9: ("-o DIR", "Set output directory"),
            10: ("-p PLAYER", "Stream extracted URL to a PLAYER"),
            11: ("-c", "Load cookies.txt or cookies.sqlite"),
            12: ("-t SECONDS", "Set socket timeout"),
            13: ("-d", "Show traceback and other debug info"),
            14: ("-a", "Auto rename same name different files"),
            15: ("-k", "Ignore SSL errors"),
            16: ("-m", "Download video using an m3u8 URL"),
            17: ("-x HOST:PORT", "Use an HTTP proxy for downloading"),
            18: ("-y HOST:PORT", "Use an HTTP proxy for extracting only"),
            19: ("--no-proxy", "Never use a proxy"),
            20: ("-s HOST:PORT", "Use a SOCKS5 proxy for downloading")
        }
        
        self.url = ""
        self.selected_options = []
        self.availible_formats = ["mp4", "mp3"]

        self.first_step_widget()

    def first_step_widget(self):
        self.main_frame = ttk.Frame(self.root, padding="30 20")
        self.main_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.url_text = tk.StringVar()
        self.url_text.set("Enter your URL here...")

        self.url_entry = ttk.Entry(
            self.main_frame, width=50, textvariable=self.url_text
        )
        self.url_entry.bind("<FocusIn>", self.clear_url_entry)
        self.url_entry.bind("<FocusOut>", self.restore_url_entry)
        self.url_entry.grid(column=0, row=0, padx=5, pady=5)

        self.continue_button = ttk.Button(
            self.main_frame, text="Continue", command=self.second_step_widget
        )
        self.continue_button.grid(column=1, row=0, padx=5, pady=5)

    def second_step_widget(self):
        self.url = self.url_entry.get()
        self.continue_button.grid_forget()
        self.url_entry.config(state="disabled")

        self.download_button = ttk.Button(
            self.main_frame, text="Download", command=self.download_video
        )

        self.download_button.grid(column=1, row=0, padx=5, pady=5)

        self.additional_frame = ttk.Frame(self.main_frame)
        self.additional_frame.grid(column=0, row=1, columnspan=2, sticky=tk.W)

        self.back_button = ttk.Button(
            self.additional_frame, text="Back", command=self.back_to_first_step
        )
        self.back_button.grid(column=0, row=0, padx=5, pady=5)

        self.format_combobox_text = tk.StringVar()
        self.format_combobox_text.set("Choose format...")
        self.format_combobox = ttk.Combobox(self.additional_frame, textvariable=self.format_combobox_text, state='readonly')
        self.format_combobox['values'] = self.availible_formats

        self.format_combobox.grid(column=1, row=0, padx=5, pady=5)

        self.settings_button = ttk.Button(
            self.additional_frame, text="Settings", command=self.show_settings_window
        )
        self.settings_button.grid(column=2, row=0, padx=5, pady=5)

    def show_settings_window(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")

        self.option_vars = [tk.BooleanVar() for _ in self.options_dict]

        for key, value in self.options_dict.items():
            option_checkbox = tk.Checkbutton(
                self.settings_window,
                text=value[1],
                variable=self.option_vars[key],
                onvalue=True,
                offvalue=False,
            )
            option_checkbox.pack()

        save_button = tk.Button(
            self.settings_window, text="Save Settings", command=self.save_settings
        )
        save_button.pack()

        cancel_button = tk.Button(
            self.settings_window, text="Cancel", command=self.hide_settings_window
        )
        cancel_button.pack()

    def hide_settings_window(self):
        self.settings_window.withdraw()

    def back_to_first_step(self):
        self.selected_options = []
        self.availible_formats = ["mp4", "mp3"]
        self.first_step_widget()

    def save_settings(self):
        for key, value in self.options_dict.items():
            if self.option_vars[key].get():
                self.selected_options.append(key)

        self.hide_settings_window()

    def download_video(self):
        cmd = ["you-get"]
        for key in self.selected_options:
            cmd += [self.options_dict.get(key)[0]]
        cmd += [self.url]
        print(cmd)


    def clear_url_entry(self, event):
        if self.url_entry.get() == "Enter your URL here...":
            self.url_entry.delete(0, tk.END)

    def restore_url_entry(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "Enter your URL here...")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    YouGetGUI().run()
