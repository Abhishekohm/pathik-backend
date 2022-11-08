from tkinter.messagebox import RETRY
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .models import User, TokensTable
from .serializers import UserSerializer, AuthUserSerializer
from .decorators import login_required
import jwt
from .utils import send_passwordreset_email
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # print(username, password)
    if username is None or password is None:
        raise AuthenticationFailed(code=401)

    user = User.objects.filter(username=username).first()
    if user is None:
        raise NotFound(code=404)

    instance = user
    user = AuthUserSerializer(user).data

    # checking password
    if check_password(password, user.get('password')) == False:
        return Response({
            'message': 'username or password is incorrect'
        }, status=401)

    # generating tokens
    access_token = instance.getAccessToken()
    refresh_token = instance.getRefreshToken()
    print('access_token => ', access_token)
    print('refresh_token => ', refresh_token)

    response = Response({
        'user': user,
        'access_token': access_token
    })
    response.set_cookie('jwt_refresh_token', refresh_token, httponly=True)
    return response


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if username is None or password is None or email is None:
        raise AuthenticationFailed(code=401)

    instance = User(username=username, email=email)
    instance.password = make_password(password)
    instance.save()
    user = UserSerializer(instance).data
    access_token = instance.getAccessToken()
    refresh_token = instance.getRefreshToken()
    print('access_token => ', access_token)
    print('refresh_token => ', refresh_token)
    response = Response({
        'user': user,
        'access_token': access_token
    })
    response.set_cookie('jwt_refresh_token', refresh_token, httponly=True)
    print(response)
    return response


@api_view(['GET'])
@login_required
def private(request):
    return Response({
        'message': 'private route hit'
    })


@api_view(['GET'])
def refresh(request):
    refresh_token = request.COOKIES.get('jwt_refresh_token')
    if refresh_token is None:
        return Response(status=403)
    user = User.objects.filter(refreshToken=refresh_token).first()

    if user is None:
        return Response(403)

    try:
        payload = jwt.decode(refresh_token, 'secret', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Response(status=403)
    except:
        return Response(status=500)

    seralized_user = UserSerializer(user).data

    if seralized_user.get('id') != payload.get('id'):
        return Response(status=403)

    access_token = user.getAccessToken()

    return Response({
        'access_token': access_token,
        'user': seralized_user
    })


# /api/auth/reset_password?userid=id&token=token
# validate the token and reset otherwise throw the error

@csrf_exempt
@api_view(['POST', 'GET'])
def reset_password(request, token, userId):
    if request.method == "POST":
        # username = request.data.get('username')
        # email = request.data.get('email')

        # user = User.objects.filter(
        #     Q(username=username) | Q(email=email)).first()
        # if user is None:
        #     raise NotFound(code=404)

        # serialized_user = UserSerializer(user).data
        # reset_token = user.getPasswordRefreshToken()
        # print(reset_token)

        # send_passwordreset_email(serialized_user.get('email'), reset_token)

        print(request.POST.get('password1'))
        print(request.POST.get('password2'))
        # me = messages.error(request, "Password not matching")

        return Response({
            'user': 'user'
        })

    elif request.method == "GET":
        print(token)
        print(userId)
        messages.error(request, "Password not matching")
        return render(request, 'reset_password.html')

# /api/resetpassword


@ api_view(['GET'])
def resetpasssord(request):
    username = request.GET.get('username')
    print(username)

    user = User.objects.filter(Q(username=username)).first()
    if user is None:
        raise NotFound(code=404)

    serialized_user = UserSerializer(user).data
    reset_token = user.getPasswordRefreshToken()
    print(reset_token)
    token = TokensTable(userid=user.id, resetToken=reset_token)
    token.save()
    print(serialized_user.get('email'))

    send_passwordreset_email(
        serialized_user.get('email'), reset_token, user.id)
    return Response({
        'status': True
    })


@ api_view(["GET"])
def test(request, testNo):
    print(testNo)
    return Response()
# seperete this view
# expected route - /api/logout not /api/auth/logout


@ api_view(['GET'])
def logout(request):
    refresh_token = request.COOKIES.get('jwt_refresh_token')
    print(refresh_token)
    if refresh_token is None:
        return Response(status=204)

    user = User.objects.filter(refreshToken=refresh_token).first()
    serialized_user = UserSerializer(user).data
    print(serialized_user)
    if user is None:
        response = Response(status=204)
        response.delete_cookie('jwt_refresh_token')
        return response

    user.refreshToken = ""
    user.save()
    serialized_user = UserSerializer(user).data

    print(serialized_user)
    response = Response(status=200)
    response.delete_cookie('jwt_refresh_token')

    return response
