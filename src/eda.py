from datetime import datetime
import numpy as np
import pandas as pd
import tkinter as tk
import time
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pandastable.core import Table
import seaborn as sns
from error import *

sns.set_style("darkgrid")
matplotlib.use('TkAgg')


class eda_page(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='ivory2')
        tk.Label(self, text="Exploratory Data Analysis", bg='ivory2', fg='ivory4',
                 font=("Courier", 44)).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        tk.Label(self, text="I know you want to skip Exploratory Data Analysis (EDA) ", bg='ivory2', fg='ivory4',
                 font=("Courier", 20)).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        tk.Label(self, text="but it is indeed really important!", bg='ivory2', fg='ivory4',
                 font=("Courier", 20)).place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        tk.Label(self, text="Please try the following:", bg='ivory2', fg='ivory4',
                 font=("Courier", 20)).place(relx=0.35, rely=0.45)
        tk.Button(self, text="1. check if your data contain any NAN value", command=root.run_nan, bg='ivory2', fg='ivory4',
                  font=("Courier", 20)).place(relx=0.35, rely=0.5)
        tk.Button(self, text="2. distribution plot", command=root.run_dist, bg='ivory2', fg='ivory4',
                  font=("Courier", 20)).place(relx=0.35, rely=0.55)
        tk.Button(self, text="3. timeline plot", command=root.run_trend, bg='ivory2', fg='ivory4',
                  font=("Courier", 20)).place(relx=0.35, rely=0.6)
        tk.Button(self, text="4. heatmap plot", command=root.run_corr, bg='ivory2', fg='ivory4',
                  font=("Courier", 20)).place(relx=0.35, rely=0.65)


