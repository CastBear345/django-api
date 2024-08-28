from rest_framework import serializers
from django.contrib.auth import authenticate
from account.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    telegram_chat_id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username_lower = data['username'].lower()
        if CustomUser.objects.filter(username=username_lower).exists():
            raise serializers.ValidationError({"username": "Username is taken"})
        return data

    def create(self, data):
        user = CustomUser.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            telegram_chat_id=data['telegram_chat_id'],
            username=data['username'].lower()
        )
        user.set_password(data['password'])
        user.save()
        return data
  
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not CustomUser.objects.filter(username=data['username'].lower()).exists():
            raise serializers.ValidationError("Account not found")
        return data

    def get_jwt_token(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            return {'message': 'Invalid credentials', 'data': {}}

        refresh = RefreshToken.for_user(user)

        return {
            'message': 'Login success',
            'data': {
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
        }