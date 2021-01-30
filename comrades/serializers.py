from rest_framework import serializers
from comrades.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=50, min_length=4)
    # email = serializers.EmailField(max_length=50, min_length=4)
    # first_name = serializers.CharField(max_length=50, min_length=4)
    # last_name = serializers.CharField(max_length=50, min_length=4)
    # country = serializers.CharField(max_length=50, min_length=4)
    # # The password must be validated and should not be read by the client
    # password = serializers.CharField(
    #     max_length=128,
    #     min_length=8,
    #     write_only=True,
    # )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    # webtoken = serializers.CharField(max_length=255, read_only=True)
    user = None

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'country')

    def validate(self, attrs):
        email = attrs['email']
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email', 'Email is already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        self.user = CustomUser.objects.create_user(**validated_data)
        return self.user

    def save(self, **kwargs):
        super().save(**kwargs)
        self.user.is_active = False
        self.user.save()
        return self.user

