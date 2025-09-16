from app import app
import pandas as pd
from app import dbconnection

def getStockRanks(data, headers):
    """
    Return ranked stocks precomputed in stock_financials table.

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
        # Load precomputed ranks from database
        query = """
            SELECT 
                stock_symbol AS stock,
                magic_formula_rank AS "magicFormulaRank",
                rank,
                market_cap_category AS "marketCapCategory",
                last_rank AS "lastRank"
            FROM stock_financials
            WHERE magic_formula_rank IS NOT NULL;
        """
        engine = dbconnection["engine"]
        df = pd.read_sql_query(query, engine)
        app.logger.info(f"📊 Loaded {len(df)} ranked stocks from DB")

        # Apply filtering if marketCap was provided
        if market_cap_category:
            df = df[df["marketCapCategory"] == market_cap_category]

        # Sort by rank to ensure proper order
        df = df.sort_values(by="rank").reset_index(drop=True)

        # Convert to list of dicts
        stocks = df[["stock", "magicFormulaRank", "rank", "marketCapCategory","lastRank"]].to_dict(orient="records")
        app.logger.info(f"✅ Prepared response with {len(stocks)} stocks")

        return stocks, None

    except Exception as e:
        app.logger.error(f"❌ Error retrieving ranked stocks: {e}")
        return None, e


def getStats():
    """
    Get summary statistics from the stock_financials table.

    Returns:
        tuple: (statistics as dict, error if any)
    """
    app.logger.info("📊 Entered getStockStats function")

    try:
        query = """
            SELECT 
                stock_symbol,
                earnings_yield,
                return_on_capital,
                market_cap_category,
                rank,
                last_rank
            FROM stock_financials
            WHERE rank IS NOT NULL;
        """
        engine = dbconnection["engine"]
        df = pd.read_sql_query(query, engine)

        total_stocks = len(df)

        # Market cap distribution
        market_cap_dist = df["market_cap_category"].value_counts().to_dict()

        # Average metrics
        avg_ey = df["earnings_yield"].mean()
        avg_roc = df["return_on_capital"].mean()

        # Rank movement (positive means stock moved up in rank)
        df["rank_change"] = df["last_rank"] - df["rank"]
        avg_rank_change = df["rank_change"].mean()
        max_gainer = df.loc[df["rank_change"].idxmax()] if not df.empty else None
        max_loser = df.loc[df["rank_change"].idxmin()] if not df.empty else None

        stats = {
            "totalStocks": total_stocks,
            "marketCapDistribution": market_cap_dist,
            "averageEarningsYield": round(avg_ey, 4) if avg_ey else None,
            "averageReturnOnCapital": round(avg_roc, 4) if avg_roc else None,
            "averageRankChange": round(avg_rank_change, 2) if avg_rank_change else None,
            "biggestGainer": {
                "stock": max_gainer["stock_symbol"],
                "rankChange": int(max_gainer["rank_change"]),
                "rank": int(max_gainer["rank"]),
                "lastRank": int(max_gainer["last_rank"])
            } if max_gainer is not None else None,
            "biggestLoser": {
                "stock": max_loser["stock_symbol"],
                "rankChange": int(max_loser["rank_change"]),
                "rank": int(max_loser["rank"]),
                "lastRank": int(max_loser["last_rank"])
            } if max_loser is not None else None,
        }

        app.logger.info("✅ Stock statistics computed successfully.")
        return stats, None

    except Exception as e:
        app.logger.error(f"❌ Failed to compute stock stats: {e}")
        return None, e