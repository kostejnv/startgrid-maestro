from o_startlist_creator.logic.event import Event
from o_startlist_creator.logic.validator import CoursesValidator
from o_startlist_creator.logic.solvers.minizinc_solver import Minizinc
import datetime

SOLVER_TIMEOUT = 10

class Solver:
    def __init__(self) -> None:
        pass

    def solve(self, event:Event) -> None:
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