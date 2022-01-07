import os

import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from vkr_modules.playlist import Playlist


class VoltaicKovaaksReport:
	def __init__(self):
		self.window = tk.Tk()
		self.window.protocol("WM_DELETE_WINDOW", self.quit)
		
		sizex, sizey = 650, 250
		self.window.geometry(f'{sizex}x{sizey}')

		self.window.title('Voltaic KovaaK\'s Report')
		self.window.iconbitmap('resources/vkr_icon.ico')

		text_statfolder_title = 'KovaaK\'s Stat Folder:'
		label_statfolder_title = tk.Label(master=self.window, text=text_statfolder_title)
		label_statfolder_title.grid(column=0, row=0)

		self.text_statfolder_path = tk.StringVar()
		self.label_statfolder_path = tk.Label(master=self.window, textvariable=self.text_statfolder_path)
		self.label_statfolder_path.grid(column=1, row=0)

		spacer1 = tk.Label(master=self.window, text='', height=1)
		spacer1.grid(column=0, row=1)

		button_browse = tk.Button(master=self.window, text='Browse Folder', command=self.browse_folder)
		button_browse.grid(column=0, row=2, sticky=tk.W, padx=10)

		button_generate = tk.Button(master=self.window, text='Generate Report', command=self.generate_report)
		button_generate.grid(column=0, row=4, sticky=tk.W, padx=10)

		img_teto = Image.open('resources/kasane_teto.png')
		photoimg_teto = ImageTk.PhotoImage(img_teto)
		label_teto = tk.Label(image=photoimg_teto)
		label_teto.place(x=sizex, y=sizey, anchor=tk.SE)

		# label_teto.grid(column=3, row=3)

		self.window.mainloop()

	def browse_folder(self):
		w = tk.Tk()
		w.withdraw()
		statfolder_path = filedialog.askdirectory(title='Select KovaaK\'s stats folder')
		self.text_statfolder_path.set(statfolder_path)
		w.destroy()

	def generate_report(self):
		if self.text_statfolder_path.get() == '':
			messagebox.showerror('Error', 'Set your KovaaK\'s Stat folder before generating a report.')
		else:
			# playlist = Playlist(stats_folder=self.text_statfolder_path.get(), root_folder=os.path.dirname(__file__))
			playlist = Playlist(stats_folder=self.text_statfolder_path.get(), root_folder=os.getcwd())
			playlist.generate_folders()
			playlist.generate_reports()

			messagebox.showinfo('Operation completed', 'Generated in report.html\nFeel free to close this application.')

	def quit(self):
		self.window.quit()
		self.window.destroy()


if __name__ == "__main__":
    vkr = VoltaicKovaaksReport()
