import random

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.views import View

import tours.data as mock_data


def main_view(request):
    context = {}

    # для шапки
    context['title'] = mock_data.title
    context['subtitle'] = mock_data.subtitle

    context['description'] = mock_data.description
    context['departures'] = mock_data.departures

    count_sample = 6
    tours_id = mock_data.tours.keys()
    get_sample = min(count_sample, len(tours_id))
    random_tours = random.sample(tours_id, get_sample)
    context['random_tours'] = {i: mock_data.tours[i] for i in random_tours}

    return render(request, 'index.html', context)


def departure_view(request, departure: str):
    context = {}

    # для шапки
    context['title'] = mock_data.title
    context['departures'] = mock_data.departures

    context['cur_departure'] = departure

    _departure_tours = {}
    for tour_id, tour_data in mock_data.tours.items():
        if tour_data['departure'] == departure:
            _departure_tours[tour_id] = tour_data
    context['departure_tours'] = _departure_tours

    _tours_filtered_price = []
    _tours_filtered_nights = []
    for tour_id, tour_data in context['departure_tours'].items():
        _tours_filtered_price.append(tour_data['price'])
        _tours_filtered_nights.append(tour_data['nights'])
    context['min_price'] = min(_tours_filtered_price)
    context['max_price'] = max(_tours_filtered_price)
    context['min_nights'] = min(_tours_filtered_nights)
    context['max_nights'] = max(_tours_filtered_nights)

    return render(request, 'departure.html', context)


def tour_view(request, id: int):
    context = {}

    # для шапки
    context['title'] = mock_data.title
    context['departures'] = mock_data.departures

    current_tour = mock_data.tours[id]
    context['tour'] = current_tour

    return render(request, 'tour.html', context)


# Handlers
def custom_handler400(request, exception):
    # Call when SuspiciousOperation raised
    return HttpResponseBadRequest('Неверный запрос!')


def custom_handler403(request, exception):
    # Call when PermissionDenied raised
    return HttpResponseForbidden('Доступ запрещен!')


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
