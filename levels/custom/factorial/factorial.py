from pyjop import *

SimEnv.connect() and SimEnvManager.first().reset(stop_code=False)

e = DataExchange.first()

n = e.get_data("target_fact")

def factorial(n):
    if n == 0 or n == 1: 
        return 1
    return n * factorial(n - 1)

e.set_data("result", factorial(n))
