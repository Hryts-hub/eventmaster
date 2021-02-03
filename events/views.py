from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.models import Events
from events.serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter


class MyPaginator(PageNumberPagination):
    page_size = 3


class ListCreateEvent(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    pagination_class = MyPaginator
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["date_event", "start_time"]
    queryset = Events.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
    # by token only
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        date_event = data['date_event']
        events = Events.objects.filter(user=request.user, date_event=date_event).order_by("start_time")
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


class StatisticMonth(APIView):
    # by token only
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        month = data['month']
        events = Events.objects.filter(user=request.user)#.order_by("date_event", "start_time")
        data = dict()

        date_list = []
        for event in events:
            date_event = event.date_event
            if str(date_event).startswith(month):
                date_list.append(date_event)
        list(set(date_list)).sort()
        for date in date_list:
            events_per_day = events.filter(date_event=date).order_by("start_time")
            i = 0
            event_list = []
            ev = dict()
            for day_event in events_per_day:
                start_time = day_event.start_time
                end_time = day_event.end_time
                event_name = day_event.event
                i += 1
                ev[i] = [start_time, end_time, event_name]
                event_list.append(ev[i])
            data[str(date)] = event_list
        return Response(data, status=status.HTTP_200_OK)