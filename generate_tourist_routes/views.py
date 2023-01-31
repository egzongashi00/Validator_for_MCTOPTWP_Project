from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django_dump_die.middleware import dd


def sum_eighth_element(id_list, input_instance):
    array_list = []
    lines = input_instance.splitlines()
    for line in lines:
        array_list.append(line.split())

    result = 0
    for arr in array_list:
        if int(arr[0]) in list(map(int, id_list)) and arr[0] != '0':
            result += int(arr[7])
    return result


@csrf_exempt
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        input_instance_file = request.FILES.get('input_instance', False)
        solution_instance_file = request.FILES.get('solution_instance', False)

        input_instance = input_instance_file.read().decode('utf-8')
        solution_instance = solution_instance_file.read().decode('utf-8').split(' -> ')

        return render(request, 'index.html', {
            'validated': True,
            'expected_budget': input_instance.split()[2],
            'actual_budget': sum_eighth_element(solution_instance, input_instance)
        })
