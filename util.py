from multiprocessing.pool import ThreadPool
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import data_source


def prepare_tickers_suffix(tickers: list[str]) -> list[str]:
    return [f'{ticker}.JK' for ticker in tickers]


__indonesia_suffix = '.JK'


def __get_closed_price_for_market_value(ticker: str, start_time: datetime, end_time: datetime) -> float:
    the_ticker = yf.Ticker(ticker)
    return the_ticker.history(start=start_time, end=end_time, raise_errors=True).iloc[0]['Close']


def __get_number_of_share_for_market_value(ticker: str, start_time: datetime, end_time: datetime) -> int:
    the_ticker = yf.Ticker(ticker)

    gathered_share = the_ticker.get_shares_full(start=start_time, end=end_time)
    number_of_share = 0
    if gathered_share is not None:
        if not gathered_share.empty:
            number_of_share = gathered_share[0]

    return number_of_share


def get_market_capital(ticker: str, date: str) -> float:
    start_time = datetime.strptime(date, '%Y-%m-%d')
    end_time = start_time + timedelta(days=1)

    pool = ThreadPool(processes=2)

    async_closed_price = pool.apply_async(
        __get_closed_price_for_market_value, (ticker, start_time, end_time))
    async_number_of_share = pool.apply_async(
        __get_number_of_share_for_market_value, (ticker, start_time, end_time))

    closed_price = async_closed_price.get()
    number_of_share = async_number_of_share.get()

    del pool

    return closed_price * number_of_share


def prepare_top_10_tickers_per_sector(date: str) -> pd.DataFrame:
    gathered_market_values: list[dict] = []
    for sector in data_source.tickers.keys():
        gathered_market_values_per_sector: list[dict] = []
        for sector_member in data_source.tickers[sector]:
            try:
                market_value = get_market_capital(
                    f'{sector_member}{__indonesia_suffix}', date)
            except Exception:
                continue
            gathered_market_values_per_sector.append({
                'sector': sector,
                'ticker': sector_member,
                'market_value': market_value
            })
        dataframe_per_sector = pd.DataFrame(gathered_market_values_per_sector)
        dataframe_per_sector = dataframe_per_sector.sort_values(
            'market_value', ascending=False)
        dataframe_per_sector = dataframe_per_sector.iloc[0:10]
        gathered_market_values.extend(dataframe_per_sector.to_dict('records'))
    return pd.DataFrame(gathered_market_values)


def generate_average_return_per_sector(data: pd.DataFrame, start_date: str, end_date: str = None) -> pd.DataFrame:
    start_time = datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)
    end_time = start_time + timedelta(days=2)
    if end_date:
        end_time = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

    concat_object: dict[str, pd.Series] = {}
    for sector in data_source.tickers.keys():
        tickers_sectorized_df = data[data['sector'] == sector]
        if len(tickers_sectorized_df) < 1:
            continue
        tickers_sectorized_series = tickers_sectorized_df['ticker']
        tickers_sectorized = tickers_sectorized_series.to_list()
        tickers_sectorized = prepare_tickers_suffix(tickers=tickers_sectorized)
        prices_per_sector = yf.download(
            tickers=tickers_sectorized, start=start_time, end=end_time)
        prices_per_sector_close = prices_per_sector['Close']
        return_of_tickers = prices_per_sector_close.pct_change(
            fill_method='pad')
        return_of_tickers = return_of_tickers.iloc[1:]
        sectoral_average_return = return_of_tickers.mean(axis=1)
        concat_object[sector] = sectoral_average_return
    average_return_per_sector = pd.concat(concat_object, axis=1)

    return average_return_per_sector


def set_relativity_label(data: pd.DataFrame) -> pd.DataFrame:
    first_column_name = data.columns[0]
    data = data.sort_values(first_column_name, ascending=False)

    length_of_data = len(data)
    half_point = length_of_data / 2

    data.insert(loc=len(data.columns), column='is_more_related', value=np.nan)
    for i in range(len(data)):
        is_more_related = i < half_point
        data.loc[data.index[i], 'is_more_related'] = is_more_related

    return data


def set_tickers_relativity_label(data: pd.DataFrame, relativity_map: pd.DataFrame) -> pd.DataFrame:
    data.insert(loc=len(data.columns), column='is_more_related', value=np.nan)
    for i in range(len(data)):
        sector = data.loc[data.index[i], 'sector']
        is_more_related = relativity_map.loc[sector]['is_more_related']
        data.loc[data.index[i], 'is_more_related'] = is_more_related

    return data
