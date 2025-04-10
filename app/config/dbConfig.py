import psycopg2
import time
import logging

def create_db_connection(config, retries=5, delay=5):
    """
    Establish a connection to the PostgreSQL database with retry logic.

    Args:
        config (dict): Configuration dictionary with database credentials.
        retries (int): Number of retry attempts.
        delay (int): Delay in seconds between retries.

    Returns:
        conn (object): PostgreSQL connection object if successful.
    """
    attempt = 0
    while attempt < retries:
        try:
            print("Reading from db details: user=", str(config.get("DB_USER")),
                  " host=", str(config.get("DB_HOST")),
                  " port=", str(config.get("DB_PORT")),
                  " database=", str(config.get("DB_NAME")))

            conn = psycopg2.connect(
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
            conn.autocommit = True
            logging.info("Database connection successful.")

            try:
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS nse_stocks (
                    id SERIAL,
                    stock_symbol TEXT UNIQUE NOT NULL
                );""")
                cursor.execute("""CREATE INDEX IF NOT EXISTS idx_stock_symbol 
                    ON nse_stocks (stock_symbol);""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS stock_financials (
                    stock_symbol TEXT PRIMARY KEY,
                    earnings_yield FLOAT,
                    return_on_capital FLOAT,
                    market_cap BIGINT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );""")
            except Exception as e:
                logging.warning("Error creating table or index: %s", str(e))

            return conn

        except psycopg2.OperationalError as e:
            logging.warning(f"Attempt {attempt+1}/{retries} - DB not ready yet: {e}")
            time.sleep(delay)
            attempt += 1

        except Exception as e:
            logging.error(f"Unexpected DB error: {e}")
            break

    # Final fallback: try to connect to 'postgres' and create the DB
    try:
        logging.info("Trying to create the database as a last resort.")
        conn = psycopg2.connect(
            dbname="postgres",
            user=config.get("DB_USER"),
            password=config.get("DB_PASSWORD"),
            host=config.get("DB_HOST"),
            port=config.get("DB_PORT", 5432)
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {config.get('DB_NAME')}")
        logging.info("Database %s created successfully.", config.get("DB_NAME"))

        return create_db_connection(config)  # Recursive retry after creation

    except Exception as e:
        logging.error("Failed to create database: %s", e)
        raise