from execution.alpaca_executor import Executor
from universe.universe import Universe
from universe.filter import filter_universe

def main():
    exec = Executor()
    universe = Universe(exec.api)

    symbols = universe.get_all_symbols()
    filtered = filter_universe(exec.api, symbols)

    print("Raw symbols:", len(symbols))
    print("Filtered symbols:", len(filtered))
    print("Sample:", filtered[:10])

if __name__ == "__main__":
    main()