import myconfig
import pandas as pd
import ccxt
import time

def bot_plunger(is_in_position):
    # Config exchange
    bybit = ccxt.bybit({
        "enableRateLimit": True,
        "apiKey": myconfig.API_KEY,
        "secret": myconfig.SECRET,
    })

    # Connect to testnet
    bybit.set_sandbox_mode(True)

    # Set params
    btc_position = myconfig.POSITION_SIZE
    symbol = myconfig.SYMBOL
    low = myconfig.LOW_RES
    high = myconfig.HIGH_RES
    in_position = is_in_position

    # Get curr price, first bid
    def get_bid():
        order_book = bybit.fetch_order_book(symbol)
        bid = order_book["bids"][0][0]
        return bid 
    bid = get_bid()

    # Check conditions, make actions
    if bid > high:
        if in_position:
            close_position = bybit.create_order(symbol=symbol, type="MARKET", side="sell", amount=btc_position, params={"reduceOnly": True})
            print("Confirm resistance levels")
            return close_position
        else:
            params = {'positionSide': 'LONG'}
            order = bybit.create_order(symbol, 'market', 'buy', btc_position, params)
            in_position = True
    elif bid < low:
        if in_position:
            close_position = bybit.create_order(symbol=symbol, type="MARKET", side="buy", amount=btc_position, params={"reduceOnly": True})
            print("Confirm resistance levels")
            return close_position 
        else:
            params = {'positionSide': 'SHORT'}
            order = bybit.create_order(symbol, 'market', 'sell', btc_position, params)
            in_position = True
    else:
        pass
    time.sleep(300)
    bot_plunger(in_position)

bot_plunger(False)
