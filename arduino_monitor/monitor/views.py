
import json
from django.http import JsonResponse, Http404
from django.shortcuts import render
from .models import SensorData
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


def data_list(request):
    data = SensorData.objects.all().order_by(
        '-timestamp')[:50]  # Latest 50 entries
    context = {'data': data}
    return render(request, 'monitor/data_list.html', context)

# monitor/views.py


def sensor_data_json(request):
    limit = int(request.GET.get('limit', 200))  # Default to 50 entries
    data = SensorData.objects.all().order_by('-timestamp')[:limit]
    data = reversed(data)  # Reverse the queryset to have the oldest first
    data_list = []

    for entry in data:
        data_point = {
            'timestamp': entry.timestamp.isoformat(),
            'value': entry.value
        }
        data_list.append(data_point)

    return JsonResponse(list(data_list), safe=False)
