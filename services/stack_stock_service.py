from app import app
import pandas as pd
from app.config.configLoader import CONFIG
from apscheduler.schedulers.background import BackgroundScheduler
from app import dbconnection

def get_all_nse_stock():
    """Fetches all NSE stock symbols and stores them in a table."""
    nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    try:
        cursor = dbconnection.cursor()
        # Load data from NSE
        df = pd.read_csv(nse_url)

        # Extract stock symbols and append ".NS"
        stock_symbols = [(symbol + ".NS",) for symbol in df["SYMBOL"].tolist()]

        # # Get file path from CONFIG
        # stock_file_path = CONFIG.get("STOCKS_FILE")
        # if not stock_file_path:
        #     raise ValueError("STOCKS_FILE path is not set in CONFIG.")

        # Save to file
        # with open(stock_file_path, "w") as f:
        #     f.write("\n".join(stock_symbols))

        query = """
            INSERT INTO nse_stocks (stock_symbol)
            VALUES (%s)
            ON CONFLICT (stock_symbol) DO NOTHING;
        """

        query1 = """
            INSERT INTO stock_financials (stock_symbol)
            VALUES (%s)
            ON CONFLICT (stock_symbol) DO NOTHING;"""

        cursor.executemany(query, stock_symbols)

        cursor.executemany(query1, stock_symbols)

        # Commit the transaction
        dbconnection.commit()
        cursor.close()

        app.logger.info(f"Successfully fetched and stored {len(stock_symbols)} NSE stocks.")

    except Exception as e:
        app.logger.info(f"Error fetching NSE stock symbols: {e}")

# Initialize Scheduler
scheduler = BackgroundScheduler()

# Run the job every 24 hours (instead of 20 seconds)
scheduler.add_job(func=get_all_nse_stock, trigger="interval", seconds=100)

# Start the scheduler
scheduler.start()
