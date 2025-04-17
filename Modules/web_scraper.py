'''
This module is responsible for scraping data from the web.
It uses the BeautifulSoup library to parse HTML content and extract relevant information.
It also handles the storage of scraped data in a structured format.
'''
# Import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_eredevisie_results(url: str,
                            form_data: dict) -> pd.DataFrame:
    """
    Function to extract the results of the Eredivisie from the website and parse these into a DataFrame.

    Parameters:
        - url (str): The URL of the website to scrape.
        - form_data (dict): The form data to be sent in the POST request.

    Returns:
        - pd.DataFrame: DataFrame containing the results of the Eredivisie.
    """
    # Get the table from the website
    response = requests.post(url, data=form_data)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_tables = soup.find_all('table')
    target_table = all_tables[4]    # The table with the results is the 5th table on the page

    # Extract the data from the table
    headers = []
    data = []

    # Extract the headers
    for head in target_table.find_all('tr')[0].find_all('th'):
        headers.append(head.text.strip())

    # Extract the data
    for row in target_table.find_all('tr')[1:]:
        # Get all columns in the row
        cols = row.find_all('td')
        # Extract data from each column
        row_data = [col.text.strip() for col in cols]
        # Append the row data to the main data list
        data.append(row_data)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=headers)

    return df