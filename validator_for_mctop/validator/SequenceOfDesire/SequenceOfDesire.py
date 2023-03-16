from validator_for_mctop.model.SequenceOfDesireValidation import SequenceOfDesire
from validator_for_mctop.processor import Processor


def check_sequence_of_desire(sequence_of_desire, sequence,
                             input_instance_array):  # sequence of desire: 9 3 4, sequence: 0 5 6 8 9 3 0
    sequence_without_zeros = sequence[
                             1:-1]  # We remove 0 in start and end of the array, as we don't need them, sequence: 5 6 8 9 3

    count = 1
    for element in sequence_without_zeros:
        location = Processor.find_location_by_id(input_instance_array, element)[-10:]  # Here we get [0 1 0 0 0 0 0 0 1 0]

        if int(location[
                   int(sequence_of_desire[0]) - 1]) == 1:  # Check if e9 is set 1 in the element [0 1 0 0 0 0 0 0 1 0]
            sequence_of_desire = sequence_of_desire[
                                 1:]  # And we remove the 9 from the sequence of desire. Sequence of desire: 3 4

            if len(sequence_of_desire) == 0:  # If sequence of desire has been left with zero elements, then this constrain passed.
                return False
        count = count + 1  # If not, check other values in sequence if they will do the job.

    return SequenceOfDesire(sequence_of_trip='→'.join(sequence), is_validated=False)


def sequence_of_desire_validation(input_instance_array, solution_instance_array):
    input_instance_array_only_arrays_with_locations = input_instance_array[len(solution_instance_array) + 3:]

    validated_sequence_of_desire = []
    count = 0
    for solution_instance_element in solution_instance_array:
        validated_sequence_of_desire.append(
            check_sequence_of_desire(input_instance_array[count + 3:][0], solution_instance_element,
                                     input_instance_array_only_arrays_with_locations)
        )
        count = count + 1
    return validated_sequence_of_desire


class SequenceOfDesireValidator:
    pass
