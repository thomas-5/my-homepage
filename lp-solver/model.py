import numpy as np

# Simplex

def mask_to_0(a, tolerance):
  a_mask = np.isclose(a, 0.0, atol=tolerance)
  a = np.where(a_mask, 0.0, a)
  return a

# Transform LP to canonical form for basis B
def transform_canonical(cT, A, b, B, z_hat, tolerance=1e-6, canonical=False):
  if canonical: print("------------- Canonical Form -------------")
  cB = np.transpose(cT)[B]
  if canonical: print(f"c_B = {cB}")
  y = np.linalg.inv(np.transpose(A[:,B])) @ cB
  y = mask_to_0(y, tolerance)
  if canonical: print(f"A_B = \n {A[:,B]}")
  if canonical: print(f"A_B^-T = \n {mask_to_0(np.linalg.inv(np.transpose(A[:,B])),tolerance)}")
  if canonical: print(f"y = A_B^-T · c_B = {y}")
  cT = cT - np.round(y @ A, 10)
  cT = mask_to_0(cT, tolerance)
  if canonical: print(f"new c_T = c_T - y · A = {cT}")
  if canonical: print(f"z_hat = {z_hat}, \n b = {b}, \n y_T = {y}")
  z_hat += y @ b
  if canonical: print(f"new z_hat = z_hat + y_T · b = {z_hat}")
  b = np.round(np.linalg.inv(A[:,B]) @ b, 10)
  A = np.round(np.linalg.inv(A[:,B]) @ A, 10)
  A = mask_to_0(A, tolerance)
  if canonical: print("------------------------------------------")
  return cT, A, b, z_hat

# Find entering element
def find_entering(cT):
  positive_indices = np.where(cT > 0)[0]
  min_i = positive_indices[0]
  return min_i

# Find leaving element
def find_leaving(A, b, B, k, canonical=False):
  ratio = b/A[:,k].reshape(-1,1)
  for i,v in enumerate(A[:,k].reshape(-1,1)):
    if v < 0:
      ratio[i] = -1
  positive_indices = np.where(ratio >= 0)[0]
  t = positive_indices[np.argmin(ratio[positive_indices])]
  for i, v in enumerate(A[t]):
    if v == 1:
      leaving = True
      for j, v2 in enumerate(A[:,i]):
        if (v2 != 0) & (j != t):
          leaving = False
      if i not in B:
        leaving = False
      if leaving:
        return i
  return -1

def phase_two(A, cT, b, B, z_hat = np.array([0.]), tolerance = 1e-6, info = False, canonical = False, max_epoch = 10):
  oA, ocT = A, cT
  cT, A, b, z_hat = transform_canonical(cT, A, b, B, z_hat, tolerance, canonical)
  if info: print(f"Initial basis: B = {sorted([i+1 for i in B])}")
  if info: print(f"Initial objective in canonical form of B:\n{cT}x + {z_hat}")
  if info: print(f"Initial constraint in canonical form of B: \n{A}x, \n =\n{b}")
  epoch = 0
  while not np.all(np.logical_or(cT < 0, np.isclose(cT, 0.0, atol=1e-5))) and epoch < max_epoch:
    epoch += 1
    if info: print(f"---------------------- Epoch {epoch}. ----------------------")
    k = find_entering(cT)
    if info: print(f"Entering element = {k+1}")
    if np.all(A[:,k] <= 0):
      r = list(-A[:,k])
      x_bar = list(b.reshape(1,-1)[0])
      for i in range(len(cT)):
        if i not in B:
          r.insert(i,0)
          x_bar.insert(i,0)
      r[k] = 1
      if info: print("--------------------------- END ------------------------------")
      if info: print(f"This LP is Unbounded.")
      if info: print("Certificate:")
      if info: print(f"r = {r}T")
      if info: print(f"x_bar = {x_bar}T")
      return x_bar
    t = find_leaving(A, b, B, k, canonical)
    if info: print(f"Leaving element = {t+1}")
    B.append(k)
    B.remove(t)
    B.sort()
    if info: print(f"Basis: {[i+1 for i in B]}")
    cT, A, b, z_hat = transform_canonical(cT, A, b, B, z_hat, tolerance, canonical)
    z_hat = mask_to_0(z_hat, tolerance)
    cT = mask_to_0(cT, tolerance)
    b = mask_to_0(b, tolerance)
    if info: print(f"Objective: {cT}x + {z_hat}")
    if info: print(f"Constraint: \n{A}x, \n =\n{b}")

  opt_sol = list(b.reshape(1,-1)[0])
  for i in range(len(cT)):
    if i not in B:
      opt_sol.insert(i,0)
  if epoch != 0:
    if info: print("--------------------------- END ------------------------------")
    if info: print(f"Optimal value: {z_hat[0]}")
    if info: print(f"Optimal solution: x = {opt_sol}T")
    if info: print(f"Certificate of optimality: y = {mask_to_0(np.linalg.inv(np.transpose(oA[:,B])),tolerance)@np.transpose(ocT)[B]}T")
  return opt_sol

def phase_one(A, b, info):
  auxiliary_A = A
  auxiliary_b = b
  for i,v in enumerate(b):
    if v[0] < 0:
      auxiliary_A[i] = -1 * auxiliary_A[i]
      auxiliary_b[i] = -1 * auxiliary_b[i]

  auxiliary_A = np.hstack((A, np.identity(len(A))))
  auxiliary_cT = np.hstack((np.array([0 for _ in range(len(A[0]))]),
                           np.array([-1 for _ in range(len(A))])))
  B = [len(auxiliary_cT) - i for i in range(1, len(A)+1)]
  print("--------------------------- PHASE 1. ------------------------------")
  opt_sol = phase_two(auxiliary_A, auxiliary_cT, b, B, z_hat = np.array([0.]), info=info)
  for i in [len(auxiliary_cT) - i for i in range(1, len(A)+1)]:
    if opt_sol[i] != 0.:
      print("This LP is infeasible")
      print(f"Certificate of infeasibility: {auxiliary_cT[B] @ np.linalg.inv(auxiliary_A[:,B])}T")
      print("--------------------------- END OF PHASE 1. ------------------------------")
      return None
  print(f"This LP is feasible, one feasible solution: {opt_sol}")
  print("--------------------------- END OF PHASE 1. ------------------------------")
  print("--------------------------- PHASE 2. ------------------------------")
  return B

def simplex(A, cT, b, z_hat = np.array([0.]), tolerance=1e-6, info=False, canonical=False, max_epoch=10):
  B = phase_one(A, b, info=info)
  if B is not None:
    phase_two(A, cT, b, B, z_hat=z_hat, tolerance=tolerance, info=True, canonical=canonical, max_epoch=max_epoch)
  return