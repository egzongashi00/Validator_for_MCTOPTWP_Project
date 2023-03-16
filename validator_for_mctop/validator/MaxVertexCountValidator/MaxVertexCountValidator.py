from validator_for_mctop.model.MaxVertexCountValidation import MaxVertexCountValidation
from validator_for_mctop.processor import Processor


def check_max_allowed_number_of_vertices(input_instance_array, solution_instance_array,
                                         input_instance_array_only_arrays_with_locations):
    vertices_of_locations = []
    for solution_instance_element in solution_instance_array:
        if solution_instance_element == '0':
            continue
        vertices_of_locations.append(
            Processor.find_location_by_id(input_instance_array_only_arrays_with_locations, solution_instance_element)[-10:])

    sums_of_vertices = Processor.find_sums_of_vertices(vertices_of_locations)

    for i in range(len(sums_of_vertices)):
        if sums_of_vertices[i] > int(Processor.find_max_allowed_vertices_for_type_z(input_instance_array)[i]):
            return MaxVertexCountValidation(sums_of_vertices=sums_of_vertices,
                                            max_allowed_vertices_for_type_z=Processor.find_max_allowed_vertices_for_type_z(
                                                 input_instance_array), is_validated=False,
                                            sequence_of_trip='→'.join(solution_instance_array))
    return False


def max_allowed_number_of_vertices_validation(input_instance_array, solution_instance_array):
    input_instance_array_only_arrays_with_locations = input_instance_array[len(solution_instance_array) + 3:]

    validated_max_allowed_number_of_vertices = []
    if len(solution_instance_array) == 1:
        validated_max_allowed_number_of_vertices.append(
            check_max_allowed_number_of_vertices(input_instance_array, solution_instance_array[0],
                                                 input_instance_array_only_arrays_with_locations)
        )
    else:
        for solution_instance_element in solution_instance_array:
            validated_max_allowed_number_of_vertices.append(
                check_max_allowed_number_of_vertices(input_instance_array, solution_instance_element,
                                                     input_instance_array_only_arrays_with_locations)
            )
    return validated_max_allowed_number_of_vertices


class MaxVertexCountValidator:
    pass
