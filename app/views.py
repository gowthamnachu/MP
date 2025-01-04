from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
import numpy as np
from django.shortcuts import render
from .linear_solver import solve_linear_program
from io import BytesIO
import base64
import matplotlib.pyplot as plt

def graphical(request):
    if request.method == 'POST':
        # Parse input data
        c = list(map(float, request.POST['c'].split(',')))
        A = [list(map(float, row.split(','))) for row in request.POST['A'].split(';')]
        b = list(map(float, request.POST['b'].split(',')))

        # Solve the linear program
        fig, ax = plt.subplots()
        optimal_point, optimal_value = solve_linear_program(c, A, b, ax=ax)

        # Save the plot as a base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plot_url = f"data:image/png;base64,{base64.b64encode(image_png).decode()}"

        return render(request, 'graphical.html', {
            'optimal_point': optimal_point,
            'optimal_value': optimal_value,
            'plot_url': plot_url,
        })
    return render(request, 'graphical.html')

def intro_video(request):
    return render(request, 'intro_video.html')
def home(request):
    return render(request, 'home.html')
def simplex(request):
    return render(request, 'simplex.html')
 