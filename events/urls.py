from django.urls import path
from events.views import ListCreateEvent, StatisticByUser, StatisticDay, StatisticMonth
# from events.views import ListHolidays
from events.views import HolydaysMonth

urlpatterns = [
    path("list_create_event/", ListCreateEvent.as_view(), name='list_create_event'),
    path("statistic_by_user/", StatisticByUser.as_view(), name='statistic_by_user'),
    path("statistic_day/", StatisticDay.as_view(), name='statistic_day'),
    path("statistic_month/", StatisticMonth.as_view(), name='statistic_month'),
    # path("list_holidays/", ListHolidays.as_view(), name='list_holidays'),
    path("holidays_month/", HolydaysMonth.as_view(), name='holidays_month'),
]