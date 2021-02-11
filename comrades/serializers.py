from rest_framework import serializers
from rest_framework.fields import CharField
from comrades.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'country')


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'country')

    def validate(self, attrs):
        username = attrs['username']
        if username.find("@") != -1:
            raise serializers.ValidationError({f'{username}', 'This username looks like email'})
        return super().validate(attrs)

    def create(self, validated_data):
        self.user = CustomUser.objects.create_user(**validated_data)
        return self.user

    def save(self):
        self.user = super().save(is_active=False)
        return self.user


class ActivationSerializer(serializers.ModelSerializer):
    login = CharField(max_length=150, help_text='Enter email or username')

    class Meta:
        model = CustomUser
        fields = ('login',)


class LoginSerializer(serializers.ModelSerializer):
    login = CharField(max_length=150, help_text='Enter email or username')

    class Meta:
        model = CustomUser
        fields = ('login', 'password')