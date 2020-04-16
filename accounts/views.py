import random
import string

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import HttpResponse
# import that facilitate activation token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# local imports
from .email import send_welcome_email
from .models import *
from .serializers import *
from .sms import send_confirmation_code, fall_back_confirmation_code
from .tokens import account_activation_token

User = get_user_model()

# generate random code

class UserCreate(APIView):
    """
    Registration of a user.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @staticmethod
    def post(request):
        """
        gets data from request then checks whether the user_data
        is valid before it saves it to the database
        :param request:
        :return: response status {error HTTP_400 or success HTTP_201}
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                cleaned_user = serializer.data
                email = cleaned_user['email']
                name = cleaned_user['username']
                send_welcome_email(name, email, user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    """
    ***** BACKEND IS VERY IMPORTANT ******
    adding backend help resolve the multiple authentication issues

    TODO LIST (DESIGN)
    1. Add templates to replace `return HttpResponse('Thank you for your email confirmation. Now you can login your
        account.') and  return HttpResponse('Activation link is invalid!')`
    2. Write test and maintain the existing code to pass
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class CurrentUserView(APIView):
    """
    Getting current user
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    allow user to retrieve and update there information
    """
    serializer_class = ProfileSerializers
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        """
        GET Method to get the current user profile details
        :param self:
        :param request:
        :return:
        """
        profile = Profile.objects.get(user=request.user.id)
        serializers = ProfileSerializers(profile)
        if request.user.id == profile.user.id:
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def patch(self, request):

        """
        update user profile
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user.id)
            serializer = ProfileSerializers(profile, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UpdatePhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch (self, request):
        """
        update phone number
        :param request:
        :return:
        """ 
        current_user = Profile.objects.get(user=request.user.id)
        serializers = ProfileSerializers(current_user, request.data, partial=True)
        if serializers.is_valid():
            code = ''.join(random.sample((string.digits), 4))
            phone_number = serializers.validated_data.get('phone_number', None)
            current_user.confirmed_code = False
            serializers.save()
            print(code,'user code here-------------------')
            if phone_number is not None and send_confirmation_code(code, phone_number) is 'sent' or 'queued':
                current_user.verification_code = code
                current_user.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationCodeView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        validate phone number
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            current_user = Profile.objects.get(user=request.user.id)
            confirmation_code = request.data.get('confirmation_code', None)
            if current_user.verification_code == confirmation_code:
                current_user.confirmed_code = True
                current_user.save()
                serializers = ProfileSerializers(current_user)
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class ChangePasswordView(APIView):
    """
    An endpoint for changing the user's password.
    """
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

    def put(self, request):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"success":True})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

