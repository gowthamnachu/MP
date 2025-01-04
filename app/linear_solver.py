import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

def plot_constraints(constraints, bounds, feasible_region=None, optimal_vertex=None, ax=None):
    """Plots the constraints, feasible region, and optimal solution on the provided axis."""
    x = np.linspace(bounds[0], bounds[1], 400)
    if ax is None:
        ax = plt.gca()

    # Plot constraints as lines
    for coeff, b in constraints:
        if coeff[1] != 0:  # Plot lines with a slope
            y = (b - coeff[0] * x) / coeff[1]
            ax.plot(x, y, label=f"{coeff[0]}x1 + {coeff[1]}x2 ≤ {b}")
        else:  # Vertical line
            x_val = b / coeff[0]
            ax.axvline(x_val, color='r', linestyle='--', label=f"x1 = {x_val}")

    # Highlight feasible region
    if feasible_region is not None and len(feasible_region) > 0:
        hull = ConvexHull(feasible_region)
        polygon = Polygon(feasible_region[hull.vertices], closed=True, color='lightgreen', alpha=0.5, label='Feasible Region')
        ax.add_patch(polygon)

    # Highlight corner points
    if feasible_region is not None:
        for point in feasible_region:
            ax.plot(point[0], point[1], 'bo')  # Mark corners

    # Highlight the optimal solution
    if optimal_vertex is not None:
        ax.plot(optimal_vertex[0], optimal_vertex[1], 'ro', label='Optimal Solution')

    ax.set_xlim(bounds)
    ax.set_ylim(bounds)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title("Linear Programming: Graphical Method")
    ax.legend()
    ax.grid()

def solve_linear_program(c, A, b, ax=None):
    """Solve the linear programming problem and plot on the provided axis."""
    bounds = [0, max(b)]  # Define a reasonable range for visualization
    constraints = list(zip(A, b))

    # Solve using vertices of the feasible region
    vertices = []
    num_constraints = len(A)
    for i in range(num_constraints):
        for j in range(i + 1, num_constraints):
            # Find intersection of two lines
            A_ = np.array([A[i], A[j]])
            b_ = np.array([b[i], b[j]])
            try:
                vertex = np.linalg.solve(A_, b_)
                if all(np.dot(A, vertex) <= b) and all(vertex >= 0):  # Ensure non-negativity and feasibility
                    vertices.append(vertex)
            except np.linalg.LinAlgError:
                continue

    # Filter unique vertices
    feasible_vertices = np.unique(vertices, axis=0)

    # Evaluate the objective function at each vertex
    if len(feasible_vertices) > 0:
        z_values = [np.dot(c, v) for v in feasible_vertices]
        optimal_value = max(z_values)
        optimal_vertex = feasible_vertices[np.argmax(z_values)]

        # Plot the constraints and feasible region
        if ax:
            plot_constraints(constraints, bounds, feasible_region=feasible_vertices, optimal_vertex=optimal_vertex, ax=ax)

        return optimal_vertex, optimal_value
    else:
        return None, None
