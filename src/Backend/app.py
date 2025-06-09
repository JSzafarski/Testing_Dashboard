from fastapi import FastAPI
import sqlite3
from datetime import datetime
import uvicorn
import os
app = FastAPI()


def initialise_db():
    """
    This function prepared the database structure
    :return: none
    """
    connection = sqlite3.connect("src\\data\\example_results.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            status TEXT,
            response_time FLOAT,
            timestamp TEXT
        )
    """)
    connection.commit()
    connection.close()


@app.get("/run-testing")
async def run_testing():
    #  link to pytest later
    result = {"endpoint": "test/api", "status": "pass", "response_time": 0.5}
    conn = sqlite3.connect("src/data/example_results.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO results (endpoint, status, response_time, timestamp) VALUES (?, ?, ?, ?)",
        (result["endpoint"], result["status"], result["response_time"], datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return {"message": "Tests checked", "result": result}

if __name__ == "__main__":
    initialise_db() #ensure the db file is initialised
    uvicorn.run(app, host="0.0.0.0", port=8000) #communicate with FastApi using ASGI