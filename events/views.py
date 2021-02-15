from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.models import Events, Holidays
from events.serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from datetime import datetime
from django.utils import timezone

from events.services import event_per_day_func


class MyPaginator(PageNumberPagination):
    page_size = 3


class ListCreateEvent(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    # this code for testing with SessionAuthentication
    pagination_class = MyPaginator
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["date_event", "start_time"]
    queryset = Events.objects.all().order_by("user")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(user=request.user)
            if event.remind:
                t = str(timezone.make_aware(datetime.now()) - event.time_to_remind)
                if not t.startswith("-"):
                    serializer.validated_data["message"] = f"You create the event with remind in the past " \
                                                           f"- we can't remind you about this event by email"
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.error_messages,
            status=status.HTTP_400_BAD_REQUEST
        )


class StatisticByUser(APIView):
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Events.objects.filter(user=request.user).order_by("date_event", "start_time")
        data = dict()
        i = 0
        for event in events:
            event_name = event.event
            date_event = event.date_event
            start_time = event.start_time
            end_time = event.end_time
            i += 1
            data[i] = [date_event, start_time, end_time, event_name]
        return Response(data, status=status.HTTP_200_OK)


class StatisticDay(APIView):
    # by token only,
    # to test SessionAuthentication  date_event = "2021-05-05"
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        # in tests data fields in url.
        # GET '/events/statistic_day/?date_event=2021-08-08',
        # during running tests data == {} and we are gets data fields from request.META['QUERY_STRING']
        if data == {}:
            date_event_str = request.META['QUERY_STRING']
            date_event = date_event_str.split("=")[1]
        else:
            # date_event = "2021-05-05"
            date_event = data['date_event']
        events = Events.objects.filter(user=request.user, date_event=date_event).order_by("start_time")
        data = dict()
        data[str(date_event)] = event_per_day_func(events)
        return Response(data, status=status.HTTP_200_OK)


class StatisticMonth(APIView):
    # by token only
    # to test SessionAuthentication  month = "2021-05"
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        if data == {}:
            month_str = request.META['QUERY_STRING']
            month = month_str.split("=")[1]
        else:
            # month = "2021-05" #  test
            month = data['month']
        events = Events.objects.filter(user=request.user).order_by("date_event")
        data = dict()
        date_list = []
        for event in events:
            date_event = event.date_event
            if str(date_event).startswith(month) and date_event not in date_list:
                date_list.append(date_event)
        for date in date_list:
            events_per_day = events.filter(date_event=date).order_by("start_time")
            data[str(date)] = event_per_day_func(events_per_day)
        return Response(data, status=status.HTTP_200_OK)


class HolidaysMonth(APIView):
    # by token only
    # to test SessionAuthentication  month = "2021-05"
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        if data == {}:
            month_str = request.META['QUERY_STRING']
            month = month_str.split("=")[1]
        else:
            # month = "2021-05"  #  test
            month = data['month']
        user = request.user
        country = user.country
        holidays = Holidays.objects.filter(country=country).order_by("date")
        data = dict()
        date_list = []
        for day in holidays:
            date = day.date
            if str(date).startswith(month) and date not in date_list:
                date_list.append(date)
        for date in date_list:
            holiday_per_day = holidays.filter(date=date)
            i = 0
            holiday_list = []
            holy = dict()
            for day_holiday in holiday_per_day:
                holiday = day_holiday.holiday.split(': ')[1]
                duration = day_holiday.duration.split(',')[0]
                description = day_holiday.description
                i += 1
                holy[i] = [holiday, description, duration]
            holiday_list.append(holy)
            data[str(date)] = holiday_list
        return Response(data, status=status.HTTP_200_OK)
