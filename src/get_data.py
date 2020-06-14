from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import pandas as pd
import tkinter as tk
import pickle
from pandastable.core import Table
from error import *
import re


class ydata:
    def __init__(self):
        self._stock = None
        self._interval = None
        self._start = None
        self._end = None
        self._period = None
        self._data = None
        self._industry = None

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, v):
        self._stock = v

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, v: str):
        if v in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']:
            self._interval = v
        else:
            print("Invalid interval")

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, v: str):
        self._start = v

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, v: str):
        self._end = v

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, v: str):
        if v in ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']:
            self._period = v
        else:
            print("Invalid period")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, v: pd.DataFrame):
        self._data = v

    @property
    def industry(self):
        return self._industry

    @industry.setter
    def industry(self, v: pd.Series):
        self._industry = v

    def get_data(self, stock: list, interval: str = '1d', period: str = '1mo', end: str = None, start: str = None):
        if end == None and start == None and period != 'max':
            end = datetime.today().strftime('%Y-%m-%d')
        stock_str = ''
        for i in stock:
            stock_str += i + ' '
        try:
            yf.pdr_override()
            self._data = pdr.get_data_yahoo(stock_str, group_by='ticker', interval=interval, start=start, end=end,
                                            period=period)
            self.stock = stock
            self.interval = interval
            self.start = self.data.index[0].strftime('%Y-%m-%d')
            self.end = self.data.index[-1].strftime('%Y-%m-%d')
            return 1
        except:
            return 0


