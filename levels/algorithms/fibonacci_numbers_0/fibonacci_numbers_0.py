from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

e = DataExchange.first()

n = e.get_data("target_fib_idx")

if n <= 1:
    r = n
a, b = 0, 1
for _ in range(2, n + 1):
    a, b = b, a + b
r = b

e.set_data("result", str(r))
