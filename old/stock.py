import os
import pandas as pd
from yahooquery import Ticker

STOCKS_FILE = "stocks_list.txt"
RESULTS_FILE = "nse_magic_formula_results.csv"

def get_all_nse_stock():
    """Fetches all NSE stock symbols and stores them in a file."""
    nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(nse_url)
    stock_symbols = [symbol + ".NS" for symbol in df["SYMBOL"].tolist()]

    # Save to file
    with open(STOCKS_FILE, "w") as f:
        f.write("\n".join(stock_symbols))

    return stock_symbols

def load_stocks_from_file():
    """Loads stock symbols from file."""
    if os.path.exists(STOCKS_FILE):
        with open(STOCKS_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def remove_stock_from_file(stock_symbol):
    """Removes a processed stock from the stocks list file."""
    stocks = load_stocks_from_file()
    stocks.remove(stock_symbol)
    
    with open(STOCKS_FILE, "w") as f:
        f.write("\n".join(stocks))

def save_stock_result(stock_data):
    """Appends a stock's financial results to the results CSV file."""
    df = pd.DataFrame([stock_data])
    if not os.path.exists(RESULTS_FILE):
        df.to_csv(RESULTS_FILE, index=False)  # Create new file
    else:
        df.to_csv(RESULTS_FILE, mode="a", header=False, index=False)  # Append to existing file

def get_financials():
    """Processes stock symbols from file and calculates Magic Formula rankings."""
    stock_symbols = load_stocks_from_file()
    
    if not stock_symbols:
        print("✅ No stocks left to process!")
        return

    skipped = []

    for stock_symbol in stock_symbols:
        try:
            stock = Ticker(stock_symbol)

            # Fetch financial statements
            income_statement = stock.income_statement()
            balance_sheet = stock.balance_sheet()
            summary_detail = stock.summary_detail.get(stock_symbol, {})

            # Function to safely extract the latest non-null value
            def get_latest_value(series):
                return series.dropna().iloc[0] if isinstance(series, pd.Series) and not series.dropna().empty else None

            # Identify if the stock is a bank
            asset_profile = stock.asset_profile
            if not isinstance(asset_profile, dict) or stock_symbol not in asset_profile or not isinstance(asset_profile[stock_symbol], dict):
                print(f"⚠️ Warning: Failed to fetch sector info for {stock_symbol}")
                sector_info = "Unknown"
            else:
                sector_info = asset_profile[stock_symbol].get("sector", "")

            is_bank = "Bank" in sector_info or "Financial" in sector_info

            market_cap = summary_detail.get("marketCap")
            if market_cap is None:
                print(f"⚠️ Skipping {stock_symbol}: Market Cap missing")
                skipped.append(stock_symbol)
                continue

            if is_bank:
                print(f"🏦 {stock_symbol} is a bank. Using bank-specific metrics...\n")

                net_interest_income = get_latest_value(income_statement.get("NetInterestIncome"))
                deposits = get_latest_value(balance_sheet.get("Payables"))  # Often represents Deposits
                total_liabilities = get_latest_value(balance_sheet.get("TotalLiabilitiesNetMinorityInterest"))

                if None in [net_interest_income, deposits, total_liabilities]:
                    print(f"⚠️ Skipping {stock_symbol}: Missing financial data")
                    skipped.append(stock_symbol)
                    continue

                earnings_yield = net_interest_income / market_cap
                return_on_capital = net_interest_income / (deposits + total_liabilities)

            else:
                print(f"🏢 {stock_symbol} is a regular company. Using standard metrics...\n")

                ebit = get_latest_value(income_statement.get("EBIT"))
                cash = get_latest_value(balance_sheet.get("CashAndCashEquivalents"))
                current_assets = get_latest_value(balance_sheet.get("CurrentAssets"))
                total_assets = get_latest_value(balance_sheet.get("TotalAssets"))
                current_liabilities = get_latest_value(balance_sheet.get("CurrentLiabilities"))
                total_debt = get_latest_value(balance_sheet.get("TotalDebt"))

                if None in [ebit, cash, current_assets, total_assets, current_liabilities, total_debt]:
                    print(f"⚠️ Skipping {stock_symbol}: Missing financial data")
                    skipped.append(stock_symbol)
                    continue

                enterprise_value = market_cap + total_debt - cash
                net_working_capital = current_assets - current_liabilities
                net_fixed_assets = total_assets - current_assets

                earnings_yield = ebit / enterprise_value
                return_on_capital = ebit / (net_working_capital + net_fixed_assets)

            stock_result = {
                "Stock": stock_symbol,
                "Earnings Yield": earnings_yield,
                "Return on Capital": return_on_capital,
                "Market Cap": market_cap
            }

            # Save the stock result
            save_stock_result(stock_result)

            # Remove stock from file after processing
            remove_stock_from_file(stock_symbol)

        except Exception as e:
            print(f"❌ Error processing {stock_symbol}: {e}")
            skipped.append(stock_symbol)
            continue

    print(f"\n🔹 Processing complete. Skipped stocks ({len(skipped)}): {skipped}")
    print(f"✅ All results saved in {RESULTS_FILE}")

# Example Usage
if not os.path.exists(STOCKS_FILE):
    get_all_nse_stock()

get_financials()
