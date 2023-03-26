import math


def turn_into_array(text, separator):
    array_list = []
    lines = text.splitlines()
    for line in lines:
        array_list.append(line.split(separator))
    return array_list


def to_pairs(array):
    result = []
    for i in range(len(array) - 1):
        result.append([array[i], array[i + 1]])
    return result


def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


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


def find_max_allowed_vertices_for_type_z(input_instance_array):
    return input_instance_array[1]


def is_constrain_validated(elements):
    for element in elements:
        if element:
            return False
    return True


class Processor:
    pass
