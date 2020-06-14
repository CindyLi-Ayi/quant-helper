

import talib as ta
import tkinter as tk
import re
import itertools
import numpy as np
from pandastable.core import Table
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
            self.p[-1].set('period (s:e:n)')
            e = tk.Entry(self, textvariable=self.p[-1], width=10, validate='focusout',
                         validatecommand=self.val_linspace(0), invalidcommand=self.inval_linspace)
            e.place(relx=0.4, rely=0)
            e.bind("<FocusIn>", self.default(self.p[-1], 'period (s:e:n)'))
            e.bind("<FocusOut>", self.default(self.p[-1], 'period (s:e:n)'))
        if op in ['Moving Average Convergence/Divergence']:
            for i, arg in enumerate(['fastperiod', 'slowperiod', 'signalperiod']):
                self.p.append(tk.StringVar())
                self.p[-1].set(arg+' (s:e:n)')
                e = tk.Entry(self, textvariable=self.p[-1], width=10, validate='focusout',
                             validatecommand=self.val_linspace(i), invalidcommand=self.inval_linspace)
                e.place(relx=0.4+i*0.1, rely=0)
                e.bind("<FocusIn>", self.default(self.p[-1], arg+' (s:e:n)'))
                e.bind("<FocusOut>", self.default(self.p[-1], arg+' (s:e:n)'))
        if op in ['Absolute Price Oscillator', 'Percentage Price Oscillator', 'Chaikin A/D Oscillator']:
            for i, arg in enumerate(['fastperiod', 'slowperiod']):
                self.p.append(tk.StringVar())
                self.p[-1].set(arg+' (s:e:n)')
                e = tk.Entry(self, textvariable=self.p[-1], width=10, validate='focusout',
                             validatecommand=self.val_linspace(i), invalidcommand=self.inval_linspace)
                e.place(relx=0.4+i*0.1, rely=0)
                e.bind("<FocusIn>", self.default(self.p[-1], arg + ' (s:e:n)'))
                e.bind("<FocusOut>", self.default(
                    self.p[-1], arg + ' (s:e:n)'))
        if op in ['Balance Of Power', 'Chaikin A/D Line', 'On Balance Volume', 'True Range']:
            tk.Label(self, text='No argument needed', bg='ivory2',
                     fg='ivory4', font=("Courier", 14)).place(relx=0.4, rely=0)
        tk.Button(self, text='+', bg='ivory3', fg='ivory4',
                  command=self.onadd).place(relx=0.9, rely=0)

    def onadd(self):
        try:
            _, short = re.findall(r'(.+) \((.+)\)', self.v.get())[0]
            self.root.param[short] = [
                [int(j) for j in i.get().split(':')] for i in self.p]
            k = self.root.widget.index(self)
            self.root.widget.insert(k+1, add_option(self.root, self.option))
            self.root.place_widget()
        except:
            ERROR("Invalid input!")

    def val_linspace(self, i):
        def f():
            if re.fullmatch(r'\d+:\d+:\d+', self.p[i].get()):
                return True
            else:
                return False
        return f

    def inval_linspace(self):
        ERROR('Invalid input format! (should be np.linspace \d+:\d+:\d+)')

    def default(self, strv, text):
        def f(event):
            current = strv.get()
            if current == text:
                strv.set("")
            elif current == '':
                strv.set(text)
        return f