class nan_page(tk.Frame):
    def __init__(self, root, data):
        self.root = root
        self.data = data
        super().__init__(root, bg='ivory2')
        tk.Label(self, text="Check NAN Values", bg='ivory2', fg='ivory4', font=(
            "Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        disp = tk.StringVar()
        disp.set("Checking......")
        tk.Label(self, textvariable=disp, bg='ivory2', fg='ivory4', font=(
            "Courier", 20)).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.baddata = []
        r, c = data.shape
        for i in range(r):
            if True in data.iloc[i, :].isnull().values:
                self.baddata.append(i)
        if len(self.baddata) == 0:
            disp.set('Great! The data does not contain any nan entry~')
        else:
            disp.set('Hey, rows containing nan values are listed below.')
            self.frame = tk.Frame(self)
            self.table = Table(
                self.frame, dataframe=data.iloc[self.baddata, :])
            self.table.show()
            self.frame.place(relx=0.5, rely=0.3, anchor=tk.N)
            tk.Label(self, text="How do you want to fix those nan values?", bg='ivory2', fg='ivory4',
                     font=("Courier", 20)).place(relx=0.3, rely=0.7)
            tk.Button(self, text="delete", command=self.ondelete, bg='ivory3', fg='ivory4', font=("Courier", 20)).place(
                relx=0.3, rely=0.75)
            tk.Button(self, text="set to 0", command=self.setzero, bg='ivory3', fg='ivory4',
                      font=("Courier", 20)).place(relx=0.45, rely=0.75)
            tk.Button(self, text="forward fill", command=self.ffill, bg='ivory3', fg='ivory4',
                      font=("Courier", 20)).place(relx=0.3, rely=0.8)
            tk.Button(self, text="linear interpolate", command=self.interpolate, bg='ivory3', fg='ivory4',
                      font=("Courier", 20)).place(relx=0.45, rely=0.8)
        tk.Button(self, text="Go to distribution", command=self.root.run_dist, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)
        tk.Button(self, text="Go to indicator", command=self.root.run_indicator, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.95, anchor=tk.CENTER)

    def ondelete(self):
        self.data.dropna(inplace=True)
        self.table.model.df = self.data
        self.table.redraw()

    def setzero(self):
        self.data.fillna(0, inplace=True)
        self.table.model.df = self.data
        self.table.redraw()

    def ffill(self):
        self.data.fillna(method='ffill', inplace=True)
        self.table.model.df = self.data
        self.table.redraw()

    def interpolate(self):
        self.data.interpolate(axis=0, inplace=True)
        self.table.model.df = self.data
        self.table.redraw()


class dist_page(tk.Frame):
    def __init__(self, root, data):
        self.root = root
        super().__init__(root, bg='ivory2')
        self.data = data
        tk.Label(self, text="Distribution Plot", bg='ivory2', fg='ivory4', font=(
            "Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        tk.Label(self, text="Choose the columns you would like to plot distribution for", bg='ivory2', fg='ivory4',
                 font=("Courier", 20)).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        option = list(data.columns)
        self.v = tk.StringVar()
        self.v.set("please select the column")
        w = tk.OptionMenu(self, self.v, *option, command=self.onselection)
        w.config(width=50, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        f = Figure()
        self.a = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas._tkcanvas.place(relx=0.5, rely=0.3, anchor=tk.N)

        tk.Button(self, text="Go to NAN", command=self.root.run_nan, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.1, rely=0.05, anchor=tk.CENTER)
        tk.Button(self, text="Go to timeline", command=self.root.run_trend, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)
        tk.Button(self, text="Go to indicator", command=self.root.run_indicator, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.95, anchor=tk.CENTER)

    def onselection(self, col):
        self.a.clear()
        sns.distplot(self.data.loc[:, col], ax=self.a)
        self.canvas.draw()


class trend_page(tk.Frame):
    def __init__(self, root, data):
        self.root = root
        super().__init__(root, bg='ivory2')
        self.data = data
        tk.Label(self, text="Timeline Plot", bg='ivory2', fg='ivory4', font=(
            "Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        tk.Label(self, text="Choose the column you would like to plot the trend for: ", bg='ivory2',
                 fg='ivory4', font=("Courier", 20)).place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        option = list(data.columns)
        self.v = tk.StringVar()
        self.v.set("please select the column")
        w = tk.OptionMenu(self, self.v, *option, command=self.onselection)
        w.config(width=50, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        f = Figure()
        self.a = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas._tkcanvas.place(relx=0.5, rely=0.3, anchor=tk.N)

        tk.Button(self, text="Go to distribution", command=self.root.run_dist, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.1, rely=0.05, anchor=tk.CENTER)
        tk.Button(self, text="Go to correlation", command=self.root.run_corr, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)
        tk.Button(self, text="Go to indicator", command=self.root.run_indicator, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.95, anchor=tk.CENTER)

    def onselection(self, col):
        self.a.clear()
        sns.lineplot(x=self.data.index, y=self.data.loc[:, col], ax=self.a)
        self.canvas.draw()


class corr_page(tk.Frame):
    def __init__(self, root, data):
        self.root = root
        super().__init__(root, bg='ivory2')
        self.data = data
        tk.Label(self, text="Correlation Heatmap", bg='ivory2', fg='ivory4', font=(
            "Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        tk.Label(self, text="Choose the columns you would like to plot the correlation heatmap for: ",
                 bg='ivory2', fg='ivory4', font=("Courier", 20)).place(relx=0.5, rely=0.17, anchor=tk.CENTER)
        self.option = list(data.columns)
        self.result = []
        for i in self.option:
            self.result.append(tk.IntVar())
            b = tk.Checkbutton(
                self, text=i, variable=self.result[-1], bg='ivory2', fg='ivory4')
            x, y = round((len(self.result)-1) %
                         6/10+0.2, 1), (len(self.result)-1)//6/30+0.2
            b.place(relx=x, rely=y)
        bt = tk.Button(self, text='Draw', command=self.onselection)
        bt.place(relx=0.5, rely=len(self.result)//6/20+0.20, anchor=tk.CENTER)
        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas._tkcanvas.place(relx=0.5, rely=len(
            self.result)//6/20+0.23, anchor=tk.N)

        tk.Button(self, text="Go to timelime", command=self.root.run_trend, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.1, rely=0.05, anchor=tk.CENTER)
        tk.Button(self, text="Go to indicator", command=self.root.run_indicator, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.95, anchor=tk.CENTER)

    def onselection(self, event=None):
        n = len(self.option)
        result = [self.option[i] for i in range(n) if self.result[i].get()]
        hm = np.corrcoef(self.data.loc[:, result], rowvar=False)
        self.a.clear()
        sns.heatmap(hm, ax=self.a, cbar=False, square=True, linewidths=.5, vmin=-1,
                    vmax=1, annot=True, xticklabels=[], yticklabels=result, cmap='bwr')
        self.canvas.draw()
