import json

import psycopg2

# Database connection parameters
db_params = {
    "dbname": "dataskipper_db",
    "user": "root",
    "password": "password",
    "host": "localhost",
    "port": 5439,
}

# Define the table and the order of columns as per your database schema
table_name = "datalogger_electricaldata"
columns = (
    "client_id",
    "generation_timestamp",
    '"voltage_RMS"',
    '"current_RMS"',
    "phase",
    "voltage_frequency",
    "power",
    "energy",
    "delete_status",
)


def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)


def prepare_data_for_insert(samples):
    """Prepare data for insertion into the database."""
    return [
        (
            sample["client_id"],
            sample["timestamp"],
            sample["voltage_rms"],
            sample["current_rms"],
            sample["phase"],
            sample["voltage_frequency"],
            sample["power"],
            sample["energy"],
            False,
        )
        for sample in samples
    ]


def insert_data_into_db(connection_params, table, columns, data):
    """Insert data into the database using psycopg2."""
    insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        psycopg2.extras.execute_values(
            cursor, insert_query, data, template=None, page_size=100
        )
        conn.commit()
        print("Data inserted successfully")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def load_data():
    json_file_path = "/Users/sanjana/Downloads/iot_1.json"
    json_data = load_json_data(json_file_path)
    prepared_data = prepare_data_for_insert(json_data)
    insert_data_into_db(db_params, table_name, columns, prepared_data)


load_data()
