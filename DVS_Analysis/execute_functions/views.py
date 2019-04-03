import json

from django.http import HttpResponse
from django.shortcuts import render
import nbimporter
from notebooks import DVS_ANALYSIS_FUNCTIONAL, wind_rose
from plotly.offline.offline import _plot_html


def execute(request):
    if request.method == 'POST':
        plot_kind = request.POST.get('plot_kind')
        if plot_kind:
            bar_box = DVS_ANALYSIS_FUNCTIONAL.bar_box(plot_kind)
        else:
            bar_box = DVS_ANALYSIS_FUNCTIONAL.bar_box()

        scatter_plot_limit = request.POST.get('scatter_plot_limit')
        bubble_size = request.POST.get('bubble_size')
        if scatter_plot_limit and bubble_size:
            scatter = DVS_ANALYSIS_FUNCTIONAL.drawScatter(int(scatter_plot_limit), float(bubble_size))
        elif scatter_plot_limit:
            scatter = DVS_ANALYSIS_FUNCTIONAL.drawScatter(SCATTER_PLOT_LIMIT=int(scatter_plot_limit))
        elif bubble_size:
            scatter = DVS_ANALYSIS_FUNCTIONAL.drawScatter(BUBBLE_SIZE=float(bubble_size))
        else:
            scatter = DVS_ANALYSIS_FUNCTIONAL.drawScatter()

        rand_state = request.POST.get('rand_state')
        if rand_state:
            cube = DVS_ANALYSIS_FUNCTIONAL.cube_helix(int(rand_state))
        else:
            cube = DVS_ANALYSIS_FUNCTIONAL.cube_helix()
        context = {
            'bar_box': bar_box[2:-1],
            'scatter': scatter[2:-1],
            'cube': cube[2:-1]
        }
        return render(request, 'execute_functions/home.html', context)
    else:
        bar_box = DVS_ANALYSIS_FUNCTIONAL.bar_box()
        scatter = DVS_ANALYSIS_FUNCTIONAL.drawScatter()
        cube = DVS_ANALYSIS_FUNCTIONAL.cube_helix()
        context = {
            'bar_box': bar_box[2:-1],
            'scatter': scatter[2:-1],
            'cube': cube[2:-1]
        }
        return render(request, 'execute_functions/home.html', context)


def draw(request):
    interactive = wind_rose.draw_interactive()
    plot_html, plotdivid, width, height = _plot_html(
        interactive, None, True, '100%', 525, True, True)
    response_data = {}
    response_data['result'] = 'success'
    response_data['graph'] = plot_html
    # response_data = json.dumps(response_data)
    # print(json.loads(response_data))
    return HttpResponse(json.dumps(response_data), content_type='application/json')