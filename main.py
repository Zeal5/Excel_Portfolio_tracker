import pandas as pd
from pprint import pprint

# import xlsxwriter


class TickerData:
    def __init__(self, ticker: str):
        self.ticker = ticker

        self.avg_buy_price: float = 0  # average method uses this
        self.avg_sell_price: float = 0
        self.breakeven_price: float = 0
        self.holdings: float = 0  # average method uses this
        self.holdings_sold: float = 0
        self.total_cost: float = 0
        self.total_profit: float = 0
        # self.lowest_buy :float= 0
        # self.highest_buy :float=0

    def calc_average(self, price: float, _amount: float):
        """get old avg.price add new price and divide by total amount"""
        self.holdings += _amount
        self.total_cost += price * _amount
        # print(f"amount {self.holdings}\ttotal cost : {self.total_cost}")
        self.avg_buy_price = self.total_cost / self.holdings

    def calc_break_even_price(self, _price: float, _amount_sold: float):
        self.holdings -= _amount_sold
        self.holdings_sold += _amount_sold
        self.total_cost -= _price * _amount_sold
        self.total_profit += _price * _amount_sold
        self.avg_sell_price = self.total_profit / self.holdings_sold
        self.breakeven_price = self.total_cost / self.holdings


def calculate_average(_ticker: str, _df: pd.DataFrame) -> dict:
    """Calculate average price for each ticker Df from all the entries Df"""
    ticker = TickerData(_ticker)

    for index, row in _df.iterrows():
        # print(index, row)
        # print(f'index {index} : series {row["side"]}')
        _price: float = float(row["price"])
        _amount = float(row["units"])
        if row["side"] == "buy":
            ticker.calc_average(_price, _amount)
        else:
            ticker.calc_break_even_price(_price, _amount)

    summary = {
        "ticker": ticker.ticker,
        "average_buy_price": ticker.avg_buy_price,
        "average_sell_price": ticker.avg_sell_price,
        "breakeven_price": ticker.breakeven_price,
        "qty": ticker.holdings,
        "qty_sold": ticker.holdings_sold,
        "total_cost": ticker.total_cost,
        "total_profit": ticker.total_profit,
    }
    return summary


def load_excel(_sheet_name: str):
    xl = pd.ExcelFile(_sheet_name)
    df = xl.parse("Sheet1")
    df.columns = df.columns.str.lower()
    df = df.map(lambda x: x.strip().lower() if type(x) == str else x)
    df = df.dropna()
    print(df)
    print("-" * 50)
    return df


def get_unique_ticker(_df: pd.DataFrame) -> set:
    """Return unique tickers from dataframe"""
    tickers = {i.lower().strip() for i in _df["ticker"].tolist()}
    print(tickers)
    return tickers


def main():
    sheet_name = "Book1.xlsx"
    df = load_excel(sheet_name)
    unique_tickers = get_unique_ticker(df)
    summary_dict = {}
    for ticker in unique_tickers:
        """Seperate rows for each ticker into df"""
        # print(ticker)
        df_ticker = df.loc[df["ticker"] == ticker]
        # print(df_ticker)
        summary_dict[ticker] = calculate_average(ticker, df_ticker)

    # pprint(summary_dict, indent =3)
    new_df = pd.DataFrame(summary_dict)
    new_df = new_df.transpose()
    # new_df.drop(new_df.index[0], inplace=True)
    # print(new_df)
    # # new_df.to_excel("Book2.xlsx", sheet_name = "summary")
    print(new_df)
    with pd.ExcelWriter('Book2.xlsx', mode='a',engine="openpyxl", if_sheet_exists="overlay") as writer:
       new_df.to_excel(writer, sheet_name='summary',header= False,index=False, startrow= 1)
    print('done')



main()
