from django.urls import path
from events.views import ListCreateEvent, StatisticByUser, StatisticDay, StatisticMonth

urlpatterns = [
    path("list_create_event/", ListCreateEvent.as_view(), name='list_create_event'),
    path("statistic_by_user/", StatisticByUser.as_view(), name='statistic_by_user'),
    path("statistic_day/", StatisticDay.as_view(), name='statistic_day'),
    path("statistic_month/", StatisticMonth.as_view(), name='statistic_month'),
]