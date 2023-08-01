from rest_framework.serializers import ModelSerializer
from gestion.models import Inspect, Mission, Company, Agent, Sector, \
    City, Answer, Question, ValidAnswer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    ##
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class SectorSerializer(ModelSerializer):
    class Meta:
        model = Sector
        fields = ['sector_name']


class CompanySerializer(ModelSerializer):
    sector = SectorSerializer()
    city = CitySerializer()

    class Meta:
        model = Company
        fields = '__all__'


class AgentSerializer(ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class MissionSerializer(ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class InspectionSerializer(ModelSerializer):
    company = CompanySerializer(read_only=True)
    # agent = AgentSerializer()
    mission = MissionSerializer(read_only=True)

    class Meta:
        model = Inspect
        fields = '__all__'


class QuestionAnswersSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    answer = QuestionAnswersSerializer(source='answer_set', many=True)

    class Meta:
        model = Question
        fields = '__all__'


class ValidAnswersSerializer(ModelSerializer):
    inspect = InspectionSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = ValidAnswer
        fields = '__all__'