class download_page(tk.Frame):
    def __init__(self, root, data):
        file = open(r'../sp500tickers.pkl', 'rb')
        self.all_stock_ticks = pickle.load(file)
        super().__init__(root, bg='ivory2')

        self.root = root
        self.data = data
        self.stock, self.interval, self.start, self.end, self.period = \
            tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

        mark1 = 0.35

        tk.Label(self, text="Download Data from Yahoo Finance", bg='ivory2', fg='ivory4', font=("Courier", 44)).place(
            relx=0.5, rely=0.1, anchor=tk.CENTER)

        tk.Label(self, text="stock", font=("Courier", 20), bg='ivory2', fg='ivory4').place(relx=mark1, rely=0.2,
                                                                                           anchor=tk.NE)
        self.stock.set('stock ticker: MSFT')
        e1 = tk.Entry(self, textvariable=self.stock, width=50, fg='ivory4', validate="focusout",
                      validatecommand=self.val_stock, invalidcommand=self.inval_stock)
        e1.place(relx=mark1, rely=0.2)
        e1.bind("<FocusIn>", self.default(self.stock, 'stock ticker: MSFT'))
        e1.bind("<FocusOut>", self.default(self.stock, 'stock ticker: MSFT'))

        tk.Label(self, text="interval", font=("Courier", 20), bg='ivory2', fg='ivory4').place(relx=mark1, rely=0.25,
                                                                                              anchor=tk.NE)
        interval_ = ['1m', '2m', '5m', '15m', '30m', '60m',
                     '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        self.interval.set('1d')
        w = tk.OptionMenu(self, self.interval, *interval_)
        w.config(width=50, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=mark1, rely=0.25)

        tk.Label(self, text="start", font=("Courier", 20), bg='ivory2', fg='ivory4').place(relx=mark1, rely=0.3,
                                                                                           anchor=tk.NE)
        self.start.set('yyyy-mm-dd')
        e2 = tk.Entry(self, textvariable=self.start, width=50, fg='ivory4', validate="focusout",
                      validatecommand=self.val_stime, invalidcommand=self.inval_time)
        e2.place(relx=mark1, rely=0.3)
        e2.bind("<FocusIn>", self.default(self.start, 'yyyy-mm-dd'))
        e2.bind("<FocusOut>", self.default(self.start, 'yyyy-mm-dd'))

        tk.Label(self, text="end", font=("Courier", 20), bg='ivory2', fg='ivory4').place(relx=mark1, rely=0.35,
                                                                                         anchor=tk.NE)
        self.end.set('yyyy-mm-dd')
        e3 = tk.Entry(self, textvariable=self.end, width=50, fg='ivory4', validate="focusout",
                      validatecommand=self.val_etime, invalidcommand=self.inval_time)
        e3.place(relx=mark1, rely=0.35)
        e3.bind("<FocusIn>", self.default(self.end, 'yyyy-mm-dd'))
        e3.bind("<FocusOut>", self.default(self.end, 'yyyy-mm-dd'))

        tk.Label(self, text="period", font=("Courier", 20), bg='ivory2', fg='ivory4').place(relx=mark1, rely=0.4,
                                                                                            anchor=tk.NE)
        period_ = ['1d', '5d', '1mo', '3mo', '6mo',
                   '1y', '2y', '5y', '10y', 'ytd', 'max']
        self.period.set('1mo')
        w = tk.OptionMenu(self, self.period, *period_)
        w.config(width=50, bg='ivory2', fg='ivory4')
        w["menu"].config(bg='ivory2', fg='ivory4')
        w.place(relx=mark1, rely=0.4)

        tk.Button(self, text="download", command=self.downloading, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Button(self, text="Go to upload", command=self.root.run_upload, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)

    def val_stock(self):
        for i in self.stock.get().split():
            if i not in self.all_stock_ticks:
                return False

    def inval_stock(self):
        ERROR("Invalid ticker!")

    def val_stime(self):
        if re.fullmatch(r'\d\d\d\d-\d\d-\d\d', self.start.get()):
            return True
        else:
            return False

    def val_etime(self):
        if re.fullmatch(r'\d\d\d\d-\d\d-\d\d', self.end.get()):
            return True
        else:
            return False

    def inval_time(self):
        ERROR('Invalid Time format! (Should be yyyy-mm-dd)')

    def downloading(self, event=None):
        if self.stock.get() == 'stock ticker: MSFT':
            stock = ['MSFT']
        else:
            stock = self.stock.get().split()
        interval = self.interval.get()
        if self.start.get() == 'yyyy-mm-dd':
            start = None
        else:
            start = self.start.get()
        if self.end.get() == 'yyyy-mm-dd':
            end = None
        else:
            end = self.end.get()
        period = self.period.get()
        dic_ = dict(zip(('stock', 'interval', 'start', 'end',
                         'period'), (stock, interval, start, end, period)))
        dic = {}
        for i in dic_:
            if dic_[i] != "":
                dic[i] = dic_[i]
        succ = self.data.get_data(**dic)
        if not succ:
            ERROR("Invalid input!")
        else:
            self.data.stock = stock
            self.frame = tk.Frame(self)
            self.table = Table(self.frame, dataframe=self.data.data)
            self.table.show()
            self.frame.place(relx=0.5, rely=0.6, anchor=tk.N)
            tk.Button(self, text="Go to EDA", command=self.root.eda_page, font=("Courier", 20), bg='ivory3',
                      fg='ivory4').place(relx=0.9, rely=0.95, anchor=tk.CENTER)

    def default(self, strv, text):
        def f(event):
            current = strv.get()
            if current == text:
                strv.set("")
            elif current == '':
                strv.set(text)
        return f


class upload_page(tk.Frame):
    def __init__(self, root, data):
        super().__init__(root, bg='ivory2')
        self.root = root
        self.data = data
        tk.Label(self, text="Upload panel data from this device", bg='ivory2', fg='ivory4', font=("Courier", 44)).place(
            relx=0.5, rely=0.1, anchor=tk.CENTER)
        tk.Label(self, text="file address", font=("Courier", 20), bg='ivory2', fg='ivory4').place(relx=0.4, rely=0.2,
                                                                                                  anchor=tk.NE)
        self.address = tk.StringVar()
        self.address.set('..//data.pkl')

        e = tk.Entry(self, textvariable=self.address, width=50, fg='ivory4')
        e.place(relx=0.4, rely=0.2)
        e.bind("<FocusIn>", self.default)
        e.bind("<FocusOut>", self.default)

        bt = tk.Button(self, text="upload", command=self.uploading,
                       font=("Courier", 20), bg='ivory3', fg='ivory4')
        bt.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        tk.Button(self, text="Go to download", command=self.root.run_download, font=("Courier", 20), bg='ivory3',
                  fg='ivory4').place(relx=0.9, rely=0.05, anchor=tk.CENTER)

        file = open(r'../sp500tickers.pkl', 'rb')
        self.all_stock_ticks = pickle.load(file)

    def uploading(self, event=None):
        try:
            address = self.address.get()
            file = open(address, 'rb')
            self.data.data = pickle.load(file)
            self.frame = tk.Frame(self)
            self.table = Table(self.frame, dataframe=self.data.data)
            self.table.show()
            self.frame.place(relx=0.5, rely=0.4, anchor=tk.N)
            tk.Button(self, text="Go to EDA", command=self.root.eda_page, font=("Courier", 20), bg='ivory3',
                      fg='ivory4').place(relx=0.9, rely=0.95, anchor=tk.CENTER)
            try:
                self.data.stock = set([i[0] for i in self.data.data.columns])
            except:
                ERROR("Wrong data format (Index: time, Columns: (ticker, ohlcv))!")
            print(type(self.data.data.columns))
            if not all(i in self.all_stock_ticks for i in self.data.stock)\
                    and all(i[1] in ['Open', 'Hign', 'Low', 'Close', 'Volumn', 'Adj Close'] for i in self.data.data.columns):
                ERROR("Wrong data format (Index: time, Columns: (ticker, ohlcv))!")
        except:
            ERROR("Invalid address!")

    def default(self, event):
        current = self.address.get()
        if current == '..//data.pkl':
            self.address.set("")
        elif current == '':
            self.address.set('..//data.pkl')
