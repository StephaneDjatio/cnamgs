from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Prefetch
from .serializers import InspectionSerializer, QuestionSerializer, ValidAnswersSerializer
from gestion.models import Inspect, Question, Answer, ValidAnswer
import json


# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/companies/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of companies'
        },
        {
            'Endpoint': '/inspections/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of inspections'
        },
        {
            'Endpoint': '/inspections/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single of inspections'
        },
        {
            'Endpoint': '/inspections/id/update',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Returns a single of inspections'
        },
        {
            'Endpoint': '/login',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Connect to user account'
        },
        {
            'Endpoint': '/logout',
            'method': 'GET',
            'body': None,
            'description': 'Logout to user account'
        },
    ]

    return Response(routes)


@api_view(['GET'])
def getInspections(request):
    inspections = Inspect.objects.all()
    serializer = InspectionSerializer(inspections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getInspection(request, pk):
    inspection = Inspect.objects.get(pk=pk)
    serializer = InspectionSerializer(inspection, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateInspection(request, pk):
    data = request.data
    print(data)

    inspection = Inspect.objects.get(id=pk)
    serializer = InspectionSerializer(inspection, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)

    return Response(serializer.data)


@api_view(['GET'])
def getQuestions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def postAnswers(request):
    # print(json.loads(request.data['question']))
    Inspect.objects.filter(pk=request.data['idInspection']).update(is_completed=True)
    for question in json.loads(request.data['question']):
        # print(question['idQuestion'])
        validateAnswers = ValidAnswer.objects.create(inspect_id=request.data['idInspection'],
                                                     question_id=question['idQuestion'],
                                                     answer_id=question['selectedAnswer'])
    return Response('Confirm')


@api_view(['GET'])
def getAnswers(request, pk):
    answers = ValidAnswer.objects.filter(inspect_id=pk).all()
    serializer = ValidAnswersSerializer(answers, many=True)
    return Response(serializer.data)
