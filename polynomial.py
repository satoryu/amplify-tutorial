import os
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution
from amplify.client import FixstarsClient

q = gen_symbols(BinaryPoly, 0, (2, 2))

f = (
  -q[0][0] * q[1][1]
  + q[0][0] * q[0][1]
  + q[0][1] * q[1][1]
  + q[0][0] * q[1][0]
  + q[1][0] * q[1][1]
)

client = FixstarsClient()
client.token = os.environ['AMPLIFY_TOKEN']
client.parameters.timeout = 1000

solver = Solver(client)
result = solver.solve(f)
values = result[0].values
d = decode_solution(q, values)

print(d)