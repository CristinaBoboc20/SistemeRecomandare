import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import *
from dotenv import load_dotenv


load_dotenv()

database = os.getenv("database")
token = os.getenv("token")

client = RecombeeClient(database, token)

df = pd.read_csv("books.csv")


properties = {
    "author": "string",
    "title": "string",
    "category": "string",
    "read_status": "string",
    "read_more_by_author": "string",
    "i_am_in_it": "string",
    "collectible": "string",
    "comment": "string"
}


for property_name, property_type in properties.items():
    client.send(AddItemProperty(property_name, property_type))


for row_index, book_row in df.iterrows():
    item_id = f"book_{row_index}"
    client.send(SetItemValues(
        item_id,
        {
            "author": str(book_row.get("Author", "")),
            "title": str(book_row.get("Title", "")),
            "category": str(book_row.get("Category", "")),
            "read_status": str(book_row.get("Read? (y=yes, n=not going to, g=gave up)", "")),
            "read_more_by_author": str(book_row.get("Read more by author?", "")),
            "i_am_in_it": str(book_row.get("I'm in it", "")),
            "collectible": str(book_row.get("Signed or Collectible", "")),
            "comment": str(book_row.get("Comment", "")),
        },
        cascade_create=True
    ))
