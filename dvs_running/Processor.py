import nbformat
from nbparameterise import (
    extract_parameters, replace_definitions, parameter_values
)
from nbconvert.preprocessors import ExecutePreprocessor
import time

start_time = time.time()

SOURCE_IPYNB_FILE = "DVS_ANALYSIS.ipynb"

with open(SOURCE_IPYNB_FILE) as f:
    nb = nbformat.read(f, as_version=4)

orig_parameters = extract_parameters(nb)

param_dictionary = {'PLOT_HIST_SIZE': 30,
                    'PLOT_KIND': 'box',
                    'SCATTER_PLOT_LIMIT': 50,
                    'BUBBLE_SIZE': 300.0,
                    'RANK': 30}

params = parameter_values(orig_parameters, **param_dictionary)

new_nb = replace_definitions(nb, params, execute=False)

ep = ExecutePreprocessor(timeout=2000, kernel_name='python3')
ep.preprocess(new_nb, resources={'metadata': {'path': ''}})

with open(SOURCE_IPYNB_FILE, 'wt') as f:
    nbformat.write(new_nb, f)

print("\n--- %s seconds ---" % (time.time() - start_time))
