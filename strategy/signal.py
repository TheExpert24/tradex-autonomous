def generate_signal(prob, buy_th=0.51, sell_th=0.49):
    if prob > buy_th:
        return 1   # BUY
    elif prob < sell_th:
        return -1  # SELL
    else:
        return 0   # HOLD