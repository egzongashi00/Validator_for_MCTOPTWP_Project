from validator_for_mctoptwp.model.PatternSequenceValidation import PatternSequence
from validator_for_mctoptwp.processor import Processor


def check_pattern_sequence(pattern_sequence, sequence, input_instance_array):  # pattern sequence: 9 3 4, sequence: 0 5 6 8 9 3 0
    sequence_without_zeros = sequence[1:-1]  # We remove 0 in start and end of the array, as we don't need them, sequence: 5 6 8 9 3

    count = 1
    for element in sequence_without_zeros:
        location = Processor.find_location_by_id(input_instance_array, element)[-10:]  # Here we get [0 1 0 0 0 0 0 0 1 0]

        if int(location[int(pattern_sequence[0]) - 1]) == 1:  # Check if e9 is set 1 in the element [0 1 0 0 0 0 0 0 1 0]
            pattern_sequence = pattern_sequence[1:]  # And we remove the 9 from the pattern sequence. Pattern sequence: 3 4

            if len(pattern_sequence) == 0:  # If pattern sequence has been left with zero elements, then this constrain passed.
                return False
        count = count + 1  # If not, check other values in sequence if they will do the job.

    return PatternSequence(sequence_of_trip='→'.join(sequence), is_validated=False)


def pattern_sequence_validation(input_instance_array, solution_instance_array):
    input_instance_array_only_arrays_with_locations = input_instance_array[len(solution_instance_array) + 3:]

    validated_pattern_sequence = []
    count = 0
    for solution_instance_element in solution_instance_array:
        validated_pattern_sequence.append(
            check_pattern_sequence(input_instance_array[count + 3:][0], solution_instance_element, input_instance_array_only_arrays_with_locations)
        )
        count = count + 1
    return validated_pattern_sequence


class PatternSequenceValidator:
    pass
