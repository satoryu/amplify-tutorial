import os
from amplify import BinaryPoly, BinaryQuadraticModel, gen_symbols, Solver, decode_solution
from amplify.client import FixstarsClient

q = gen_symbols(BinaryPoly, 2)
print(q)

f = 1 - q[0] * q[1]
print(f)

model = BinaryQuadraticModel(f)

client = FixstarsClient()
client.token = os.environ['AMPLIFY_TOKEN']
client.parameters.timeout = 1000 # 1 second

solver = Solver(client)
result = solver.solve(model)
values = result[0].values
print(f"q = {decode_solution(q, values)}")
