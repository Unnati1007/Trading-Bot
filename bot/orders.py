import logging

def place_order(client, symbol, side, order_type, quantity, price=None, tp_percent=None, sl_percent=None):
    try:
        # Place the main order
        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
        else:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

        logging.info(f"Main Order Response: {order}")
        
        # For bracket orders, we need a reference price
        exec_price = float(order.get('avgPrice', 0))
        if exec_price == 0 and price:
            exec_price = float(price)
            
        # Place Bracket Orders (Take-Profit & Stop-Loss)
        if (tp_percent or sl_percent) and exec_price > 0:
            opp_side = "SELL" if side == "BUY" else "BUY"
            
            if tp_percent:
                tp_price = exec_price * (1 + (tp_percent/100.0)) if side == "BUY" else exec_price * (1 - (tp_percent/100.0))
                tp_price = round(tp_price, 2)
                
                tp_order = client.futures_create_order(
                    symbol=symbol,
                    side=opp_side,
                    type="TAKE_PROFIT_MARKET",
                    quantity=quantity,
                    stopPrice=tp_price,
                    reduceOnly=True
                )
                logging.info(f"TP Order Response: {tp_order}")
                order['tp_price'] = tp_price
                
            if sl_percent:
                sl_price = exec_price * (1 - (sl_percent/100.0)) if side == "BUY" else exec_price * (1 + (sl_percent/100.0))
                sl_price = round(sl_price, 2)
                
                sl_order = client.futures_create_order(
                    symbol=symbol,
                    side=opp_side,
                    type="STOP_MARKET",
                    quantity=quantity,
                    stopPrice=sl_price,
                    reduceOnly=True
                )
                logging.info(f"SL Order Response: {sl_order}")
                order['sl_price'] = sl_price

        return order

    except Exception as e:
        logging.error(f"Error placing order: {e}")
        raise
