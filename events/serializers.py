from rest_framework.serializers import ModelSerializer
from comrades.models import CustomUser
from events.models import Events


class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username']
        # fields = '__all__'


class EventSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Events
        fields = ('event', 'date_event', 'start_time', 'end_time', 'user', 'remind')

