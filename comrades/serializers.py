from rest_framework import serializers
from comrades.models import CustomUser
# from comrades.models import Country
# from django.forms import CharField


# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         # fields = '__all__'
#         fields = ['country_name']


class RegistrationSerializer(serializers.ModelSerializer):
    user = None

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'password', 'first_name', 'last_name', 'country')

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
