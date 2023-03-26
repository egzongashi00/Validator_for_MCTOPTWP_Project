from validator_for_mctoptwp.model.BudgetValidation import BudgetValidation


def sum_of_spendings_in_different_locations(location_ids, input_instance_array, number_of_lines_to_remove=5):
    input_instance_array = input_instance_array[number_of_lines_to_remove:]

    result = 0
    for item in input_instance_array:
        if item[0] in location_ids:
            result += int(item[7])
    return result


def validate_budget(input_instance_array, solution_instance_array):
    spendings = []
    if len(solution_instance_array) == 1:
        spendings.append(sum_of_spendings_in_different_locations(solution_instance_array[0], input_instance_array))
    else:
        for solution_instance_element in solution_instance_array:
            spendings.append(sum_of_spendings_in_different_locations(
                solution_instance_element,
                input_instance_array,
                len(solution_instance_array) + 4
                # Records for files with 1 route, start at 5. [1-5, 2-6, 3-7, 4-8 etc.], that's why I added +4.
            ))
    return BudgetValidation(budget=input_instance_array[0][2], spendings=spendings, sum_of_spendings=sum(spendings),
                            is_validated=int(input_instance_array[0][2]) >= sum(spendings))


class BudgetValidator:
    pass
