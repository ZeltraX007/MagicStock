from yahooquery import Ticker

def get_financials(stock_symbol):
    stock = Ticker(stock_symbol)

    # Fetch data
    income_statement = stock.income_statement()
    income_statement = income_statement.sort_values(by="asOfDate", ascending=False)
    balance_sheet = stock.balance_sheet()
    balance_sheet = balance_sheet.sort_values(by="asOfDate", ascending=False)
    cash_flow = stock.cash_flow()
    cash_flow = cash_flow.sort_values(by="asOfDate", ascending=False)

    # Helper function to extract latest non-null value
    def get_latest(series):
        return series.dropna().iloc[0] if series is not None and not series.dropna().empty else None

    # Check if the stock is a bank (banks usually don't have EBIT)
    asset_profile = stock.asset_profile
    if not isinstance(asset_profile, dict) or stock_symbol not in asset_profile or not isinstance(asset_profile[stock_symbol], dict):
        print(f"⚠️ Warning: Failed to fetch sector info for {stock_symbol}")
        sector_info = "Unknown"
    else:
        sector_info = asset_profile[stock_symbol].get("sector", "")
    is_bank = "Bank" in sector_info or "Financial" in sector_info

    if is_bank:
        print(f"🏦 {stock_symbol} is a bank. Using bank-specific metrics...\n")
        
        # Use Net Interest Income instead of EBIT
        net_interest_income = get_latest(income_statement.get("NetInterestIncome"))
        print(f"Net Interest Income (NII): {net_interest_income}")

        # Use Total Revenue instead of Operating Income
        total_revenue = get_latest(income_statement.get("TotalRevenue"))
        print(f"Total Revenue: {total_revenue}")

        # Use Deposits & Total Liabilities instead of Current Liabilities
        deposits = get_latest(balance_sheet.get("Payables"))  # 'Payables' often refers to Deposits
        total_liabilities = get_latest(balance_sheet.get("TotalLiabilitiesNetMinorityInterest"))
        print(f"Deposits: {deposits}")
        print(f"Total Liabilities: {total_liabilities}")

    else:
        print(f"🏢 {stock_symbol} is a regular company. Using standard metrics...\n")

        # Get EBIT
        ebit = get_latest(income_statement.get("EBIT"))
        print(f"EBIT: {ebit}")

        # Get Operating Income
        operating_income = get_latest(income_statement.get("OperatingIncome"))
        print(f"Operating Income: {operating_income}")

        # Get Current Assets
        current_assets = get_latest(balance_sheet.get("CurrentAssets"))
        print(f"Current Assets: {current_assets}")

        # Get Current Liabilities
        current_liabilities = get_latest(balance_sheet.get("CurrentLiabilities"))
        print(f"Current Liabilities: {current_liabilities}")

        # Get Total Debt
        total_debt = get_latest(balance_sheet.get("TotalDebt"))
        print(f"Total Debt: {total_debt}")

    # Common values for all stocks
    market_cap = stock.summary_detail.get(stock_symbol, {}).get("marketCap")
    print(f"Market Cap: {market_cap}")

    cash = get_latest(balance_sheet.get("CashAndCashEquivalents"))
    print(f"Cash: {cash}")

# Example: Checking a bank stock (HDFCBANK.NS) & a regular stock (INFY.NS)
get_financials("HDFCBANK.NS")
get_financials("3PLAND.NS")
