from pyjop import *

SimEnv.connect()
SimEnvManager.first().reset(stop_code=False)

e = DataExchange.first()

n = e.get_data("target_fib_idx")

# Initialize variables
a, b = 0, 1

if n <= 0:
    r = 0
elif n == 1:
    r = 1
else:
    for _ in range(n - 1):
        a, b = b, a + b
    r = b

e.set_data("result", str(r))
