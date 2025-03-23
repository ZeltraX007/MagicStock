from app import app
import pandas as pd
import json
from app.config.configLoader import CONFIG

def getStockRanks(data, headers):
    """
    Rank stocks according to the Magic Formula by Joel Greenblatt and return JSON output with Market Cap Category.

    Args:
        data (dict): Request data containing "marketCap".
        headers (dict): Request headers (not used currently).

    Returns:
        tuple: (structured response as dict, error if any)
    """

    market_cap_category = data.get("marketCap")

    # Validate marketCap input
    valid_categories = ["LARGE", "MID", "SMALL"]
    if market_cap_category and market_cap_category not in valid_categories:
        app.logger.info("Market Cap not in List")
        return None, ValueError("Market Cap not in List")

    try:
        # Load the CSV file
        df = pd.read_csv(CONFIG.get("FINANCIAL_DATA_PATH"))

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

        # Apply filtering if marketCap was provided
        if market_cap_category:
            df = df[df["Market Cap Category"] == market_cap_category]

        # Ensure column names are correct
        df.columns = ["Stock", "Earnings Yield", "Return on Capital", "Market Cap", "Market Cap Category"]

        # Rank stocks based on Earnings Yield (higher is better)
        df["Earnings Yield Rank"] = df["Earnings Yield"].rank(ascending=False, method="min")

        # Rank stocks based on Return on Capital (higher is better)
        df["ROC Rank"] = df["Return on Capital"].rank(ascending=False, method="min")

        # Compute the final Magic Formula rank (sum of individual ranks)
        df["Magic Formula Rank"] = df["Earnings Yield Rank"] + df["ROC Rank"]

        # Sort stocks by Magic Formula Rank (lower is better)
        df = df.sort_values(by="Magic Formula Rank").reset_index(drop=True)

        # Add a sequential rank column (starting from 1)
        df["Rank"] = df.index + 1

        # Rename columns for API response
        df = df.rename(columns={
            "Stock": "stock",
            "Magic Formula Rank": "magicFormulaRank",
            "Rank": "rank",
            "Market Cap Category": "marketCapCategory"
        })

        # Convert DataFrame to dictionary
        stocks = df[["stock", "magicFormulaRank", "rank", "marketCapCategory"]].to_dict(orient="records")

        return stocks, None

    except Exception as e:
        app.logger.error(f"Error processing stock ranking: {e}")
        return None, e
    