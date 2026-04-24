from execution.alpaca_executor import Executor

def main():
    exec = Executor()

    account = exec.account()

    print("Cash:", account.cash)
    print("Equity:", account.equity)
    print("Buying Power:", account.buying_power)

if __name__ == "__main__":
    main()