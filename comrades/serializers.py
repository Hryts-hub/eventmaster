from rest_framework import serializers
from comrades.models import CustomUser  #,Country


# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = ['country']


class RegistrationSerializer(serializers.ModelSerializer):
    # country = CountrySerializer()
    user = None

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'country')

    def validate(self, attrs):
        email = attrs['email']
        username = attrs['username']
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({f'{email}', 'This email is already in use'})
        if username.find("@"):
            raise serializers.ValidationError({f'{username}', 'This username looks like email'})
        return super().validate(attrs)

    def create(self, validated_data):
        self.user = CustomUser.objects.create_user(**validated_data)
        return self.user

    def save(self, **kwargs):
        super().save(**kwargs)
        self.user.is_active = False
        self.user.save()
        return self.user

