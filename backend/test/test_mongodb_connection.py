from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
from urllib.parse import quote_plus
import certifi


username = "pycharmrepo_db_user"
password = "PushpumKris"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

cluster_url = "cluster0.w9peb3y.mongodb.net"

MONGODB_URI = (
    f"mongodb+srv://{encoded_username}:{encoded_password}"
    f"@{cluster_url}/?retryWrites=true&w=majority"
)


def test_connection():
    client = None

    try:
        client = MongoClient(
            MONGODB_URI,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000
        )

        client.admin.command("ping")

        print("MongoDB connected successfully!")

    except ServerSelectionTimeoutError as e:
        print("Server selection timeout.")
        print("Possible reasons:")
        print("1. IP address is not allowed in MongoDB Atlas")
        print("2. Internet/firewall/VPN is blocking MongoDB")
        print("3. Wrong cluster URL")
        print("Reason:", e)

    except OperationFailure as e:
        print("MongoDB authentication failed.")
        print("Check username, password, and database user permissions.")
        print("Reason:", e)

    except ConnectionFailure as e:
        print("MongoDB connection failed.")
        print("Reason:", e)

    except Exception as e:
        print("Something went wrong.")
        print("Reason:", e)

    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")


if __name__ == "__main__":
    test_connection()
