"""Interactive CLI for MatdarMitra records."""
from app.records import load_records, search, count_by, get_by_id

def show(record):
    print("\n" + "-" * 70)
    print(f"{record.get('id')} | {record.get('record_type')} | {record.get('category')}")
    if record.get("form_number"):
        print("Form:", record["form_number"])
    if record.get("question"):
        print("Question:", record["question"])
        print("Answer:", record["answer"])
    else:
        print("Purpose:", record.get("purpose"))
        print("Who should fill:", record.get("who_should_fill"))
        print("Documents:", record.get("documents_needed"))
        print("Submit to:", record.get("submit_to"))
    print("Source:", record.get("source_url"))

def main():
    records = load_records()
    print(f"MatdarMitra loaded {len(records)} records ({count_by(records, 'record_type')}).")
    while True:
        print("\n1. Print all records\n2. Search by keyword\n3. Count by category\n4. Get record by ID\n0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            for record in records: show(record)
        elif choice == "2":
            matches = search(records, input("Keyword: "))
            print(f"Found {len(matches)} record(s).")
            for record in matches: show(record)
        elif choice == "3":
            for category, total in count_by(records).items(): print(f"{category}: {total}")
            print("Total:", len(records))
        elif choice == "4":
            record = get_by_id(records, input("Record ID (e.g. FORM-6): "))
            show(record) if record else print("Record not found.")
        elif choice == "0":
            print("Goodbye from MatdarMitra!")
            break
        else:
            print("Invalid option. Choose 0-4.")

if __name__ == "__main__":
    main()
