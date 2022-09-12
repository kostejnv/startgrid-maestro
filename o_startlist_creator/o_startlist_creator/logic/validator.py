from collections import Counter


class Validator:
    def __init__(self, event, schedule_length):
        self.schedule_length = schedule_length
        self.event = event
        self.schedule = None

    def validate_schedule(self):
        was_event_valid = self.__validate_event()
        if was_event_valid: self.schedule = self.__create_schedule(self.event)
        self.__print_schedule(self.schedule)
        if (
                was_event_valid and
                self.__validate_length() and
                self.__validate_same_courses() and
                self.__validate_first_control() and
                self.__validate_capacity() and
                self.__validate_far_and_near_cat()

        ):
            return True
        else:
            return False

    def __validate_capacity(self):
        if any(map(lambda x: len(x) > self.event.capacity, self.schedule)):
            print(f'SOLVER ERROR! Capacity constraint was not satisfied')
            return False
        return True

    def __validate_first_control(self):
        first_control_schedule = [list(map(lambda cat: self.event.categories[cat].first_control, minute)) for minute in
                                  self.schedule]
        failing_minutes = 0
        for minute, controls_in_minute in enumerate(first_control_schedule):
            if len(controls_in_minute) == 0: continue
            most_common_control, number_of_occurences = Counter(controls_in_minute).most_common(1)[0]
            if number_of_occurences > 1:
                print(f'SOLVER ERROR! In the time {minute} there are more runners with control {most_common_control}')
                # return False
                failing_minutes += 1
        #print(f'{failing_minutes} start time failed from {len(first_control_schedule)}')
        if failing_minutes < 1:
            return True
        return False

    def __validate_far_and_near_cat(self):
        return True

    def __create_schedule(self, event):
        categories = event.get_not_empty_categories_with_interval_start().values()
        schedule_length = max([cat.final_start + 1 + (cat.get_category_count() - 1) * cat.final_interval for cat in categories])
        schedule = [[] for _ in range(schedule_length)]
        for cat in categories:
            for i in range(cat.get_category_count()):
                index = cat.final_start + i * cat.final_interval
                schedule[index].append(cat.name)
        return schedule

    def __print_schedule(self, schedule):
        for minute in schedule:
            print('*' * len(minute))

    def __validate_length(self):
        if self.schedule_length != len(self.schedule):
            print(f"WARNING: schedule length ({self.schedule_length}) is different than expected ({len(self.schedule)})")
            return False
        return True

    def __validate_event(self):
        for cat in self.event.get_not_empty_categories_with_interval_start().values():
            if cat.final_start is None or cat.final_interval is None:
                print(f"WARNING: category {cat.name} is not scheduled")
                return False
        return True

    def __validate_same_courses(self):
        cats = self.event.get_not_empty_categories_with_interval_start()
        for cat in cats.values():
            finish_time_cat = cat.final_start + (cat.get_category_count() - 1) * cat.final_interval
            for same_course_cat_name in cat.categories_w_same_course:
                if same_course_cat_name not in cats.keys():
                    continue
                same_course_cat = cats[same_course_cat_name]
                finish_time_same_course_cat = same_course_cat.final_start + (
                            same_course_cat.get_category_count() - 1) * same_course_cat.final_interval

                max_interval = max(same_course_cat.final_interval,cat.final_interval)

                if finish_time_cat < same_course_cat.final_start:
                    if abs(finish_time_cat - same_course_cat.final_start) < max_interval:
                        print(
                            f"WARNING: categories {cat.name} and {same_course_cat.name} have same courses and interval between them is too small")
                        return False
                elif cat.final_start > finish_time_same_course_cat:
                    if abs(cat.final_start - finish_time_same_course_cat) < max_interval:
                        print(
                            f"WARNING: categories {cat.name} and {same_course_cat.name} have same courses and interval between them is too small")
                        return False
                else:
                    print(f"WARNING: categories {cat.name} and {same_course_cat.name} have same courses and overlap each other")
                    return False
        return True
