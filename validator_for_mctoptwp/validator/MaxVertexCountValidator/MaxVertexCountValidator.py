from validator_for_mctoptwp.model.MaxVertexCountValidation import MaxVertexCountValidation
from validator_for_mctoptwp.processor import Processor


def validate_max_allowed_number_of_vertices(input_instance_array, sums_of_vertices):
    for i in range(len(sums_of_vertices)):
        if int(sums_of_vertices[i]) > int(Processor.find_max_allowed_vertices_for_type_z(input_instance_array)[i]):
            return MaxVertexCountValidation(sums_of_vertices=sums_of_vertices,
                                            max_allowed_vertices_for_type_z=Processor.find_max_allowed_vertices_for_type_z(input_instance_array),
                                            is_validated=False)
    return MaxVertexCountValidation(sums_of_vertices=sums_of_vertices,
                                    max_allowed_vertices_for_type_z=Processor.find_max_allowed_vertices_for_type_z(input_instance_array),
                                    is_validated=True)


class MaxVertexCountValidator:
    pass
