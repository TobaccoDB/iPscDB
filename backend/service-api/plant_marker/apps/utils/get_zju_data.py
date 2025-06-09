import importlib.util


def get_api_data(script_path, dataset, queryFile):
    spec = importlib.util.spec_from_file_location("module_name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.get_api_data(dataset, queryFile)
    return result


def format_cell_type(cell_type):
    s = str(cell_type).split('(')
    return s[0]
