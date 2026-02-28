from typing import List, Dict, Any

class ConsoleWriter:
    """
    prints results to terminal
    """
    
    def __init__(self):
        print("console writer initialized")
    
    def write(self, data: List[Dict[str, Any]], title: str = "") -> None:
        """
        write data to console
        args:
            data list of result dictionaries
            title title for output
        """
        print("\n" + "="*60)
        if title:
            print(f"{title}")
            print("="*60)
        
        for item in data:
            print("\nresults")
            for key, value in item.items():
                print(f"{key} {value}")
        
        print("="*60)


        # FIZA'S WORK
# add these classes
# 1 graphicschartwriter with methods
#   create_pie_chart
#   create_bar_chart
#   create_line_graph
#   create_scatter_plot
# 2 filewriter for saving to files