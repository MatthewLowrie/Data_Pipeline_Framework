from factory import StepFactory
from loaders import JSONLoader
from observers import ConsoleObserver, TimingObserver
from pipeline import Pipeline
from sources import CSVSource
from transforms import FilterNulls, RenameColumns, TypeCast


def main() -> None:
    # Create observers
    console_observer = ConsoleObserver()
    timing_observer = TimingObserver()

    # Build pipeline using direct composition and method chaining
    pipeline = (
        Pipeline("sales_etl")
        .set_source(CSVSource(name="sales_csv", filepath="data/sales.csv"))
        .add_transform(FilterNulls(name="remove_empty", fields=["amount", "product"]))
        .add_transform(TypeCast(name="cast_types", schema={"amount": float, "quantity": int}))
        .add_transform(RenameColumns(name="standardize", mapping={"product": "product_name"}))
        .set_loader(JSONLoader(name="json_output", filepath="output/sales_clean.json"))
        .add_observer(console_observer)
        .add_observer(timing_observer)
    )
    # Run the pipeline
    result = pipeline.run()

    # Print results
    print()
    print(pipeline.get_log().summary())
    print(f"\nRecords processed: {result.records_in}")
    print(f"Records loaded: {result.records_out}")
    print(f"Drop rate: {result.drop_rate:.1%}")
    print(f"Success: {result.success}")
    print()
    print(timing_observer.summary())
    
        # Demonstrate Factory pattern
    print("\n--- Factory-built Pipeline ---\n")

    factory_pipeline = Pipeline("factory_demo")

    source = StepFactory.create_source({
        "type": "json",
        "name": "events_json",
        "filepath": "data/events.json"
    })

    transform = StepFactory.create_transform({
        "type": "filter_nulls",
        "name": "clean_events",
        "fields": ["event_type", "timestamp"]
    })

    loader = StepFactory.create_loader({
        "type": "csv",
        "name": "csv_output",
        "filepath": "output/events_clean.csv"
    })
    
    factory_pipeline.set_source(source)
    factory_pipeline.add_transform(transform)
    factory_pipeline.set_loader(loader)
    factory_pipeline.add_observer(ConsoleObserver())

    result = factory_pipeline.run()
    print()
    print(factory_pipeline.get_log().summary())


if __name__ == "__main__":
    main()