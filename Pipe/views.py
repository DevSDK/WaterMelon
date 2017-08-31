from django.conf.locale import id
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from Pipe.models import Pipe
from Pipe.serializer import PipeSerializer


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def GetPipeList(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\": \"Invalid  POST Method\"}", status=400)
    if request.user is None:
        return HttpResponse("{\"message\": \"not allowed user session\"}", status=400)
    if request.user.is_authenticated() == False:
        return HttpResponse("{\"message\": \"Should be login\"}", status=400)

    data = Pipe.objects.filter(FK_User=request.user)
    serializer = PipeSerializer(data, many=True)
    return Response(serializer.data ,content_type=u"application/json; charset=utf-8")

@csrf_exempt
def PostPipeAdd(request):
    if request.method == 'GET':
        return HttpResponse("{\"message\": \"Invalid  GET Method\"}", status=400)
    if request.user is None:
        return HttpResponse("{\"message\": \"not allowed user session\"}", status=400)
    if request.user.is_authenticated() == False:
        return HttpResponse("{\"message\": \"Should be login\"}", status=400)

    nickname = request.POST.get("NickName")

    if nickname is None:
        return HttpResponse("{\"message\": \"required NickName=000\"}", status=400)

    pipe = Pipe.objects.create(NickName = nickname, FK_User= request.user)
    pipe.save()

    return HttpResponse("{\"message\": \"Success\"}")




@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def GetPipeInfo(request):
    if request.method == 'POST':
        return HttpResponse("{\"message\": \"Invalid  POST Method\"}", status=400)
    if request.user is None:
        return HttpResponse("{\"message\": \"not allowed user session\"}", status=400)
    if request.user.is_authenticated() == False:
        return HttpResponse("{\"message\": \"Should be login\"}", status=400)
    pipe = request.GET['pipe']

    if pipe is None:
        return HttpResponse("{\"message\": \"required pipe_parameter\"}", status=400)

    data = Pipe.objects.filter(id=pipe).last()

    if data is None:
        return HttpResponse("{\"message\": \"cannot find pipe\"}", status=400)


    serializer = PipeSerializer(data)
    return Response(serializer.data,content_type=u"application/json; charset=utf-8")