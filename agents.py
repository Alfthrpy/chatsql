import mysql.connector
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, HfApiModel, tool
load_dotenv()
def createConnection(user='root',password='password',host='127.0.0.1',database='sakila'):
    cnx = mysql.connector.connect(user=user, password=password,
                              host=host,
                              database=database)
    
    return cnx


def getAllTable(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return tables



def createColumnDesc(connection):
    DESC_TABLE = """"""
    cursor = connection.cursor()
    tables = getAllTable(connection)
    for table in tables:
        cursor.execute(f"DESCRIBE {table[0]}")
        columns = cursor.fetchall()

        DESC_TABLE += f"*{table[0].upper()}\n"
        for column in columns:
            column_name = column[0]
            column_type = column[1]

            DESC_TABLE += f"- {column_name} : {column_type}\n"

    return DESC_TABLE


cnx = createConnection()
desc = createColumnDesc(cnx)

DESCRIPTION = """
Allows you to perform SQL queries on the table and returns results in various formats. Beware that this tool's output is a string representation of the execution output.
It can use the following tables:
"""
DESCRIPTION += desc



@tool
def sql_engine(query: str) -> str:
    """
    Performs SQL queries and returns results as a minimal string for LLM processing.

    Args:
        query: The SQL query to execute. This should be valid SQL.

    Returns:
        str: Query results in a concise, consistent, and minimal format.
    """
    cursor = cnx.cursor(dictionary=True)  # Enable dictionary cursor
    cursor.execute(query)

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    # Fetch all rows
    rows = cursor.fetchall()

    # Return results in a flat format
    if not rows:
        return "No results found"

    result = []
    result.append("|".join(columns))  # Column headers
    for row in rows:
        result.append("|".join(str(row[col]) for col in columns))

    return "\n".join(result)



sql_engine.description = DESCRIPTION
token = os.getenv('HUGGINGFACE_TOKEN') 

agent = CodeAgent(
    tools=[sql_engine],
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct",token=token),
    additional_authorized_imports=["matplotlib.pyplot"]
)




