from django.http import HttpResponse
from django.template import loader
from ortools.linear_solver import pywraplp


def index(request):
    # Create the solver and the Decision variables
    solver = pywraplp.Solver('RouteOptimization', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    y = {}
    M = 4
    N = 4
    S = {20.0, 30.0, 10.0, 40.0}
    # max_service_time = 2

    # Iterate over the routes and locations
    # for d in range(M):
    #     for i in range(N):
    #         for j in range(N):
    #             # Create x_ijd variable
    #             x[i, j, d] = solver.IntVar(0, 1, f'x_{i}_{j}_{d}')
    #
    #         # Create y_id variable
    #         y[i, d] = solver.IntVar(0, 1, f'y_{i}_{d}')
    #
    #         # Create s_id variable
    #         S[i, d] = solver.IntVar(0, max_service_time, f's_{i}_{d}')

    # CONSTRAINS
    # Constraints 2 guarantee that M routes start from location 1 and end at location N.
    for d in range(M):
        for j in range(1, N):
            solver.Add()

    # OBJECTIVE FUNCTION
    obj = solver.Objective()
    for d in range(M):
        for i in range(1, N - 1):
            obj.SetCoefficient(S[i] * y[(i, d)])
    obj.SetMaximization()

    # Set the objective function
    solver.Solve()

    template = loader.get_template('index.html')
    return HttpResponse(template.render())
