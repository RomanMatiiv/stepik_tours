from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.http import HttpResponseServerError
from django.views import View

import tours.data as mock_data


def main_view(request):
    return render(request, 'index.html')


def departure_view(request, departure: str):
    return render(request, 'departure.html')


def tour_view(request, id: int):
    tour_data = mock_data.tours[id]

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


# class TestView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'test.html', {'name': 'Alex', 'place': 'Lab'})
#
#
# class TestIndex(View):
#     def get(self, request):
#         return render(request, 'test_index.html')
#
#
# class TestAbout(View):
#     def get(self, request):
#         return render(request, 'test_about.html')


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
