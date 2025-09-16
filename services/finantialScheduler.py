import os
import pandas as pd
from yahooquery import Ticker
from app import app
from app.config.configLoader import CONFIG
from apscheduler.schedulers.background import BackgroundScheduler
from app import dbconnection
from datetime import datetime
import psycopg2
from curl_cffi import requests

def load_stocks_from_db():
    """Loads stock symbols from the PostgreSQL nse_stocks table."""
    conn = dbconnection["raw_conn"]
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT stock_symbol FROM nse_stocks;")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        app.logger.error(f"Error loading stock symbols from DB: {e}")
        return []

def get_financials():
    """Processes stock symbols from file and calculates Magic Formula rankings."""
    # Create a session that impersonates Chrome
    session = requests.Session(impersonate="chrome")
    stock_symbols = load_stocks_from_db() # Uncomment this line to load from DB
    # For testing, we can use a hardcoded list of stock symbols
    # stock_symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "HDFC.NS", "KOTAKBANK.NS", "LT.NS", "ITC.NS","20MICRONS.NS","21STCENMGM.NS"]

    app.logger.info(f"stock_symbols: {stock_symbols}")
    skipped = []

    all_stock_results = []
    conn = dbconnection["raw_conn"]

    for stock_symbol in stock_symbols:
        try:
            stock = Ticker(
            stock_symbol,
            asynchronous=True,
            session=session
        )

            # Fetch financial statements
            income_statement = stock.income_statement()
            balance_sheet = stock.balance_sheet()
            summary_detail = stock.summary_detail.get(stock_symbol, {})

            # Function to safely extract the latest non-null value
            def get_latest_value(series):
                return series.dropna().iloc[0] if isinstance(series, pd.Series) and not series.dropna().empty else None
            
            def safe_div(numerator, denominator):
                try:
                    if denominator == 0 or pd.isna(denominator):
                        return None
                    result = numerator / denominator
                    if not pd.isna(result) and result not in [float("inf"), float("-inf")]:
                        return result
                    return None
                except Exception:
                    return None

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

                earnings_yield = safe_div(net_interest_income , market_cap)
                return_on_capital = safe_div(net_interest_income , (deposits + total_liabilities))

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

                earnings_yield = safe_div(ebit, enterprise_value)
                return_on_capital = safe_div(ebit, (net_working_capital + net_fixed_assets))

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
        
    app.logger.info(f"all processed stock results: {all_stock_results}")

    #Caludate the rankings
    df = pd.DataFrame(all_stock_results)

    # Skip ranking if empty
    if not df.empty:
        df["Market Cap"] = pd.to_numeric(df["Market Cap"], errors="coerce")

        def categorize_market_cap(value):
            if value >= 500_000_000_000:
                return "LARGE"
            elif value >= 100_000_000_000:   
                return "MID"
            elif value >= 10_000_000_000:    
                return "SMALL"
            else:
                return "NO CAP"

        df["market_cap_category"] = df["Market Cap"].apply(categorize_market_cap)
        df["earnings_yield_rank"] = df["Earnings Yield"].rank(ascending=False, method="min")
        df["roc_rank"] = df["Return on Capital"].rank(ascending=False, method="min")
        df["magic_formula_rank"] = df["earnings_yield_rank"] + df["roc_rank"]
        df = df.sort_values(by="magic_formula_rank").reset_index(drop=True)
        df["rank"] = df.index + 1

    # Convert DataFrame back to dicts
    all_stock_results = df.to_dict(orient="records")

    #insert the stock results into the database
    try:
        with conn.cursor() as cursor:
            for result in all_stock_results:
                if None in result.values():
                    app.logger.info(f"⚠️ Skipping {result['Stock']} due to missing data")
                    skipped.append(result["Stock"])
                    continue
                cursor.execute("""
                    INSERT INTO stock_financials (
                        stock_symbol, earnings_yield, return_on_capital, market_cap, 
                        updated_at, magic_formula_rank, rank, market_cap_category
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (stock_symbol) DO UPDATE SET
                        earnings_yield = EXCLUDED.earnings_yield,
                        return_on_capital = EXCLUDED.return_on_capital,
                        market_cap = EXCLUDED.market_cap,
                        updated_at = EXCLUDED.updated_at,
                        last_rank = stock_financials.rank,
                        magic_formula_rank = EXCLUDED.magic_formula_rank,
                        rank = EXCLUDED.rank,
                        market_cap_category = EXCLUDED.market_cap_category;
                """, (
                    str(result["Stock"]),
                    float(result["Earnings Yield"]),
                    float(result["Return on Capital"]),
                    int(result["Market Cap"]),
                    datetime.now(),
                    int(result["magic_formula_rank"]),
                    int(result["rank"]),
                    result["market_cap_category"]
                ))

                # Also insert into stock_rank_history
                cursor.execute("""
                    INSERT INTO stock_rank_history (
                        stock_symbol, rank, magic_formula_rank, market_cap_category
                    )
                    VALUES (%s, %s, %s, %s);
                """, (
                    str(result["Stock"]),
                    int(result["rank"]),
                    int(result["magic_formula_rank"]),
                    str(result["market_cap_category"])
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

get_financials() # Uncomment this line to run the function immediately

# Initialize Scheduler
scheduler = BackgroundScheduler()

# Run the job every 24 hours (instead of 20 seconds)
scheduler.add_job(func=get_financials, trigger="interval", days=90)

# Start the scheduler
scheduler.start()
