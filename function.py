import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import data_source


def prepare_tickers_suffix(tickers: list[str]) -> list[str]:
    return [f"{ticker}.JK" for ticker in tickers]


__indonesia_suffix = ".JK"


def get_market_capital(ticker: str, date: str) -> float:
    start_time = datetime.strptime(date, '%Y-%m-%d')
    end_time = start_time + timedelta(days=1)
    the_ticker = yf.Ticker(ticker)
    closed_price = the_ticker.history(
        start=start_time, end=end_time, raise_errors=True).iloc[0]['Close']
    gathered_share = the_ticker.get_shares_full(
        start=start_time, end=end_time)
    number_of_share = 0
    if gathered_share is not None:
        if not gathered_share.empty:
            number_of_share = gathered_share[0]
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
