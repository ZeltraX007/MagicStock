from app import app
import pandas as pd
import json
from app.config.configLoader import CONFIG
from app import dbconnection

def getStockRanks(data, headers):
    """
    Rank stocks according to the Magic Formula by Joel Greenblatt and return JSON output with Market Cap Category.

    Args:
        data (dict): Request data containing "marketCap".
        headers (dict): Request headers (not used currently).

    Returns:
        tuple: (structured response as dict, error if any)
    """
    app.logger.info("🟡 Entered getStockRanks function")

    market_cap_category = data.get("marketCap")
    app.logger.debug(f"📥 Received marketCap: {market_cap_category}")

    # Validate marketCap input
    valid_categories = ["LARGE", "MID", "SMALL"]
    if market_cap_category and market_cap_category not in valid_categories:
        app.logger.warning("⚠️ Invalid marketCap provided")
        return None, ValueError("Invalid marketCap value. Must be one of: LARGE, MID, SMALL.")

    try:
        # Load from database instead of CSV
        query = """
            SELECT 
                stock_symbol AS Stock, 
                earnings_yield AS "Earnings Yield", 
                return_on_capital AS "Return on Capital", 
                market_cap AS "Market Cap" 
            FROM stock_financials;
        """
        df = pd.read_sql_query(query, dbconnection)
        app.logger.info(f"📊 Loaded {len(df)} rows from stock_financials table")

        # Convert Market Cap to numeric for filtering
        df["Market Cap"] = pd.to_numeric(df["Market Cap"], errors="coerce")

        # Function to categorize market cap
        def categorize_market_cap(value):
            if value > 200_000_000_000:
                return "LARGE"
            elif 50_000_000_000 <= value <= 200_000_000_000:
                return "MID"
            elif 5_000_000_000 <= value <= 50_000_000_000:
                return "SMALL"
            else:
                return "NO CAP"

        # Assign Market Cap Category
        df["Market Cap Category"] = df["Market Cap"].apply(categorize_market_cap)
        app.logger.info("🏷️ Assigned Market Cap Categories")

        # Apply filtering if marketCap was provided
        if market_cap_category:
            df = df[df["Market Cap Category"] == market_cap_category]

        # Ensure column names are correct
        df.columns = ["Stock", "Earnings Yield", "Return on Capital", "Market Cap", "Market Cap Category"]

        # Rank stocks based on Earnings Yield and ROC
        df["Earnings Yield Rank"] = df["Earnings Yield"].rank(ascending=False, method="min")
        df["ROC Rank"] = df["Return on Capital"].rank(ascending=False, method="min")
        app.logger.info("📈 Ranked stocks by Earnings Yield and Return on Capital")

        # Compute the final Magic Formula rank
        df["Magic Formula Rank"] = df["Earnings Yield Rank"] + df["ROC Rank"]
        # Sort stocks by Magic Formula Rank 
        df = df.sort_values(by="Magic Formula Rank").reset_index(drop=True)
        df["Rank"] = df.index + 1
        app.logger.info("🎯 Calculated final Magic Formula Rank")

        # Rename columns for output
        df = df.rename(columns={
            "Stock": "stock",
            "Magic Formula Rank": "magicFormulaRank",
            "Rank": "rank",
            "Market Cap Category": "marketCapCategory"
        })

        # Convert to list of dicts
        stocks = df[["stock", "magicFormulaRank", "rank", "marketCapCategory"]].to_dict(orient="records")
        app.logger.info(f"✅ Prepared response with {len(stocks)} ranked stocks")

        return stocks, None

    except Exception as e:
        app.logger.error(f"❌ Error processing stock ranking: {e}")
        return None, e
    