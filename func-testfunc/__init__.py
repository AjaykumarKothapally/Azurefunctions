import logging
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import json

# Define the Azure Cosmos DB connection details
COSMOS_DB_ENDPOINT = "https://shopclues-cosmosdb.documents.azure.com:443/"
COSMOS_DB_KEY = "tHd5gEAZOyGtwhygEr2agd0UsR2f0u24cgfWcRO7z2JDwGCy1grSl3AawFyj0cFfIv1DFwRlZiyAACDbBAMy2Q=="
COSMOS_DB_DATABASE_NAME = "ShopCluesDB"
COSMOS_DB_CONTAINER_NAME = "Products"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Initialize Cosmos DB client
        client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
        database = client.get_database_client(COSMOS_DB_DATABASE_NAME)
        container = database.get_container_client(COSMOS_DB_CONTAINER_NAME)

        # Query all items from the Cosmos DB container
        items = list(container.read_all_items())

     # Convert items to JSON
        items_json = json.dumps(items, indent=2)

        return func.HttpResponse(items_json, mimetype="application/json", status_code=200)

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(f"Unexpected error: {str(e)}", status_code=500)