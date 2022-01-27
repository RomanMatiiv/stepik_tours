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
    context['title'] = mock_data.title
    context['subtitle'] = mock_data.subtitle
    context['description'] = mock_data.description
    context['departures'] = mock_data.departures

    get_sample = 6
    tours_keys = mock_data.tours.keys()
    if len(tours_keys) < get_sample:
        get_sample = len(tours_keys)
    random_tours = random.sample(tours_keys, get_sample)
    context['random_tours'] = {i: mock_data.tours[i] for i in random_tours}

    return render(request, 'index.html', context)


def departure_view(request, departure: str):
    context = {}
    context['cur_departure_readable'] = mock_data.departures[departure]
    context['departure'] = departure
    context['departures'] = mock_data.departures

    context['title'] = mock_data.title

    tours_filtered = {}
    _tours_filtered_price = []
    _tours_filtered_nights = []
    for tour_id, tour_data in mock_data.tours.items():
        if tour_data['departure'] == departure:
            tours_filtered[tour_id] = tour_data
            _tours_filtered_price.append(tour_data['price'])
            _tours_filtered_nights.append(tour_data['nights'])
    tour_min_price = min(_tours_filtered_price)
    tour_max_price = max(_tours_filtered_price)
    tour_min_nights = min(_tours_filtered_nights)
    tour_max_nights = max(_tours_filtered_nights)

    context['tours_filtered'] = tours_filtered
    context['tour_min_price'] = tour_min_price
    context['tour_max_price'] = tour_max_price
    context['tour_min_nights'] = tour_min_nights
    context['tour_max_nights'] = tour_max_nights

    return render(request, 'departure.html', context)


def tour_view(request, id: int):
    tour_data = mock_data.tours[id]

    tour_data['title'] = mock_data.title

    tour_data['departures'] = mock_data.departures

    # определяем departure из справочника
    encoded_departure = tour_data['departure']
    decoded_departure = mock_data.departures[encoded_departure]
    tour_data['departure_readable'] = decoded_departure

    tour_data['stars_readable'] = '★' * int(tour_data['stars'])

    # разделяем тысячи в цене с помощью пробелов
    tour_price = tour_data['price']
    tour_data['price_readable'] = '{:,}'.format(tour_price).replace(',', ' ')

    _nights = int(tour_data['nights'])
    if _nights == 1:
        tour_data['nights_postfix'] = 'ночь'
    elif _nights == 2:
        tour_data['nights_postfix'] = 'ночи'
    else:
        tour_data['nights_postfix'] = 'ночей'

    return render(request, 'tour.html', tour_data)


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
