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
    try:
        db_path = os.path.join("src", "data", "example_results.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        connection = sqlite3.connect(db_path)
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
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        #error involving db creation
    except Exception as e:
        #error involving path
        print(f"Unexpected error: {e}")



@app.get("/run-testing")#defined a route to get the api response
async def run_testing():
    #  link to pytest later
    result = {"endpoint": "test/api", "status": "passed", "response_time": 0.1}
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