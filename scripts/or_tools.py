import sys

from ortools.linear_solver import pywraplp
from ortools.model_builder.python import pywrap_model_builder_helper
from ortools.linear_solver import linear_solver_pb2

lp_file = sys.argv[1]
print('{name}: {value}'.format(value=lp_file, name='lp_file'))
solver_name = sys.argv[2]
print('{name}: {value}'.format(value=solver_name, name='solver_name'))

if len(sys.argv) == 4:
    solver_params = sys.argv[3]
    print('{name}: {value}'.format(value=solver_params, name='solver_params'))
else:
    solver_params = None

solver = pywraplp.Solver.CreateSolver(solver_name)
solver.EnableOutput()
solver.SetNumThreads(8)
if solver_params:
    param_set = solver.SetSolverSpecificParametersAsString(solver_params)
    if not param_set:
        raise f'Failed setting parameter "{solver_params}"'

print("Loading model...")
with open(lp_file) as f:
    lp_string = f.read()

model_string = pywrap_model_builder_helper.ImportFromLpString(lp_string)
model = linear_solver_pb2.MPModelProto.FromString(model_string)

solver.LoadModelFromProto(model)

print("Model loaded")
print("Solving model...")
solution = solver.Solve()

print(f"Solver completed with exit code: {solution}")
