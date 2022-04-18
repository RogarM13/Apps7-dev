import psycopg2
import psycopg2.extras as extras

# postgres config (in prod would go to secrets)
POSTGRES_HOST = "127.0.0.1"
POSTGRES_PORT = "5432"
POSTGRES_DATABASE = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postpass123!"

conn = psycopg2.connect(
    database=POSTGRES_DATABASE,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
)

# functions
def create_table(table_name: str, conn=conn):
    cur = conn.cursor()
    try:
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS public.daily_report
        (Date DATE    NOT NULL,
        App  CHAR(255)   NOT NULL,
        Platform CHAR(50)   NOT NULL,
        Requests INT,
        Impressions INT,
        Revenue REAL,
        Currency CHAR(50)
        )
        ;"""
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        cur.close()
        return f"Table could not be created. Error occured: {e}"

    cur.close()
    return "Table created."


def insert_data_from_dataframe(df, table_name: str, conn=conn):

    tuples = [tuple(x) for x in df.to_numpy()]
    colnames = ",".join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, colnames)

    cur = conn.cursor()
    try:
        extras.execute_values(cur, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print("Error: %s" % e)
        conn.rollback()
        cur.close()

    cur.close()
    return "Data inserted."
