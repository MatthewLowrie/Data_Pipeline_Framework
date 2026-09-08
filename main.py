from loaders import JSONLoader
from sources import CSVSource, JSONSource


def main() -> None:
    csv_source = CSVSource(name="sales_csv", filepath="data/sales.csv")
    csv_records = csv_source.extract()
    print(f"CSV extracted: {len(csv_records)} records")

    json_source = JSONSource(name="events_json", filepath="data/events.json")
    json_records = json_source.extract()
    print(f"JSON extracted: {len(json_records)} records")

    loader = JSONLoader(name="json_output", filepath="output/sales_clean.json")
    loaded = loader.load(csv_records)
    print(f"Loaded: {loaded} records")


if __name__ == "__main__":
    main()