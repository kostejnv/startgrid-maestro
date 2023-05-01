from .event import Event
from .validator import CoursesValidator
from .solvers.minizinc_solver import MinizincMain, Minizinc2
import datetime

SOLVER_TIMEOUT = 300

class Solver:
    def __init__(self) -> None:
        pass

    def solve(self, event:Event) -> None:
        solver = MinizincMain(timeout=datetime.timedelta(seconds=SOLVER_TIMEOUT))
        individual_cats, schedule_length = solver.solve(event)
        solver = Minizinc2(timeout=datetime.timedelta(seconds=SOLVER_TIMEOUT))
        individual_cats, schedule_length = solver.solve(event, schedule_length)
        event = self.__merge_solved_cats_to_event(individual_cats, event)
        if not CoursesValidator(event, schedule_length).validate_schedule():
            raise "INTERNAL ERROR: Returned scheduled is not correct"
        event.solved = True
        return event

    def __merge_solved_cats_to_event(self, ind_cats, event):
        for cat in ind_cats.values():
            event.categories[cat.name] = cat
        return event