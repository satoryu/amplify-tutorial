import numpy as np

def gen_random_tsp(ncity: int):
  # 座標
  locations = np.random.uniform(size=(ncity, 2))

  # 距離行列
  all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
  distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

  return locations, distances


from amplify import (
  BinaryPoly,
  BinaryQuadraticModel,
  sum_poly,
  gen_symbols,
  Solver,
  decode_solution
)

ncity = 32
locations, distances = gen_random_tsp(ncity)
q = gen_symbols(BinaryPoly, ncity, ncity)

cost = sum_poly(
  ncity,
  lambda n: sum_poly(
    ncity,
    lambda i: sum_poly(
        ncity, lambda j: distances[i][j] * q[n][i] * q[(n+1) % ncity][j]
    )
  )
)

from amplify.constraint import equal_to

row_constraints = [
  equal_to(sum_poly([q[n][i] for i in range(ncity)]), 1) for n in range(ncity)
]
col_constraints = [
  equal_to(sum_poly([q[n][i] for n in range(ncity)]), 1) for i in range(ncity)
]

constraints = sum(row_constraints) + sum(col_constraints)
constraints *= np.amax(distances)
model = cost + constraints

from amplify import Solver
from amplify.client import FixstarsClient
import os

client = FixstarsClient()
client.token = os.environ['AMPLIFY_TOKEN']
client.parameters.timeout = 5000

solver = Solver(client)
result = solver.solve(model)
if len(result) == 0:
  raise RuntimeError("Any one of constraints is not satisfied")

energy, values = result[0].energy, result[0].values

q_values = decode_solution(q, values, 1)
print(q_values)
