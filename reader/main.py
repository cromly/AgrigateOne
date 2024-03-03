import os
import psycopg2


def purge_webpages_table(conn):
    print("Purging the 'webpages' table...")
    try:
        # Create a cursor object
        cur = conn.cursor()

        # Purge (delete all rows) from the 'webpages' table
        cur.execute("DELETE FROM webpages;")

        # Commit the transaction
        conn.commit()

        print("Table purged successfully!")

    except psycopg2.Error as e:
        conn.rollback()  # Roll back changes if an error occurs
        print("Error purging the 'webpages' table:", e)


def insert_html_filenames(directory, conn):
    print("Inserting HTML filenames into the 'webpages' table...")
    try:
        # Create a cursor object
        cur = conn.cursor()

        # Purge the 'webpages' table before inserting new data
        purge_webpages_table(conn)

        # Counter for page_id
        page_id_counter = 1

        # Iterate over HTML files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                # Extract page URL from the filename
                page_url = filename

                # Insert data into the 'webpages' table with the page_id_counter value
                cur.execute("INSERT INTO webpages (page_id, page_url) VALUES (%s, %s);", (page_id_counter, page_url))

                # Increment the page_id_counter
                page_id_counter += 1

        # Commit the transaction
        conn.commit()

        print("HTML filenames inserted successfully!")

    except psycopg2.Error as e:
        conn.rollback()  # Roll back changes if an error occurs
        print("Error inserting HTML filenames:", e)


if __name__ == "__main__":
    # Connection parameters
    dbname = "postgres"
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"
    directory = "../pages"  # Adjusted directory path for reader script

    # Establish a connection to the database
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to the database!")

        # Call function to insert HTML filenames into the 'webpages' table
        insert_html_filenames(directory, conn)

        # Close the connection
        conn.close()
        print("Connection closed.")

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
