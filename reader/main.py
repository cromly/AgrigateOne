import os
import psycopg2
from bs4 import BeautifulSoup


def get_bike_id(url):
    # Extract bike ID from the URL
    return url.split('/')[-2] if url else None


def extract_bike_data(html_file):
    # Initialize variables
    bike_id = None
    bike_url = None

    # Parse the HTML file using BeautifulSoup
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find the 'marketplace-item-single-list' tag
    marketplace_item_tag = soup.find('marketplace-item-single-list')
    if marketplace_item_tag:
        # Extract the value of the ':marketplace-item-url' attribute
        bike_url_attr = marketplace_item_tag.get(':marketplace-item-url')
        if bike_url_attr:
            # Extract bike URL from the attribute value
            bike_url = bike_url_attr.strip("'")
            # Extract bike ID from the URL
            bike_id = get_bike_id(bike_url)

    return bike_id, bike_url


def insert_bike_data(directory, conn):
    print("Inserting bike data into the 'webbikes' table...")
    try:
        # Create a cursor object
        cur = conn.cursor()

        # Step 1: Purge tables 'webpages' and 'webbikes'
        print("Purging tables 'webpages' and 'webbikes'...")
        cur.execute("TRUNCATE TABLE webpages;")
        cur.execute("TRUNCATE TABLE webbikes;")
        conn.commit()
        print("Tables purged successfully.")

        # Step 2: Insert data into 'webpages' table
        print("Inserting data into 'webpages' table...")
        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                cur.execute("INSERT INTO webpages (page_url) VALUES (%s);", (filename,))
        conn.commit()
        print("Data inserted into 'webpages' table successfully.")

        # Step 3: Insert data into 'webbikes' table
        print("Inserting data into 'webbikes' table...")
        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                bike_id, bike_url = extract_bike_data(os.path.join(directory, filename))
                if bike_id and bike_url:
                    cur.execute("SELECT page_id FROM webpages WHERE page_url = %s;", (filename,))
                    page_id = cur.fetchone()[0]
                    cur.execute("INSERT INTO webbikes (bike_id, page_id, bike_url) VALUES (%s, %s, %s);",
                                (bike_id, page_id, bike_url))
        conn.commit()
        print("Data inserted into 'webbikes' table successfully.")

    except (psycopg2.Error, FileNotFoundError) as e:
        conn.rollback()  # Roll back changes if an error occurs
        print("Error inserting bike data:", e)

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        print("Connection closed.")


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

        # Call function to insert bike data into the 'webbikes' table
        insert_bike_data(directory, conn)

        # Close the connection
        conn.close()
        print("Connection closed.")

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
