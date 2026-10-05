from loaders import JSONLoader
from sources import CSVSource
from transforms import FilterNulls, RenameColumns, TypeCast


def main() -> None:
    # Extract records from CSV
    source = CSVSource(name="sales_csv", filepath="data/sales.csv")
    records = source.extract()
    print(f"Extracted: {len(records)} records")

    # Apply transforms in sequence
    filter_transform = FilterNulls(name="remove_empty", fields=["amount", "product"])
    records = filter_transform.apply(records)
    print(f"After FilterNulls: {len(records)} records")

    cast_transform = TypeCast(name="cast_types", schema={"amount": float, "quantity": int})
    records = cast_transform.apply(records)
    print(f"After TypeCast: {len(records)} records")

    rename_transform = RenameColumns(name="standardize", mapping={"product": "product_name"})
    records = rename_transform.apply(records)
    print(f"After RenameColumns: {len(records)} records")

    # Load clean records to JSON
    loader = JSONLoader(name="json_output", filepath="output/sales_clean.json")
    loaded = loader.load(records)
    print(f"Loaded: {loaded} records")


if __name__ == "__main__":
    main()