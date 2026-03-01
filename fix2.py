f = open('main.py').read()
f = f.replace('from plugins.outputs import ConsoleWriter', 'from plugins.outputs import ConsoleWriter, GraphicsChartWriter')
old = "    elif output_type == 'graphics':\n        print(\"graphics writer not yet implemented using console for now\")\n        return ConsoleWriter()"
new = "    elif output_type == 'graphics':\n        output_dir = config.get('output', {}).get('output_dir', 'output')\n        return GraphicsChartWriter(output_dir)"
f = f.replace(old, new)
open('main.py', 'w').write(f)
print('done')
