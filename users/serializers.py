from rest_framework import serializers

from users.models import UserRole, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=UserRole.choices, default=UserRole.STUDENT)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            role=validated_data.get('role')
        )
        return user