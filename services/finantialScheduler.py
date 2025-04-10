import os
import pandas as pd
from yahooquery import Ticker
from app import app
from app.config.configLoader import CONFIG
from apscheduler.schedulers.background import BackgroundScheduler
from app import dbconnection
from datetime import datetime
import psycopg2

def load_stocks_from_db():
    """Loads stock symbols from the PostgreSQL nse_stocks table."""
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute("SELECT stock_symbol FROM nse_stocks;")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        app.logger.error(f"Error loading stock symbols from DB: {e}")
        return []

def get_financials():
    """Processes stock symbols from file and calculates Magic Formula rankings."""
    # stock_symbols = load_stocks_from_db() # Uncomment this line to load from DB
    # For testing, we can use a hardcoded list of stock symbols
    stock_symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "HDFC.NS", "KOTAKBANK.NS", "LT.NS", "ITC.NS","20MICRONS.NS","21STCENMGM.NS"]

    skipped = []

    all_stock_results = []
    conn = dbconnection

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
                app.logger.info(f"⚠️ Warning: Failed to fetch sector info for {stock_symbol}")
                sector_info = "Unknown"
            else:
                sector_info = asset_profile[stock_symbol].get("sector", "")

            is_bank = "Bank" in sector_info or "Financial" in sector_info

            market_cap = summary_detail.get("marketCap")
            if market_cap is None:
                app.logger.info(f"⚠️ Skipping {stock_symbol}: Market Cap missing")
                skipped.append(stock_symbol)
                continue

            if is_bank:
                app.logger.info(f"🏦 {stock_symbol} is a bank. Using bank-specific metrics...\n")

                net_interest_income = get_latest_value(income_statement.get("NetInterestIncome"))
                deposits = get_latest_value(balance_sheet.get("Payables"))  # Often represents Deposits
                total_liabilities = get_latest_value(balance_sheet.get("TotalLiabilitiesNetMinorityInterest"))

                if None in [net_interest_income, deposits, total_liabilities]:
                    app.logger.info(f"⚠️ Skipping {stock_symbol}: Missing financial data")
                    skipped.append(stock_symbol)
                    continue

                earnings_yield = net_interest_income / market_cap
                return_on_capital = net_interest_income / (deposits + total_liabilities)

            else:
                app.logger.info(f"🏢 {stock_symbol} is a regular company. Using standard metrics...\n")

                ebit = get_latest_value(income_statement.get("EBIT"))
                cash = get_latest_value(balance_sheet.get("CashAndCashEquivalents"))
                current_assets = get_latest_value(balance_sheet.get("CurrentAssets"))
                total_assets = get_latest_value(balance_sheet.get("TotalAssets"))
                current_liabilities = get_latest_value(balance_sheet.get("CurrentLiabilities"))
                total_debt = get_latest_value(balance_sheet.get("TotalDebt"))

                if None in [ebit, cash, current_assets, total_assets, current_liabilities, total_debt]:
                    app.logger.info(f"⚠️ Skipping {stock_symbol}: Missing financial data")
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

            all_stock_results.append(stock_result)

        except Exception as e:
                app.logger.info(f"❌ Error processing {stock_symbol}: {e}")
                skipped.append(stock_symbol)
                continue
    #insert the stock results into the database
    try:
        with conn.cursor() as cursor:
            for result in all_stock_results:
                cursor.execute("""
                    INSERT INTO stock_financials (stock_symbol, earnings_yield, return_on_capital, market_cap, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (stock_symbol) DO UPDATE SET
                        earnings_yield = EXCLUDED.earnings_yield,
                        return_on_capital = EXCLUDED.return_on_capital,
                        market_cap = EXCLUDED.market_cap,
                        updated_at = EXCLUDED.updated_at;
                """, (
                    str(result["Stock"]),
                    float(result["Earnings Yield"]),
                    float(result["Return on Capital"]),
                    int(result["Market Cap"]),
                    datetime.now()
                ))
        conn.commit()
        app.logger.info("✅ Successfully stored financial data in DB.")

    except Exception as db_err:
        conn.rollback()
        app.logger.error(f"❌ Failed to store stock financials: {db_err}")

    # 🧹 Delete skipped stocks from DB if they exist
    try:
        if skipped:
            with conn.cursor() as cursor:
                cursor.executemany("""
                    DELETE FROM stock_financials WHERE stock_symbol = %s;
                """, [(symbol,) for symbol in skipped])
            conn.commit()
            app.logger.info(f"🗑️ Removed {len(skipped)} skipped stocks from stock_financials.")
    except Exception as del_err:
        conn.rollback()
        app.logger.error(f"❌ Failed to delete skipped stocks: {del_err}")

    app.logger.info(f"\n🔹 Processing complete. Skipped stocks ({len(skipped)}): {skipped}")
    app.logger.info(f"✅ All results saved in db")

# get_financials() # Uncomment this line to run the function immediately

# Initialize Scheduler
scheduler = BackgroundScheduler()

# Run the job every 24 hours (instead of 20 seconds)
scheduler.add_job(func=get_financials, trigger="interval", hours=100)

# Start the scheduler
scheduler.start()
