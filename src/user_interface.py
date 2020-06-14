from pandas_datareader import data as pdr
from datetime import datetime
import numpy as np
import pandas as pd
import tkinter as tk
import pickle
import re
import itertools
import numpy as np

import yfinance as yf
from pandastable.core import Table
import talib as ta

from get_data import *
from eda import *
from indicator import *
from performance import *
from error import *


class topwindow(tk.Frame):
    def __init__(self, root):
        self.root = root
        super().__init__(root)
        self.data = ydata()

        self.container = tk.Frame(self, bg='ivory2')
        self.container.pack(side="top", fill="both", expand=True)

        mainmenu = tk.Menu(self)
        datamenu = tk.Menu(mainmenu, tearoff=False)
        datamenu.add_command(label='download from yahoo',
                             command=self.run_download)
        datamenu.add_command(label='upload', command=self.run_upload)
        mainmenu.add_cascade(label='data', menu=datamenu)

        edamenu = tk.Menu(mainmenu, tearoff=False)
        edamenu.add_command(label='Nan Value', command=self.run_nan)
        edamenu.add_command(label='distribution', command=self.run_dist)
        edamenu.add_command(label='trend', command=self.run_trend)
        edamenu.add_command(label='correlation', command=self.run_corr)
        mainmenu.add_cascade(label='EDA', menu=edamenu)

        self.welcome_page()

        indicatormenu = tk.Menu(mainmenu, tearoff=False)
        indicatormenu.add_command(label='Backtest', command=self.run_indicator)
        indicatormenu.add_command(
            label='Performance', command=self.run_performance)
        mainmenu.add_cascade(label='Indicator', menu=indicatormenu)

        root.config(menu=mainmenu)

    def welcome_page(self):
        tk.Label(self, text="Welcome to Quant Helper~", bg='ivory2', fg='ivory4', font=("Courier", 44)).place(
            relx=0.5, rely=0.2, anchor=tk.CENTER)
        tk.Label(self, text="First, ", bg='ivory2', fg='ivory4', font=("Courier", 20)).place(
            relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Button(self, text='download data from Yahoo Finance', command=self.run_download, bg='ivory2', fg='ivory4',
                  font=("Courier", 20)).place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        tk.Label(self, text="or", bg='ivory2', fg='ivory4', font=("Courier", 20)).place(
            relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Button(self, text='upload you own data', command=self.run_upload, bg='ivory2', fg='ivory4',
                  font=("Courier", 20)).place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        tk.Label(self, text="to start your exploration~", bg='ivory2', fg='ivory4', font=("Courier", 20)).place(
            relx=0.5, rely=0.6, anchor=tk.CENTER)

    def eda_page(self):
        eda = eda_page(self)
        eda.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        eda.lift()

    def run_download(self):
        download = download_page(self, self.data)
        download.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        download.lift()
        self.root.bind('<Return>', download.downloading)

    def run_upload(self):
        upload = upload_page(self, self.data)
        upload.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        upload.lift()
        self.root.bind('<Return>', upload.uploading)

    def run_nan(self):
        nan = nan_page(self, self.data.data)
        nan.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        nan.lift()

    def run_dist(self):
        dist = dist_page(self, self.data.data)
        dist.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        dist.lift()

    def run_trend(self):
        trend = trend_page(self, self.data.data)
        trend.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        trend.lift()

    def run_corr(self):
        corr = corr_page(self, self.data.data)
        corr.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        corr.lift()
        self.root.bind('<Return>', corr.onselection)

    def run_indicator(self):
        indicator = indicator_page(self, self.data.data, self.data.stock)
        indicator.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        indicator.lift()
        self.root.bind('<Return>', indicator.oncal)

    def run_performance(self):
        performance = performance_page(self, self.data.data, self.data.stock)
        performance.place(in_=self.container, x=0,
                          y=0, relwidth=1, relheight=1)
        performance.lift()
        self.root.bind('<Return>', performance.ondraw)


root = tk.Tk()
root.title('Quant Helper')
main = topwindow(root)
main.pack(side="top", fill="both", expand=True)
root.geometry("1440x900")
root.mainloop()
