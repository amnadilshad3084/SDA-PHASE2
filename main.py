"""
main module connects all components together
"""
import json
from plugins.inputs import JSONReader, CSVReader, ExcelReader
from plugins.outputs import ConsoleWriter
from core.engine import TransformationEngine


def load_config(filepath: str = 'config.json') -> dict:
    """load configuration from json file"""
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        print("configuration loaded successfully")
        return config
    except FileNotFoundError:
        print(f"error config file not found {filepath}")
        return {}
    except json.JSONDecodeError:
        print("error invalid json format in config file")
        return {}


def create_input_reader(config: dict):
    """create the right type of data reader based on what config says"""
    
    # get data source info from config
    data_source = config.get('data_source', {})
    source_type = data_source.get('type', 'json')
    filepath = data_source.get('filepath', 'data/gdp_with_continent_filled.json')
    
    print(f"\ncreating input reader")
    print(f"type {source_type}")
    print(f"file {filepath}")
    
    # now we create the reader based on file type
    # this is the factory pattern it decides which reader to make
    if source_type == 'json':
        return JSONReader(filepath)
    elif source_type == 'csv':
        return CSVReader(filepath)
    elif source_type == 'excel':
        return ExcelReader(filepath)
    else:
        # if we dont recognize the type just use json as default
        print(f"unknown input type {source_type} using json reader")
        return JSONReader(filepath)


def create_output_writer(config: dict):
    """create the output writer this will display results"""
    
    output_config = config.get('output', {})
    output_type = output_config.get('type', 'console')
    
    print(f"\ncreating output writer")
    print(f"type {output_type}")
    
   
    if output_type == 'console':
        return ConsoleWriter()
    elif output_type == 'graphics':
        print("graphics writer not yet implemented using console for now")
        return ConsoleWriter()
    else:
        print(f"unknown output type {output_type} using console")
        return ConsoleWriter()


def bootstrap():
    """
    this is the main function that connects everything
    it follows dependency injection pattern
    """
    
    print("="*60)
    print("gdp analysis system phase 2")
    print("="*60)
    
    # first we load the config file to see what user wants
    print("\nloading configuration")
    config = load_config()
    
    if not config:
        print("error cannot start without configuration")
        return
    
    # now we create the output writer first
    # we need this before creating the engine
    print("\ncreating output writer")
    output_writer = create_output_writer(config)
    
    # here we create the core engine and inject the output into it
    # this is dependency injection the engine doesnt know what type of output it is
    # it just knows it can call write method on it
    print("\ncreating transformation engine")
    engine = TransformationEngine(output_writer, config)
    
    # now we create the input reader
    print("\ncreating input reader")
    input_reader = create_input_reader(config)
    
    # time to start the data pipeline
    # first read data then process it
    print("\nstarting data pipeline")
    print("="*60)
    
    # read the data from file
    raw_data = input_reader.read()
    
    # check if we actually got data
    if not raw_data:
        print("error no data loaded cannot proceed")
        return
    
    # now we send the data to engine for processing
    # engine will filter it analyze it and send results to output
    engine.execute(raw_data)
    
    # all done
    print("\n" + "="*60)
    print("gdp analysis system completed successfully")
    print("="*60)


def main():
    """entry point when we run this file"""
    
    try:
        # start the whole system
        bootstrap()
        
    except KeyboardInterrupt:
        # if we press ctrl c we stop
        print("\n\nprogram interrupted by user")
        
    except Exception as e:
        #if something goes wrong show error
        print(f"\nerror occurred {e}")
        import traceback
        traceback.print_exc()


# this runs when we execute python main.py
if __name__ == "__main__":
    main()