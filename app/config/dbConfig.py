import logging
import psycopg2
from psycopg2 import OperationalError

def create_db_connection(config):
    """
    Establish a connection to the PostgreSQL database.

    Args:
        config (dict): Configuration dictionary with database credentials.

    Returns:
        conn (object): PostgreSQL connection object if successful, else None.
    """
    print("Reading from db details: user=",str(config.get("DB_USER")),
                            " host=",str(config.get("DB_HOST")),
                            " port=",str(config.get("DB_PORT")),
                            " database=",str(config.get("DB_NAME")))
    try:
        # Extract database credentials from config
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
            postgres_nse_stock_db = """CREATE TABLE IF NOT EXISTS nse_stocks (
                id SERIAL,
                stock_symbol TEXT UNIQUE NOT NULL
            );"""
            cursor.execute(postgres_nse_stock_db)
            postgres_nse_stock_db_index = """CREATE INDEX IF NOT EXISTS idx_stock_symbol 
            ON nse_stocks (stock_symbol);"""
            cursor.execute(postgres_nse_stock_db_index)
        except Exception as e:
            logging.info(str(e))
        return conn

    except Exception as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        conn = psycopg2.connect(
            dbname="postgres",
            user=config.get("DB_USER"),
            password=config.get("DB_PASSWORD"),
            host=config.get("DB_HOST"),
            port=config.get("DB_PORT", 5432))
        conn.autocommit = True
        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        #Preparing query to create a database
        sql = '''CREATE database ''' +  config.get("DB_NAME")
        #Creating a database
        cursor.execute(sql)
        logging.info("Database created successful.")
        conn = create_db_connection(config)
        logging.info("Successfully created database %s", config.get("DB_NAME"))
        return conn
