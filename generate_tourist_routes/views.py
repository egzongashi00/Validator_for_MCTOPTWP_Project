from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django_dump_die.middleware import dd
from generate_tourist_routes.Model.BudgetValidation import BudgetValidation
from generate_tourist_routes.Model.LocationVisitedAtMostOnceValidation import LocationVisitedAtMostOnceValidation


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


def validate_budget(solution_instance_array, input_instance_array):
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
            'budget_validation': validate_budget(solution_instance_array, input_instance_array),
            'location_visited_at_most_once_validation': validate_location_visited_at_most_once(solution_instance_array)
        })
