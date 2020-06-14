

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import seaborn as sns
import matplotlib.pyplot as plt


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1 - y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny + dy, maxy + dy)


def ann_return(daily_ret):
    return np.mean(daily_ret) * 365


def sharpe_ratio(daily_ret):
    sharpe_ratio = np.mean(daily_ret) / np.std(daily_ret) * np.sqrt(250)
    return sharpe_ratio


def MAR(daily_ret):
    ar = ann_return(daily_ret)
    maxdd, _, _ = max_drawdown(daily_ret)
    return ar / abs(maxdd)


def max_drawdown(daily_cum_ret):
    balance = pd.Series(daily_cum_ret.flatten())
    highlevel = balance.rolling(
        min_periods=1, window=len(balance), center=False).max()
    # abs drawdown
    drawdown = balance - highlevel
    maxdd = np.min(drawdown)
    maxdd10 = drawdown.sort_values(ascending=True).iloc[:10].mean()
    # relative drawdown
    dd_ratio = drawdown / (highlevel + 1)
    maxdd_ratio = np.min(dd_ratio)
    return maxdd, maxdd10, maxdd_ratio


def pnl(signal, price, dayclose, slip=2, tick_size=0.01):

    n = signal.shape[0]
    cur_holding = np.zeros(n)  # num of stock
    asset = np.zeros(n)  # current asset
    asset[0] = 100000000
    ret = np.zeros(n)
    cost = np.zeros(n)

    dayclose = dayclose[dayclose.shape[0]-n:]
    for i in range(n):
        if i > 0:
            ret[i] = cur_holding[i - 1] * (price[i] - price[i - 1])
            # ret = change of price x cur_holding - cost
            asset[i] = asset[i - 1] + ret[i]
        money = signal[i] * asset[i] - \
            cur_holding[i - 1] * price[i]  # money to invest
        det_holding = (money / (price[i])).astype(np.int)
        cost[i] = abs(det_holding) * slip * \
            tick_size  # transaction cost incurred
        ret[i] = ret[i] - cost[i]
        cur_holding[i] = cur_holding[i - 1] + det_holding  # n of holding stock
        asset[i] = asset[i] - cost[i]  # change of asset = ret

    cum_ret = asset / asset[0] - 1
    daily_cum_ret = cum_ret[dayclose.astype(bool)]
    daily_ret = daily_cum_ret - np.roll(daily_cum_ret, 1)
    daily_ret[0] = daily_cum_ret[0]
    dayopen = np.roll(dayclose.astype(bool), 1)
    dayopen[0] = True
    open_asset = (asset + cost)[dayopen]
    if dayclose[-1] != 1:
        open_asset = open_asset[:-1]
    daily_ret_pct = daily_ret / open_asset  # percentage daily return

    det_holding = cur_holding - np.roll(cur_holding, 1)  # compute turnover
    det_holding[0] = cur_holding[0]
    cum_det_holding = abs(det_holding).cumsum()
    daily_cum_det_holding = cum_det_holding[dayclose.astype(bool)]
    turnover = daily_cum_det_holding - np.roll(daily_cum_det_holding, 1)
    turnover[0] = daily_cum_det_holding[0]
    avg_turnover = np.mean(turnover)

    return daily_cum_ret, daily_ret_pct, avg_turnover, turnover


def performance(paras_tuple, signal_input, signal_func,
                price, dayclose, pnl_paras, mode='both'):
    # get signal sequence for each bar
    signal_input.extend(paras_tuple)
    signal = signal_func(signal_input)

    # train test split
    signal_train, signal_test = train_test_split(
        signal, test_size=0.3, shuffle=False)
    if mode == 'train':
        signal_used = signal_train
    elif mode == 'test':
        signal_used = signal_test
    else:
        signal_used = signal

    signal = signal_used.to_numpy()
    price = price.to_numpy()
    slip, tick_size = pnl_paras['slip'], pnl_paras['tick_size']

    n = signal.shape[0]
    cur_holding = np.zeros(n)  # num of stock
    asset = np.zeros(n)  # current asset
    asset[0] = 100000000
    ret = np.zeros(n)
    cost = np.zeros(n)
    for i in range(n):
        if i > 0:
            ret[i] = cur_holding[i - 1] * (price[i] - price[i - 1])
            # ret = change of price x cur_holding - cost
            asset[i] = asset[i - 1] + ret[i]
        money = signal[i] * asset[i] - \
            cur_holding[i - 1] * price[i]  # money to invest
        det_holding = (money / (price[i])).astype(np.int)
        cost[i] = abs(det_holding) * slip * \
            tick_size  # transaction cost incurred
        ret[i] = ret[i] - cost[i]
        cur_holding[i] = cur_holding[i - 1] + det_holding  # n of holding stock
        asset[i] = asset[i] - cost[i]  # change of asset = ret

    cum_ret = asset / asset[0] - 1
    daily_cum_ret = cum_ret[dayclose.astype(bool)]

    balance = pd.Series(daily_cum_ret.flatten())
    highlevel = balance.rolling(
        min_periods=1, window=len(balance), center=False).max()
    drawdown = balance - highlevel

    return daily_cum_ret, drawdown, price-price[0]


def select_paras(paras_tuple, signal_input, signal_func,
                 price, dayclose, pnl_paras, mode='train'):
    signal_input.extend(paras_tuple)
    signal = signal_func(signal_input)

    # train test split
    signal_train, signal_test = train_test_split(
        signal, test_size=0.3, shuffle=False)

    if mode == 'train':
        signal_used = signal_train
    else:
        signal_used = signal_test

    # output criteria
    daily_cum_pct, daily_ret_pct, avg_turnover, turnover = pnl(signal_used.to_numpy(), price.to_numpy(), dayclose,
                                                               **pnl_paras)
    sharpe = sharpe_ratio(daily_ret_pct)
    mar = MAR(daily_ret_pct)
    annprofit = ann_return(daily_ret_pct)
    maxdd, maxdd10, maxdd_ratio = max_drawdown(daily_cum_pct)

    return sharpe, mar, annprofit, maxdd, maxdd10, maxdd_ratio, avg_turnover


def save_result(result, para_list, para_name):
    sharpe_list = [res[0] for res in result]
    mar_list = [res[1] for res in result]
    annprofit_list = [res[2] for res in result]
    maxdd_list = [res[3] for res in result]
    maxdd10_list = [res[4] for res in result]
    maxdd_ratio_list = [res[5] for res in result]
    avg_turnover_list = [res[6] for res in result]

    result = pd.DataFrame({'paras': para_list, 'sharpe': sharpe_list, 'mar': mar_list,
                           'annprofit': annprofit_list, 'maxdd': maxdd_list, 'maxdd10': maxdd10_list,
                           'maxddratio': maxdd_ratio_list, 'avg_turnover': avg_turnover_list})

    for i, para in enumerate(para_name):
        result[para] = [t[i] for t in result['paras']]
    result = result.drop('paras', axis=1)

    return result
