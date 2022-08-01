from ortools.linear_solver import pywraplp
from ortools.model_builder.python import pywrap_model_builder_helper
from ortools.linear_solver import linear_solver_pb2

with open('../data/zoltan/sample.lp') as f:
    lp_string = f.read()

model_string = pywrap_model_builder_helper.ImportFromLpString(lp_string)
model = linear_solver_pb2.MPModelProto.FromString(model_string)
print('Model:')
print(model)

solver = pywraplp.Solver.CreateSolver('GLOP')
solver.LoadModelFromProto(model)
solution = solver.Solve()

solution_response = linear_solver_pb2.MPSolutionResponse()
solver.FillSolutionResponseProto(solution_response)
print('Solution:')
print(solution_response)
