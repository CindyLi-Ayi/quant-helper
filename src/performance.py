

import talib as ta
import tkinter as tk
import re
import itertools
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from error import *
from util import *
from func_calculator import *


class add_option(tk.Frame):
    def __init__(self, root, option):
        super().__init__(root, bg='ivory2', width=1000, height=25)
        self.root = root
        self.option = option
        self.v = tk.StringVar()
        self.v.set('Please choose a indicator')
        w = tk.OptionMenu(self, self.v, *option, command=self.onselection)
        w.config(width=40, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=0, rely=0)
        self.wi = []

    def onselection(self, op):
        for i in self.wi:
            i.destroy()
        self.p = []
        op, _ = re.findall(r'(.+) \((.+)\)', op)[0]
        if op in ['Simple Moving Average', 'Weighted Moving Average', 'Exponential Moving Average',
                  'Bollinger Bands', 'Average Directional Movement Index', 'Aroon Oscillator',
                  'Commodity Channel Index', 'Relative Strength Index', 'Momentum',
                  'Average True Range', 'Normalized Average True Range']:
            self.p.append(tk.StringVar())
            self.p[-1].set('period')
            e = tk.Entry(self, textvariable=self.p[-1], width=10, validate='focusout',
                         validatecommand=self.val_linspace(0), invalidcommand=self.inval_linspace)
            e.place(relx=0.4, rely=0)
            e.bind("<FocusIn>", self.default(self.p[-1], 'period'))
            e.bind("<FocusOut>", self.default(self.p[-1], 'period'))
        if op in ['Moving Average Convergence/Divergence']:
            for i, arg in enumerate(['fastperiod', 'slowperiod', 'signalperiod']):
                self.p.append(tk.StringVar())
                self.p[-1].set(arg)
                e = tk.Entry(self, textvariable=self.p[-1], width=10, validate='focusout',
                             validatecommand=self.val_linspace(i), invalidcommand=self.inval_linspace)
                e.place(relx=0.4+i*0.1, rely=0)
                e.bind("<FocusIn>", self.default(self.p[-1], arg))
                e.bind("<FocusOut>", self.default(self.p[-1], arg))
        if op in ['Absolute Price Oscillator', 'Percentage Price Oscillator', 'Chaikin A/D Oscillator']:
            for i, arg in enumerate(['fastperiod', 'slowperiod']):
                self.p.append(tk.StringVar())
                self.p[-1].set(arg)
                e = tk.Entry(self, textvariable=self.p[-1], width=10, validate='focusout',
                             validatecommand=self.val_linspace(i), invalidcommand=self.inval_linspace)
                e.place(relx=0.4+i*0.1, rely=0)
                e.bind("<FocusIn>", self.default(self.p[-1], arg))
                e.bind("<FocusOut>", self.default(self.p[-1], arg))
        if op in ['Balance Of Power', 'Chaikin A/D Line', 'On Balance Volume', 'True Range']:
            tk.Label(self, text='No argument needed', bg='ivory2',
                     fg='ivory4', font=("Courier", 14)).place(relx=0.4, rely=0)
        tk.Button(self, text='+', bg='ivory3', fg='ivory4',
                  command=self.onadd).place(relx=0.9, rely=0)

    def onadd(self):
        try:
            _, short = re.findall(r'(.+) \((.+)\)', self.v.get())[0]
            self.root.param[short] = [int(i.get()) for i in self.p]
            k = self.root.widget.index(self)
            self.root.widget.insert(k+1, add_option(self.root, self.option))
            self.root.place_widget()
        except:
            ERROR("Invalid input!")

    def val_linspace(self, i):
        def f():
            if re.fullmatch(r'\d+', self.p[i].get()):
                return True
            else:
                return False
        return f

    def inval_linspace(self):
        ERROR('Invalid input format! (should be \d+)')

    def default(self, strv, text):
        def f(event):
            current = strv.get()
            if current == text:
                strv.set("")
            elif current == '':
                strv.set(text)
        return f


