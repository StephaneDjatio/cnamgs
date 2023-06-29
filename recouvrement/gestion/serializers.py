from rest_framework import serializers
from django.db.models import Sum, Prefetch
from .models import Trimester, Contribution, Payment, Company, User, City, Sector, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['sector_name']


class AllTrimesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trimester
        fields = '__all__'


class ContributionSerializer(serializers.ModelSerializer):
    trimester = AllTrimesterSerializer()

    class Meta:
        model = Contribution
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    trimester = AllTrimesterSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    city = CitySerializer()
    contact = ContactSerializer()
    contribution = ContributionSerializer(source='contribution_set', many=True)
    payment = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = Company
        fields = '__all__'


class PaymentPerTrimester(serializers.ModelSerializer):
    trimester = AllTrimesterSerializer()
    company = CompanySerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class TrimesterSerializer(serializers.ModelSerializer):
    contribution = ContributionSerializer(source="contribution_set", many=True)
    payment = PaymentSerializer(source="payment_set", many=True)

    class Meta:
        model = Trimester
        fields = '__all__'


class CompanyPaymentTrimesterSerializer(serializers.ModelSerializer):
    contribution = ContributionSerializer(source="contribution_set", many=True)
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_payments(self, obj):
        company_payment_query = Payment.objects.filter(company_id=obj.id).\
            values('trimester__id','trimester__trimester_begin', 'trimester__trimester_end'). \
            annotate(total=Sum('payment_amount'))
        serializer = PaymentSerializer(company_payment_query, many=True)
        return serializer.data
