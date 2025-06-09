import os
import pandas as pd
import sqlite3


def save_results_to_csv():
    """

    :return:
    """
    # Connect to database
    connection = sqlite3.connect("example_results.db")#need to ensure the db is created in the right place
    # in order to read it properly
    df = pd.read_sql_query('SELECT * FROM results', connection)
    connection.close() #close the database after we finish the read operation

    # Process and save to CSV
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.to_csv("src/data/test_results.csv", index=False)
    print("Results saved to src/data/test_results.csv")
    #effecitvely returns a list of dictionaries where each dictionary represents a row from the results table
    #that is present in the database
    return df.to_dict(orient="records")


if __name__ == "__main__":
    results = save_results_to_csv()
    print(f"Processed Results: {results}")