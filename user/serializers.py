from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from core.helpers import generate_password


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'password2', 'email', 'address', 'phone')
        extra_kwargs = {'password': {'style': {'input_type': 'password'}, 'write_only': True,
                                     'required': False, 'min_length': 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def validate(self, data):
        if 'password' in data:
            if 'password2' in data:
                if data['password'] != data['password2']:
                    msg = _("Passwords don't match.")
                    raise serializers.ValidationError(msg)
                del data['password2']
            else:
                msg = _("No confirmation password provided.")
                raise serializers.ValidationError(msg)
        elif 'password2' in data:
            msg = _("Only confirmation password provided.")
            raise serializers.ValidationError(msg)
        else:
            data['password'] = generate_password()
        if 'phone' in data:
            if (len(data['phone']) != 10) | (not data['phone'].isdigit()):
                raise serializers.ValidationError("Phone number must be 10 numbers.")
        return data


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
