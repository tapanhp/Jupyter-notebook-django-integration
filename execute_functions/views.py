import json
import os

from django.http import HttpResponse
from django.shortcuts import render
# from notebooks import DVS_ANALYSIS_FUNCTIONAL, wind_rose
from nbimporter import NotebookLoader


def import_nb(notebook):
    global i
    import nbimporter  # This library is the root and most imp part of importing notebook
    nbimporter.options['only_defs'] = True  # This tells notebook to import every cell and not just methods.

    loader = NotebookLoader()
    name = notebook
    i = loader.load_module(os.path.join('notebooks', name))


def execute(request):
    import_nb("DVS_ANALYSIS_FUNCTIONAL")
    if request.method == 'POST':
        plot_kind = request.POST.get('plot_kind')
        bar_box = i.bar_box(plot_kind) if plot_kind else i.bar_box()
        scatter_plot_limit = request.POST.get('scatter_plot_limit')
        bubble_size = request.POST.get('bubble_size')
        if scatter_plot_limit and bubble_size:
            scatter = i.drawScatter(int(scatter_plot_limit), float(bubble_size))
        elif scatter_plot_limit:
            scatter = i.drawScatter(SCATTER_PLOT_LIMIT=int(scatter_plot_limit))
        elif bubble_size:
            scatter = i.drawScatter(BUBBLE_SIZE=float(bubble_size))
        else:
            scatter = i.drawScatter()

        rand_state = request.POST.get('rand_state')
        cube = i.cube_helix(int(rand_state)) if rand_state else i.cube_helix()
    else:
        bar_box = i.bar_box()
        scatter = i.drawScatter()
        cube = i.cube_helix()
    context = {
        'bar_box': bar_box[2:-1],
        'scatter': scatter[2:-1],
        'cube': cube[2:-1]
    }
    return render(request, 'execute_functions/home.html', context)
