"""
main module - orchestrator / entry point
wires all components together using dependency injection
"""
import json
from plugins.inputs  import JSONReader, CSVReader, ExcelReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter, FileWriter
from core.engine     import TransformationEngine


#  Factory maps 
INPUT_DRIVERS = {
    "json":  JSONReader,
    "csv":   CSVReader,
    "excel": ExcelReader,
}

OUTPUT_DRIVERS = {
    "console":  ConsoleWriter,
    "graphics": GraphicsChartWriter,
    "file":     FileWriter,
}


def load_config(filepath: str = 'config.json') -> dict:
    """load configuration from json file"""
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        print("configuration loaded successfully")
        return config
    except FileNotFoundError:
        print(f"error: config file not found → {filepath}")
        return {}
    except json.JSONDecodeError:
        print("error: invalid json in config file")
        return {}


def create_input_reader(config: dict):
    """factory: create correct input reader from config"""
    data_source = config.get('data_source', {})
    source_type = data_source.get('type', 'json').lower()
    filepath    = data_source.get('filepath', 'data/gdp_with_continent_filled.json')

    print(f"\ncreating input reader → type={source_type}  file={filepath}")

    driver_class = INPUT_DRIVERS.get(source_type)
    if driver_class is None:
        print(f"unknown input type '{source_type}', defaulting to json")
        driver_class = JSONReader

    return driver_class(filepath)


def create_output_writer(config: dict):
    """factory: create correct output writer from config"""
    output_config = config.get('output', {})
    output_type   = output_config.get('type', 'graphics').lower()
    output_dir    = output_config.get('output_dir', 'output')

    print(f"\ncreating output writer → type={output_type}")

    if output_type == 'graphics':
        return GraphicsChartWriter(output_dir)
    elif output_type == 'console':
        return ConsoleWriter()
    elif output_type == 'file':
        return FileWriter(output_dir)
    else:
        print(f"unknown output type '{output_type}', defaulting to graphics")
        return GraphicsChartWriter(output_dir)


def bootstrap():
    """
    main bootstrap function
    1. load config
    2. create output (sink)
    3. inject sink into core engine
    4. create input reader, inject engine
    5. run pipeline
    """
    print("="*60)
    print("  GDP ANALYSIS SYSTEM — PHASE 2")
    print("="*60)

    # 1. load config
    config = load_config()
    if not config:
        print("error: cannot start without configuration")
        return

    # 2. create output writer (the sink)
    output_writer = create_output_writer(config)

    # 3. create core engine -- inject the sink (DIP)
    engine = TransformationEngine(output_writer, config)

    # 4. create input reader --- inject engine as PipelineService
    input_reader = create_input_reader(config)

    # 5. run pipeline
    print("\n" + "="*60)
    print("STARTING DATA PIPELINE")
    print("="*60)

    raw_data = input_reader.read()

    if not raw_data:
        print("error: no data loaded, cannot proceed")
        return

    engine.execute(raw_data)

    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)


def main():
    try:
        bootstrap()
    except KeyboardInterrupt:
        print("\nprogram interrupted by user")
    except Exception as e:
        print(f"\nerror occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()