from validator_for_mctoptwp.model.TimeValidation import TimeValidation
from validator_for_mctoptwp.processor import Processor


def check_time_validation(input_instance_array, solution_instance_array, validation_type):
    MAX_TIME = int(input_instance_array[0][6])
    time = 0
    solution_instance_pairs = Processor.to_pairs(solution_instance_array)
    for solution_instance_pair in solution_instance_pairs:
        first_location = Processor.find_location_by_id(input_instance_array, solution_instance_pair[0])
        second_location = Processor.find_location_by_id(input_instance_array, solution_instance_pair[1])
        distance = Processor.euclidean_distance(float(first_location[1]), float(first_location[2]),
                                                float(second_location[1]),
                                                float(second_location[2]))
        waiting_before_opening = Processor.find_waiting_time_before_opening(distance + time,
                                                                            Processor.find_opening_time_of_location(
                                                                                second_location))
        location_closed = Processor.check_if_location_is_closed(distance + time,
                                                                Processor.find_closing_time_of_location(
                                                                    second_location))

        time_spend_before_trip = time
        time_without_time_spend_at_second_location = time + distance + waiting_before_opening
        time += distance + waiting_before_opening + Processor.find_time_spend_at_location(second_location)

        if (MAX_TIME <= time and validation_type == 'time_validation') or (
                location_closed and validation_type == 'inside_operating_hours_validation'):
            return TimeValidation(
                location_one_id=first_location[0],
                location_two_id=second_location[0],
                distance_between_locations=distance,
                opening_time_of_location_one=Processor.find_opening_time_of_location(first_location),
                closing_time_of_location_one=Processor.find_closing_time_of_location(first_location),
                opening_time_of_location_two=Processor.find_opening_time_of_location(second_location),
                closing_time_of_location_two=Processor.find_closing_time_of_location(second_location),
                waiting_before_opening=waiting_before_opening,
                location_closed=location_closed,
                time_spend_at_location=Processor.find_time_spend_at_location(second_location),
                time_spend_before_trip=time_spend_before_trip,
                time_without_time_spend_at_second_location=time_without_time_spend_at_second_location,
                time_spend_after_trip=time,
                max_time=MAX_TIME,
                is_validated=not location_closed and MAX_TIME > time,
                sequence_of_trip='→'.join(solution_instance_array)
            )
    return False


def validate_time(input_instance_array, solution_instance_array, validation_type):
    input_instance_array = input_instance_array[len(solution_instance_array) + 3:]

    validated_time = []
    for solution_instance_element in solution_instance_array:
        validated_time.append(check_time_validation(input_instance_array, solution_instance_element, validation_type))
    return validated_time


class TimeValidator:
    pass
