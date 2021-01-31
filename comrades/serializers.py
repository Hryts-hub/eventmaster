from rest_framework import serializers
from comrades.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    user = None

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'country')

    def create(self, validated_data):
        self.user = CustomUser.objects.create_user(**validated_data)
        return self.user

    def save(self, **kwargs):
        super().save(**kwargs)
        self.user.is_active = False
        self.user.save()
        return self.user