class performance_page(tk.Frame):
    def __init__(self, root, data, stock):
        super().__init__(root, bg='ivory2')
        self.root = root
        self.data = data
        self.stock = stock

        self.stock_choice = tk.StringVar()
        self.stock_choice.set("please select the stock")
        w = tk.OptionMenu(self, self.stock_choice, *self.stock)
        w.config(width=50, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        tk.Label(self, text="Performance", bg='ivory2', fg='ivory4',
                 font=("Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.mark = 0.2

        m1 = tk.Label(self, text="Overlap Studies", bg='ivory2',
                      fg='ivory4', font=("Courier", 20))
        o1 = ['Simple Moving Average (SMA)', 'Weighted Moving Average (WMA)',
              'Exponential Moving Average (EMA)', 'Bollinger Bands (BBANDS)']
        p1 = add_option(self, o1)

        m2 = tk.Label(self, text="Momentum Indicator",
                      bg='ivory2', fg='ivory4', font=("Courier", 20))
        o2 = ['Average Directional Movement Index (ADX)', 'Aroon Oscillator (ARRONOSC)',
              'Commodity Channel Index (CCI)', 'Moving Average Convergence/Divergence (MACD)',
              'Absolute Price Oscillator (APO)', 'Percentage Price Oscillator (PPO)',
              'Balance Of Power (BOP)', 'Relative Strength Index (RSI)', 'Momentum (MOM)']
        p2 = add_option(self, o2)
        m3 = tk.Label(self, text="Volatility Indicator",
                      bg='ivory2', fg='ivory4', font=("Courier", 20))
        o3 = ['True Range (TRANGE)', 'Average True Range (ATR)',
              'Normalized Average True Range (NATR)']
        p3 = add_option(self, o3)
        m4 = tk.Label(self, text="Volume Indicator", bg='ivory2',
                      fg='ivory4', font=("Courier", 20))
        o4 = ['Chaikin A/D Line (AD)', 'Chaikin A/D Oscillator (ADOSC)',
              'On Balance Volume (OBV)']
        p4 = add_option(self, o4)
        c = tk.Label(self, text="Function for computing buy signal",
                     bg='ivory2', fg='ivory4', font=("Courier", 20))
        self.func = tk.StringVar()
        cc = tk.Entry(self, textvariable=self.func, width=100, validate='focusout', validatecommand=lambda: self.func.get(
        ) != '', invalidcommand=lambda: ERROR('Empty signal function'))
        b = tk.Button(self, text='Draw', command=self.ondraw)
        self.widget = [m1, p1, m2, p2, m3, p3, m4, p4, c, cc, b]
        self.place_widget()
        self.param = {}
        self.func_dict = {
            'SMA': (ta.SMA, (3,), 1),
            'WMA': (ta.WMA, (3,), 1),
            'EMA': (ta.EMA, (3,), 1),
            'BBANDS': (ta.BBANDS, (3,), 1),
            'ADX': (ta.ADX, (1, 2, 3), 1),
            'ARRONOSC': (ta.AROONOSC, (1, 2), 1),
            'CCI': (ta.CCI, (1, 2, 3), 1),
            'RSI': (ta.RSI, (3,), 1),
            'MOM': (ta.MOM, (3,), 1),
            'ATR': (ta.ATR, (1, 2, 3), 1),

            'NATR': (ta.NATR, (1, 2, 3), 1),

            'MACD': (ta.MACD, (3,), 3),

            'APO': (ta.APO, (3,), 2),
            'PPO': (ta.PPO, (3,), 2),
            'ADOSC': (ta.ADOSC, (1, 2, 3, 4), 2),

            'BOP': (ta.BOP, (0, 1, 2, 3), 0),
            'AD': (ta.AD, (1, 2, 3, 4), 0),
            'OBV': (ta.OBV, (3, 4), 0),
            'TRANGE': (ta.TRANGE, (1, 2, 3), 0),
        }

    def place_widget(self):
        for i, w in enumerate(self.widget):
            w.place(relx=self.mark, rely=i*0.05+0.2)

    def ondraw(self, event=None):
        if self.data.shape[1] <= 6:
            self.cal_data = self.data
        else:
            self.cal_data = self.data[self.stock_choice.get()]
        self.create_func()
        self.paras = []
        self.para_name = []

        for i in self.func_name:
            self.paras.extend(self.param[i])
        self.pnl_paras = {'slip': 8, 'tick_size': 0.01}
        daily_cum_ret, drawdown, net_price = performance(self.paras, [self.cal_data['Open'], self.cal_data['High'], self.cal_data['Low'], self.cal_data['Close'],
                                                                      self.cal_data['Volume']], self.final_func, self.cal_data['Close'], np.ones_like(self.cal_data['Open']), self.pnl_paras, mode='both')

        topwindow_result(self, daily_cum_ret, drawdown,
                         net_price, self.cal_data.index)

    def create_func(self):
        try:
            self.func_name = [i for i in re.split(
                r'\+|\-|\*|\/|\(|\)|\d| ', self.func.get()) if i != '']
            self.func_para_dic = {}
            self.k = 0
            for i in self.func_name:
                self.func_para_dic[i] = (
                    self.func_dict[i][1], (self.k, self.k + self.func_dict[i][2]))
                self.k += self.func_dict[i][2]
            self.final_func = func_calculator(
                self.func.get(), self.func_para_dic, self.func_dict).result()
        except:
            ERROR('invalid signal function')


class topwindow_result(tk.Toplevel):
    def __init__(self, root, daily_cum_ret, drawdown, net_price, date):
        super().__init__(root, bg='ivory2')
        self.geometry('1200x800')
        tk.Label(self, text="Performance Plot", bg='ivory2', fg='ivory4',
                 font=("Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.N)
        f = Figure()
        ax1 = f.add_subplot(111)
        ax2 = ax1.twinx()
        canvas = FigureCanvasTkAgg(f, self)
        canvas._tkcanvas.place(relx=0.5, rely=0.2, anchor=tk.N)
        l1 = ax1.plot(drawdown, color='g', label='drawdown')
        l2 = ax1.plot(daily_cum_ret, color='r', label='cumulative return')
        l3 = ax2.plot(net_price, color='b', label='price - price[0]')
        ls = l1 + l2 + l3
        labs = [l.get_label() for l in ls]
        ax1.legend(ls, labs)
        date = date.strftime('%Y-%m-%d')
        n = date.shape[0]
        ticks = np.linspace(0, n-1, 6).astype(int)
        label = [date[i] for i in range(n) if i in ticks]
        ax1.set_xticks(ticks)
        ax1.set_xticklabels(label)
        # align_yaxis(ax1, 0, ax2, 0)
        canvas.draw()
