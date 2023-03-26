from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from validator_for_mctoptwp.validator.Budget import BudgetValidator
from validator_for_mctoptwp.validator.LocationVisitCounts import LocationVisitCountsValidator
from validator_for_mctoptwp.processor import Processor
from validator_for_mctoptwp.validator.Time import TimeValidator
from validator_for_mctoptwp.validator.SequenceOfDesire import SequenceOfDesire
from validator_for_mctoptwp.validator.MaxVertexCountValidator import MaxVertexCountValidator


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def validate(request):
    if request.method == 'POST':
        input_instance_file = request.FILES.get('input_instance', False)
        solution_instance_file = request.FILES.get('solution_instance', False)
        problem_type = request.POST.get('problem_type')

        input_instance = input_instance_file.read().decode('utf-8')
        solution_instance = solution_instance_file.read().decode('utf-8').rstrip()

        input_instance_array = Processor.turn_into_array(input_instance, ' ')
        solution_instance_array = Processor.turn_into_array(solution_instance, ' -> ')

        sums_of_vertices = Processor.turn_into_array(solution_instance_array.pop()[0], ' ')[0]

        location_visited_at_most_once = LocationVisitCountsValidator.validate_location_visited_at_most_once(
            solution_instance_array)
        budget = BudgetValidator.validate_budget(input_instance_array, solution_instance_array)

        time = TimeValidator.validate_time(input_instance_array, solution_instance_array, 'time_validation')
        inside_operating_hours = TimeValidator.validate_time(input_instance_array, solution_instance_array,
                                                             'inside_operating_hours_validation')

        max_allowed_number_of_vertices = None
        if problem_type == 'mctoptw' or problem_type == 'mctoptwp':
            max_allowed_number_of_vertices = MaxVertexCountValidator.validate_max_allowed_number_of_vertices(input_instance_array, sums_of_vertices)

        sequence_of_desire = None
        is_sequence_of_desire_validated = None
        if problem_type == 'toptwp' or problem_type == 'mctoptwp':
            sequence_of_desire = SequenceOfDesire.sequence_of_desire_validation(input_instance_array, solution_instance_array)
            is_sequence_of_desire_validated = Processor.is_constrain_validated(sequence_of_desire)

        return render(request, 'index.html', {
            'show_table': True,
            'location_visited_at_most_once_validation': location_visited_at_most_once,
            'budget_validation': budget,
            'time_validation': time,
            'is_time_validated': Processor.is_constrain_validated(time),
            'inside_operating_hours_validation': inside_operating_hours,
            'is_inside_operating_hours_validated': Processor.is_constrain_validated(inside_operating_hours),
            'max_allowed_number_of_vertices_validation': max_allowed_number_of_vertices,
            'sequence_of_desire_validation': sequence_of_desire,
            'is_sequence_of_desire_validated': is_sequence_of_desire_validated
        })
