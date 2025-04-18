import pandas as pd


CONFIGS = {"Gateio": {"delimiter": "\t", "encoding": "utf-16"}}

REINDEX_LIST = ["ticker", "side", "price", "units", "totalcost"]

def read_gateio_orders(_file_path: str) -> pd.DataFrame:
    "Read a csv file and after cleaning it return only selected/imp rows in as df" ""

    file = pd.read_csv(_file_path, delimiter="\t", encoding="utf-16")
    file.columns = file.columns.str.lower()
    file = file.drop(["no", "order id", "time", "fee", "role"], axis=1)
    file = file.rename(
        columns={
            "trade type": "side",
            "pair": "ticker",
            "amount": "units",
            "total": "totalcost",
        }
    )
    file['side']   = file['side'].str.lower()
    file["ticker"] = file['ticker'].str.lower()
    file["ticker"] = file['ticker'].str.replace('/usdt','')
    file.reindex(columns=REINDEX_LIST)
    # Clean DF to return match 
    """
   side   ticker     price      units   totalcost
    buy    vanry  0.069100   249.1800   17.218338
    buy    vanry  0.069100   249.1700   17.217647
    buy     alph  2.360000     2.0000    4.720000
    """
    return file


def read_binance_orders(_file_path:str) ->pd.DataFrame:
    file = pd.read_excel(_file_path, "sheet1")
    file.columns = file.columns.str.lower()
    file = file.drop(['date(utc)','fee', 'fee coin'],axis=1)
    file = file.rename(
    columns={
        "type": "side",
        "market": "ticker",
        "amount": "units",
        "total": "totalcost",
    }
    )
    file['side']   = file['side'].str.lower()
    file['ticker'] = file['ticker'].str.lower()
    file['ticker'] = file['ticker'].str.replace('usdt','')
    file = file.reindex(columns=REINDEX_LIST)
    return file


def read_csv(_binance_path:str, _gateio_path : str)-> pd.DataFrame:
    gateio = read_gateio_orders(_gateio_path)
    binance = read_binance_orders(_binance_path)
    merger = pd.concat([gateio, binance],ignore_index=True)
    # pd.set_option('display.max_rows', None)
    # print(merger)
    return merger


