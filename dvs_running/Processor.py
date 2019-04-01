import pickle

import nbformat
from nbparameterise import (
    extract_parameters, replace_definitions, parameter_values
)
from nbconvert.preprocessors import ExecutePreprocessor
import time

# To record time
start_time = time.time()

# As we are making changes directly to source file, pass it's path only
SOURCE_IPYNB_FILE = "DVS_ANALYSIS_PROCEDURAL.ipynb"
TARGET_IPYNB_FILE = "COPIED_ANALYSIS.ipynb"


with open(SOURCE_IPYNB_FILE) as f:
    nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

orig_parameters = extract_parameters(nb)

# Parameters to be passed
param_dictionary = {'PLOT_HIST_SIZE': 30,
                    'PLOT_KIND': 'bar',
                    'SCATTER_PLOT_LIMIT': 50,
                    'BUBBLE_SIZE': 300.0,
                    'RANK': 30}

params = parameter_values(orig_parameters, **param_dictionary)

new_nb = replace_definitions(nb, params, execute=True)
print(new_nb.cells[4].outputs)
# ep = ExecutePreprocessor(timeout=2000, kernel_name='python3')
# ep.preprocess(new_nb, resources={'metadata': {'path': ''}})

with open(TARGET_IPYNB_FILE, 'wt') as f:
    nbformat.write(new_nb, f)

# with open(TARGET_IPYNB_FILE) as f:
#     nb = nbformat.read(f, as_version=4)
#     print(nb.cells[3].outputs[0].data['text/plain'])
#     figure = nb.cells[3].outputs[0].data['text/plain']
#     print(type(figure))

print("\n--- %s seconds ---" % (time.time() - start_time))
