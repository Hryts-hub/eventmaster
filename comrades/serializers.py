from rest_framework import serializers
from comrades.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    user = None

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'country')

    # code for login by username

    # def validate(self, attrs):
    #     email = attrs['email']
    #     if CustomUser.objects.filter(email=email).exists():
    #         raise serializers.ValidationError({f'{email}', 'This email is already in use'})
    #     return super().validate(attrs)

    def create(self, validated_data):
        self.user = CustomUser.objects.create_user(**validated_data)
        return self.user

    def save(self, **kwargs):
        super().save(**kwargs)
        self.user.is_active = False
        self.user.save()
        return self.user

