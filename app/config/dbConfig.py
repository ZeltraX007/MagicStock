from sqlalchemy import create_engine
import psycopg2
import time
import logging

def create_db_connection(config, retries=5, delay=5):
    """
    Establish a PostgreSQL connection via psycopg2 and also create a SQLAlchemy engine.
    
    Returns:
        dict with:
            'raw_conn' : psycopg2 connection (for cursor-based operations),
            'engine'   : SQLAlchemy engine (for use with pandas, etc.)
    """
    attempt = 0
    while attempt < retries:
        try:
            print("Connecting to DB:", config.get("DB_NAME"))

            # Create psycopg2 connection
            raw_conn = psycopg2.connect(
                dbname=config.get("DB_NAME"),
                user=config.get("DB_USER"),
                password=config.get("DB_PASSWORD"),
                host=config.get("DB_HOST"),
                port=config.get("DB_PORT", 5432),
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=5
            )
            raw_conn.autocommit = True
            logging.info("✅ psycopg2 connection established.")

            # Ensure tables exist
            with raw_conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS nse_stocks (
                    id SERIAL,
                    stock_symbol TEXT UNIQUE NOT NULL
                );""")
                cursor.execute("""CREATE INDEX IF NOT EXISTS idx_stock_symbol 
                    ON nse_stocks (stock_symbol);""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS stock_financials (
                    stock_symbol         TEXT PRIMARY KEY,
                    earnings_yield       double precision NOT NULL,
                    return_on_capital    double precision NOT NULL,
                    market_cap           bigint NOT NULL,
                    updated_at           timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    magic_formula_rank   integer,
                    rank                 integer,
                    market_cap_category  TEXT,
                    last_rank            integer
                );""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS stock_rank_history (
                    id SERIAL PRIMARY KEY,
                    stock_symbol TEXT NOT NULL,
                    rank INTEGER NOT NULL,
                    magic_formula_rank INTEGER NOT NULL,
                    market_cap_category TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );""")

                cursor.execute("""CREATE INDEX IF NOT EXISTS idx_rank_history_symbol ON stock_rank_history(stock_symbol);""")

            # Create SQLAlchemy engine for Pandas
            engine = create_engine(
                f'postgresql+psycopg2://{config.get("DB_USER")}:{config.get("DB_PASSWORD")}@{config.get("DB_HOST")}:{config.get("DB_PORT")}/{config.get("DB_NAME")}'
            )
            logging.info("✅ SQLAlchemy engine created for pandas/sql tools.")

            return {
                "raw_conn": raw_conn,
                "engine": engine
            }

        except psycopg2.OperationalError as e:
            logging.warning(f"Attempt {attempt+1}/{retries} - DB not ready yet: {e}")
            time.sleep(delay)
            attempt += 1

        except Exception as e:
            logging.error(f"❌ Unexpected DB error: {e}")
            break

    # Fallback: Try creating the database if connection failed
    try:
        logging.info("🔁 Attempting DB creation as fallback.")
        admin_conn = psycopg2.connect(
            dbname="postgres",
            user=config.get("DB_USER"),
            password=config.get("DB_PASSWORD"),
            host=config.get("DB_HOST"),
            port=config.get("DB_PORT", 5432)
        )
        admin_conn.autocommit = True
        with admin_conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {config.get('DB_NAME')}")
        logging.info(f"✅ Database {config.get('DB_NAME')} created. Retrying connection...")

        return create_db_connection(config)

    except Exception as e:
        logging.error("❌ Failed to create database: %s", e)
        raise
