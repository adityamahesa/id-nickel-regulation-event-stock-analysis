def prepare_tickers_suffix(tickers: list[str]) -> list[str]:
    return [ticker+".JK" for ticker in tickers]
