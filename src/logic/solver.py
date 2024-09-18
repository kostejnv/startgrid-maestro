from src.entities.event import Event
from src.logic.validator import CoursesValidator
from src.logic.solvers.minizinc_solver import Minizinc
import datetime

SOLVER_TIMEOUT = 300

class Solver:
    def __init__(self) -> None:
        pass

    def solve(self, event:Event) -> Event:
        solver = Minizinc(timeout=datetime.timedelta(seconds=SOLVER_TIMEOUT))
        individual_cats, schedule_length = solver.solve(event)
        event = self.__merge_solved_cats_to_event(individual_cats, event)
        if not CoursesValidator(event, schedule_length).validate_schedule():
            raise "INTERNAL ERROR: Returned scheduled is not correct"
        event.solved = True
        return event

    def __merge_solved_cats_to_event(self, ind_cats, event):
        for cat in ind_cats.values():
            event.categories[cat.name] = cat
        return event