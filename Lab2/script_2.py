import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import *
from dotenv import load_dotenv


load_dotenv()

database = os.getenv("database")
token = os.getenv("token")

client = RecombeeClient(database, token)

people = pd.read_csv("books.csv")


user_properties = {
    "sales_person": "string",
    "team": "string",
    "location": "string",
    "email": "string"
}

for name, type in user_properties.items():
    client.send(AddUserProperty(name, type))

for _, row in people.iterrows():
    user_id = str(row["SP ID"])
    email = row["Sales person"].replace(" ", ".").lower() + "@gmail.com"

    client.send(SetUserValues(
        user_id,
        {
            "sales_person": str(row["Sales person"]),
            "team": str(row["Team"]),
            "location": str(row["Location"]),
            "email": email
        },
        cascade_create=True
    )) 