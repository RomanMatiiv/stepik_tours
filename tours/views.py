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

    # для шапки
    context['title'] = mock_data.title
    context['departures'] = mock_data.departures

    context['cur_departure_readable'] = mock_data.departures[departure]
    context['departure'] = departure
    context['departures'] = mock_data.departures

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

    context['title'] = mock_data.title
    context['subtitle'] = mock_data.subtitle
    context['description'] = mock_data.description
    context['departures'] = mock_data.departures

    current_tour = mock_data.tours[id]
    context['tour'] = current_tour

    # определяем departure из справочника
    _encoded_departure = current_tour['departure']
    _decoded_departure = mock_data.departures[_encoded_departure]
    context['tour']['departure_readable'] = _decoded_departure

    context['tour']['stars_readable'] = '★' * int(current_tour['stars'])

    # TODO написать свой фильтр (https://docs.djangoproject.com/en/4.0/howto/custom-template-tags/)
    # разделяем тысячи в цене с помощью пробелов
    _tour_price = current_tour['price']
    context['tour']['price_readable'] = '{:,}'.format(_tour_price).replace(',', ' ')

    # TODO заменить на фильтр
    #  https://gist.github.com/dpetukhov/cb82a0f4d04f7373293bdf2f491863c8
    #  https://vas3k.ru/dev/django_ru_pluralize/
    _nights = int(current_tour['nights'])
    if _nights == 1:
        context['tour']['nights_postfix'] = 'ночь'
    elif _nights == 2:
        context['tour']['nights_postfix'] = 'ночи'
    else:
        context['tour']['nights_postfix'] = 'ночей'

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