class indicator_page(tk.Frame):
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

        tk.Label(self, text="Indicator", bg='ivory2', fg='ivory4', font=(
            "Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
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
        cc = tk.Entry(self, textvariable=self.func, width=100, validate='focusout',
                      validatecommand=lambda: self.func.get() != '', invalidcommand=lambda: ERROR('Empty signal function'))
        b = tk.Button(self, text='Backtest', command=self.oncal)
        self.widget = [m1, p1, m2, p2, m3, p3, m4, p4, c, cc, b]
        self.place_widget()
        self.param = {}
        self.func_dict = {
            'SMA': (ta.SMA, (3,), 1),
            'WMA': (ta.WMA, (3,), 1),
            'EMA': (ta.EMA, (3,), 1),
            'BBANDS': (lambda x,y: ta.BBANDS(x,y)[0], (3,), 1),
            'ADX': (ta.ADX, (1, 2, 3), 1),
            'ARRONOSC': (ta.AROONOSC, (1, 2), 1),
            'CCI': (ta.CCI, (1, 2, 3), 1),
            'RSI': (ta.RSI, (3,), 1),
            'MOM': (ta.MOM, (3,), 1),
            'ATR': (ta.ATR, (1, 2, 3), 1),

            'NATR': (ta.NATR, (1, 2, 3), 1),

            'MACD': (lambda x,y,z,a:ta.MACD(x,y,z,a), (3,), 3),

            'APO': (ta.APO, (3,), 2),
            'PPO': (ta.PPO, (3,), 2),
            'ADOSC': (ta.ADOSC, (1, 2, 3, 4), 2),

            'BOP': (ta.BOP, (0, 1, 2, 3), 0),
            'AD': (ta.AD, (1, 2, 3, 4), 0),
            'OBV': (ta.OBV, (3, 4), 0),
            'TRANGE': (ta.TRANGE, (1, 2, 3), 0),
        }
        tk.Button(self, text="Go to Performance", command=self.root.run_performance, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)

    def place_widget(self):
        for i, w in enumerate(self.widget):
            w.place(relx=self.mark, rely=i*0.05+0.2)

    def oncal(self, event=None):
        if self.data.shape[1] <= 6:
            self.cal_data = self.data
        else:
            self.cal_data = self.data[self.stock_choice.get()]
        self.create_func()
        self.paras = []
        self.para_name = []
        for i in self.func_name:
            for j in self.param[i]:
                self.paras.append(list(np.linspace(*j)))
            if i == 'MACD':
                self.para_name.extend(
                    [i + '_fastperiod', i + '_slowperiod', i + '_signalperiod'])
            elif i in ['APO', 'PPO', 'ADOSC']:
                self.para_name.extend([i+'_fastperiod', i+'_slowperiod'])
            elif i in ['BOP', 'AD', 'OBV', 'TRANGE']:
                pass
            else:
                self.para_name.append(i + '_period')
        self.para_list = list(itertools.product(*self.paras))
        self.pnl_paras = {'slip': 8, 'tick_size': 0.01}
        result = []

        for pt in self.para_list:
            result.append(select_paras(pt, [self.cal_data['Open'], self.cal_data['High'], self.cal_data['Low'], self.cal_data['Close'],
                                            self.cal_data['Volume']], self.final_func, self.cal_data['Close'], np.ones_like(self.cal_data['Open']), self.pnl_paras, mode='train'))
        result_df = save_result(result, self.para_list, self.para_name)
        topwindow_result(self, result_df, self.para_name)

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

    def test_set(self):
        result = []
        for pt in self.para_list:
            result.append(select_paras(pt, [self.cal_data['Open'], self.cal_data['High'], self.cal_data['Low'], self.cal_data['Close'],
                                            self.cal_data['Volume']], self.final_func, self.cal_data['Close'], np.ones_like(self.cal_data['Open']), self.pnl_paras, mode='test'))
        result_df = save_result(result, self.para_list, self.para_name)
        topwindow_result(self, result_df, self.para_name)


class topwindow_result(tk.Toplevel):
    def __init__(self, root, result, param):

        super().__init__(root, bg='ivory2')
        self.root = root
        self.param = param
        self.result = result
        tk.Label(self, text="Result", bg='ivory2', fg='ivory4',
                 font=("Courier", 44)).place(relx=0.5, rely=0.1, anchor=tk.N)
        self.geometry('1200x800')

        self.frame = tk.Frame(self)
        self.table = Table(self.frame, dataframe=self.result,
                           width=400, height=400)
        self.table.show()
        self.frame.place(relx=0.48, rely=0.35, anchor=tk.NE)

        self.v = []
        for i in '12':
            self.v.append(tk.StringVar())
            self.v[-1].set("please select parameter "+i)
            w = tk.OptionMenu(
                self, self.v[-1], *self.param, command=self.onselection)
            w.config(width=30, bg='ivory2', fg='ivory4')
            w["menu"].config(bg='ivory2', fg='ivory4')
            w.place(relx=0.5, rely=0.15+int(i)*0.05, anchor=tk.N)
        self.v.append(tk.StringVar())
        self.v[-1].set("please select the criteria")
        w = tk.OptionMenu(self, self.v[-1], *['sharpe', 'mar', 'annprofit', 'maxdd',
                                              'maxdd10', 'maxdd_ratio', 'avg_turnover'], command=self.onselection)
        w.config(width=30, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=0.5, rely=0.3, anchor=tk.N)

        self.f = Figure(figsize=(5, 5))
        self.a = self.f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas._tkcanvas.place(relx=0.52, rely=0.35, anchor=tk.NW)

        tk.Button(self, text="Try Test Set", command=self.root.test_set, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)

    def onselection(self, event=None):
        if self.v[0].get() != "please select the parameter 1" \
                and self.v[1].get() != "please select the parameter 2" \
                and self.v[2].get() != "please select the criteria":
            report_result = pd.pivot_table(self.result, index=[self.v[0].get()], columns=[
                self.v[1].get()], values=self.v[2].get(), aggfunc=lambda x: np.percentile(x, 90))
            self.a.clear()
            sns.heatmap(report_result, ax=self.a, cbar=False, square=True, linewidths=.5,
                        annot=True, cmap='bwr')
            self.canvas.draw()
