from validator_for_mctoptwp.model.LocationVisitCountsValidation import LocationVisitCountsValidation


def check_duplicates(array):
    duplicates = []
    count_dict = {}
    for item in array:
        if item == '0':
            continue
        if item in count_dict:
            duplicates.append(item)
        else:
            count_dict[item] = 1

    if len(duplicates) != 0:
        return LocationVisitCountsValidation(duplicated_locations=duplicates, is_validated=False)
    return LocationVisitCountsValidation(is_validated=True)


def validate_location_visited_at_most_once(solution_instance_array):
    if len(solution_instance_array) == 1:
        return check_duplicates(solution_instance_array[0])
    merged_solution_instance_array = [item for sublist in solution_instance_array for item in sublist]
    return check_duplicates(merged_solution_instance_array)


class LocationVisitCountsValidator:
    pass
