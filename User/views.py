from coreapi import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.contrib import auth

from User.serializer import UserSerializer

'''

Raw Data Field 는 10만개 유지(변동가능)


GET	/data/current/raw		response: Get CurrentData
GET	/data/current/hour		response: Get CurrentHourData
GET	/data/current/day		response: Get CurrentDay
GET	/data/current/year		response: GET CurrentYear

GET	/data/list/hour		Parameter:date=YYYY-mm-dd	response: hour data from day (24)
GET	/data/list/year		Parameter:date=YYYY-mm-dd	response: hour data list from year(8,760)

POST	/data/push		Body { Temp = 온도, Data = 흐름량L/sec, Pipe=파이프}

POST	/user/login		BODY { ID = 아이디, Password = 페스워드}

GET	/user/profile		response: Profile  Info {Name,Etc...}

'''


@csrf_exempt
def PostLogin(request):
    try:
        if request.method == 'GET':
            return HttpResponse("{\"mesage\": \"Invalid  GET Method\"}",status=400)
        if request.method == 'POST':
            if request.user.is_authenticated():
                return HttpResponse("{\"message\":\"IsLogined\"}",status=400)
            id = request.POST.get("id")
            pw = request.POST.get('pw')
            if id is None or pw is None:
                return HttpResponse("{\"message\":\"Parameter Denied\"}",status=400)
            user = auth.authenticate(username=id, password=pw)
            if user is None:
                return HttpResponse("{\"message\":\"Login InValid\"}",status=400)
            if user.is_active:
               auth.login(request, user)
            return HttpResponse('{\"message\":\"OK\"}')
    except Exception as e:
        return HttpResponse("{\"message\": \"" + e.__str__() + "\"}", status=400)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def GetProfile(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\": \"Invalid  POST Method\"}", status=400)
    if request.user is None:
        return HttpResponse("{\"message\": \"not allowed user session\"}", status=400)
    if request.user.is_authenticated() == False:
        return HttpResponse("{\"message\": \"Should be login\"}", status=400)

    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def PostRegister(request):
    if request.method == 'GET':
        return HttpResponse("{\"message\": \"Invalid GET Method\"}", status=400)

    Username = request.POST.get("username")
    EMail = request.POST.get("e-mail")
    Password = request.POST.get("password")
    Firstname = request.POST.get("firstname")
    Lastname = request.POST.get("lastname")

    if Username is None or EMail is None or Password is None or Firstname is None or Lastname is None:
        return HttpResponse("{\"message\": \"Register Invalid, Username, Email, Password , FirstName, LastName Field Required\"}", status=400)
    user = User.objects.create(Username, EMail, Password)

    user.first_name = Firstname
    user.last_name = Lastname

    user.save()

    return HttpResponse("{\"message\":\"register ok \"}")





