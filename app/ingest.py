import json
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def flatten_company(company):
    flat = {
        "company_name": company["company_name"],
        "company_number": company["company_number"],
        "company_status": company["company_status"],
        "type": company["type"],
        "jurisdiction": company["jurisdiction"],
        "date_of_creation": company["date_of_creation"],
        "sic_codes": ", ".join(company["sic_codes"]),
        "has_charges": company["has_charges"],
        "has_insolvency_history": company["has_insolvency_history"],
        "confirmation_overdue": company["confirmation_statement"]["overdue"],
        "last_accounts_date": company["accounts"]["last_accounts"]["made_up_to"],
        "officer_count": company["officer_summary"]["active_count"]
    }
    return flat

def load_and_insert():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    with open("data/mock_companies_data.json") as f:
        companies = json.load(f)
        for company in companies:
            flat = flatten_company(company)
            collection.update_one(
                {"company_number": flat["company_number"]},
                {"$set": flat},
                upsert=True
            )


if __name__ == "__main__":
    load_and_insert()
    print("Data ingestion completed.")
