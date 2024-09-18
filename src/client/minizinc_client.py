from minizinc import Instance, Model
from minizinc import Solver as MZNSolver
from typing import Any

class MinizincClient:
    def __init__(self, timeout, solver_path: str | None = None):
        self.timeout = timeout
        self.solver = MZNSolver.lookup(solver_path) if solver_path else MZNSolver.lookup("gecode")
        
    def solve(self, definition: str, variables: dict[str, Any]):
        model = Model()
        model.add_string(definition)
        instance = Instance(self.solver, model)
        for key, value in variables.items():
            instance[key] = value
        return instance.solve(timeout=self.timeout)