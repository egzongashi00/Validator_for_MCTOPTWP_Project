from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django_dump_die.middleware import dd
from generate_tourist_routes.Model.BudgetValidation import BudgetValidation
from generate_tourist_routes.Model.LocationVisitedAtMostOnceValidation import LocationVisitedAtMostOnceValidation
import math
from generate_tourist_routes.Model.TimeValidation import TimeValidation


def turn_into_array(text, separator):
    array_list = []
    lines = text.splitlines()
    for line in lines:
        array_list.append(line.split(separator))
    return array_list


def sum_of_spendings_in_different_locations(location_ids, input_instance_array, number_of_lines_to_remove=5):
    input_instance_array = input_instance_array[number_of_lines_to_remove:]

    result = 0
    for arr in input_instance_array:
        if arr[0] in location_ids:
            result += int(arr[7])
    return result


def check_duplicates(arr):
    duplicates = []
    count_dict = {}
    for item in arr:
        if item == '0':
            continue
        if item in count_dict:
            duplicates.append(item)
        else:
            count_dict[item] = 1

    if len(duplicates) != 0:
        return LocationVisitedAtMostOnceValidation(duplicated_locations=duplicates, is_validated=False)
    return LocationVisitedAtMostOnceValidation(is_validated=True)


def to_pairs(arr):
    result = []
    for i in range(len(arr) - 1):
        result.append([arr[i], arr[i + 1]])
    return result


def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_location_by_id(locations, location_id):
    for location in locations:
        if location[0] == location_id:
            return location
    return None


def find_opening_time_of_location(location):
    return int(location[5])


def find_closing_time_of_location(location):
    return int(location[6])


def find_time_spend_at_location(location):
    return float(location[3])


def find_waiting_time_before_opening(arrival_at_location_time, location_opening_time):
    if location_opening_time > arrival_at_location_time:
        return location_opening_time - arrival_at_location_time
    return 0


def check_if_location_is_closed(arrival_at_location_time, location_closing_time):
    if arrival_at_location_time > location_closing_time:
        return True
    return False


def validate_budget(input_instance_array, solution_instance_array):
    spendings = []
    if len(solution_instance_array) == 1:
        spendings.append(sum_of_spendings_in_different_locations(
            solution_instance_array[0],
            input_instance_array
        ))
    else:
        for solution_instance_element in solution_instance_array:
            spendings.append(sum_of_spendings_in_different_locations(
                solution_instance_element,
                input_instance_array,
                len(solution_instance_array) + 4
                # Records for files with 1 route, start at 5. [1-5, 2-6, 3-7, 4-8 etc.], that's why I added +4.
            ))
    return BudgetValidation(budget=input_instance_array[0][2], spendings=spendings, sum_of_spendings=sum(spendings),
                            is_validated=int(input_instance_array[0][2]) > sum(spendings))


def validate_location_visited_at_most_once(solution_instance_array):
    if len(solution_instance_array) == 1:
        return check_duplicates(solution_instance_array[0])
    merged_solution_instance_array = [item for sublist in solution_instance_array for item in sublist]
    return check_duplicates(merged_solution_instance_array)


def validate_time(input_instance_array, solution_instance_array, validation_type):
    input_instance_array = input_instance_array[len(solution_instance_array) + 3:]
    MAX_TIME = int(input_instance_array[0][6])

    time_validation = []
    time = 0
    if len(solution_instance_array) == 1:
        solution_instance_pairs = to_pairs(solution_instance_array[0])
        for solution_instance_pair in solution_instance_pairs:
            first_location = find_location_by_id(input_instance_array, solution_instance_pair[0])
            second_location = find_location_by_id(input_instance_array, solution_instance_pair[1])
            distance = euclidean_distance(float(first_location[1]), float(first_location[2]), float(second_location[1]),
                                          float(second_location[2]))
            waiting_before_opening = find_waiting_time_before_opening(distance + time,
                                                                      find_opening_time_of_location(second_location))
            location_closed = check_if_location_is_closed(distance + time,
                                                          find_closing_time_of_location(second_location))

            time_spend_before_trip = time
            time += distance + waiting_before_opening + find_time_spend_at_location(second_location)

            if (MAX_TIME <= time and validation_type == 'time_validation') or (
                    location_closed and validation_type == 'inside_operating_hours_validation'):
                time_validation.append(
                    TimeValidation(
                        location_one_id=first_location[0],
                        location_two_id=second_location[0],
                        distance_between_locations=distance,
                        opening_time_of_location_one=find_opening_time_of_location(first_location),
                        closing_time_of_location_one=find_closing_time_of_location(first_location),
                        opening_time_of_location_two=find_opening_time_of_location(second_location),
                        closing_time_of_location_two=find_closing_time_of_location(second_location),
                        waiting_before_opening=waiting_before_opening,
                        location_closed=location_closed,
                        time_spend_at_location=find_time_spend_at_location(second_location),
                        time_spend_before_trip=time_spend_before_trip,
                        time_spend_after_trip=time,
                        max_time=MAX_TIME,
                        is_validated=not location_closed and MAX_TIME > time
                    )
                )
                if MAX_TIME <= time and validation_type == 'time_validation':
                    break
        return time_validation


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def validate(request):
    if request.method == 'POST':
        input_instance_file = request.FILES.get('input_instance', False)
        solution_instance_file = request.FILES.get('solution_instance', False)

        input_instance = input_instance_file.read().decode('utf-8')
        solution_instance = solution_instance_file.read().decode('utf-8')

        input_instance_array = turn_into_array(input_instance, ' ')
        solution_instance_array = turn_into_array(solution_instance, ' -> ')

        return render(request, 'index.html', {
            'show_table': True,
            'location_visited_at_most_once_validation': validate_location_visited_at_most_once(solution_instance_array),
            'budget_validation': validate_budget(input_instance_array, solution_instance_array),
            'time_validation': validate_time(input_instance_array, solution_instance_array, 'time_validation'),
            'inside_operating_hours_validation': validate_time(input_instance_array, solution_instance_array,
                                                               'inside_operating_hours_validation'),
        })
