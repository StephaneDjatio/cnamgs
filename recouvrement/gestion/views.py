import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum, Prefetch
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Sector, City, Company, Localization, \
    Agent, Payment, Trimester, Contribution, Mission, \
    AgentAppointedMission, CompanyAppointedMission, PaymentFiles, User, Accountant, Manager, Inspect, ValidAnswer
from .serializers import TrimesterSerializer, CompanyPaymentTrimesterSerializer, UserSerializer, CompanySerializer
from api.serializers import ValidAnswersSerializer, InspectionSerializer
from .forms import UserRegistrationForm


# Create your views here.

def get_random_code(characters):
    prefix = random.randint(10, 99)
    number = random.randint(1000, 10000)
    check = int((prefix * 1e10) + number) % 97
    return f"{characters}-{number:0>2d}-{check:0>2d}"


def connect_user(request):
    template = loader.get_template('users/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            context = {'error': 'Invalid username or password'}
            messages.error(request, "Invalid username or password")
            return HttpResponse(template.render(context, request))
        else:
            login(request, user)
            return redirect(reverse('index'))
    return HttpResponse(template.render({}, request))


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse('login_user'))


@login_required(login_url='/')
def index(request):
    localizations = Localization.objects.prefetch_related().all()
    trimesters = Trimester.objects.all()
    companies = Company.objects.all()
    sectors = Sector.objects.all()
    template = loader.get_template('index.html')
    return HttpResponse(
        template.render({'localizations': localizations, 'trimesters': trimesters, 'sectors': sectors, 'companies': companies}, request))


def get_trimesters_view(request):
    trimesters = Trimester.objects.filter(trimester_begin__year=request.GET["year_value"]).all()
    return JsonResponse({"trimesters": list(trimesters.values())})


def get_company_per_year(request):
    company = Company.objects.filter(id=request.GET["company_id"]).values()
    if request.GET["trimester_id"] == "all":
        trimesters = Trimester.objects.filter(trimester_begin__year=request.GET["year_value"]).all()
    else:
        trimesters = Trimester.objects.filter(id=request.GET["trimester_id"]).all()
    array_payments = []
    array_contributions = []
    for comp in company:
        sector = Sector.objects.filter(id=comp['sector_id']).values()
        for trimester in trimesters:
            payments = Payment.objects.filter(company_id=request.GET["company_id"], trimester=trimester).aggregate(
                Sum('payment_amount')).values()
            contributions = Contribution.objects.filter(company_id=request.GET["company_id"],
                                                        trimester=trimester).aggregate(Sum('total_amount')).values()
            array_payments.append(list(payments))
            array_contributions.append(list(contributions))
    return JsonResponse({"company": list(company), "sector": list(sector), "payments": array_payments,
                         "contributions": array_contributions})


@login_required(login_url='/')
def get_company_detail_from_map(request):
    array_trimester_ids = []
    if request.GET["trimester_id"] == "all":
        trimesters = Trimester.objects.filter(trimester_begin__year=request.GET["year_value"]).values('id')
    else:
        trimesters = Trimester.objects.filter(id=request.GET["trimester_id"]).values('id')

    for trimester in trimesters:
        array_trimester_ids.append(trimester['id'])

    print(array_trimester_ids)
    company = Company.objects.filter(id=request.GET["company_id"])\
        .prefetch_related(
        Prefetch('contribution_set', Contribution.objects.filter(trimester_id__in=array_trimester_ids)),
        Prefetch('payment_set', Payment.objects.filter(trimester_id__in=array_trimester_ids)),
    ).all()
    serializer = CompanySerializer(company, many=True)
    return JsonResponse({"company": serializer.data})


@login_required(login_url='/')
def sector_view(request):
    return HttpResponse('Hello, welcome to the Sector page.')


@login_required(login_url='/')
def company_view(request):
    companies = Company.objects.select_related().all()
    template = loader.get_template('company/company.html')
    context = {
        'companies': companies,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def add_company(request):
    message = False
    if request.method == "POST":
        company_name = request.POST["company_name"]
        sector = Sector.objects.get(pk=int(request.POST["sector_name"]))
        city = City.objects.get(pk=int(request.POST["city_name"]))
        company = Company.objects.create(company_name=company_name, sector=sector, city=city)
        if 'latitude' in request.POST:
            latitude = request.POST["latitude"]
            longitude = request.POST["longitude"]
            Localization.objects.create(latitude=latitude, longitude=longitude, company=company)
        messages.success(request, 'Company created successfully.')
        return redirect(reverse('companies'))
    sectors = Sector.objects.all().values()
    cities = City.objects.all().values()
    template = loader.get_template('company/add_company.html')
    context = {
        'sectors': sectors,
        'cities': cities,
        'message': message
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def edit_company(request):
    company = Company.objects.filter(id=request.GET["company_id"]).values()
    sectors = Sector.objects.all().values()
    cities = City.objects.all().values()
    data = {
        'company': list(company),
        'sectors': list(sectors),
        'cities': list(cities),
    }
    return JsonResponse(data)


@login_required(login_url='/')
def update_company(request):
    company_name = request.POST["company_name"]
    sector = Sector.objects.get(pk=int(request.POST["sector_name"]))
    city = City.objects.get(pk=int(request.POST["city_name"]))
    Company.objects.filter(pk=request.POST["id_company"]).update(company_name=company_name, sector=sector, city=city)
    messages.success(request, 'Company updated successfully.')
    return redirect(company_view)


@login_required(login_url='/')
def delete_company(request):
    company_id = request.POST["id_company"]
    company = Company.objects.filter(id=company_id).get()
    Localization.objects.filter(company=company).delete()
    Company.objects.filter(id=company_id).delete()
    messages.error(request, 'Company deleted successfully.')
    return redirect(company_view)


@login_required(login_url='/')
def list_company_contributions(request, **kwargs):
    if request.method == "POST":
        company_id = request.POST['id_company']
        trimester_id = request.POST['trimester_id']
        amount = request.POST['amount']
        Contribution.objects.create(company_id=company_id, trimester_id=trimester_id, total_amount=amount)
        messages.success(request, 'Company contribution updated successfully.')
    company = Company.objects.filter(pk=kwargs.get('company_id')).get()
    template = loader.get_template('company/contributions.html')
    context = {
        'company': company,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def get_company_contributions(request, **kwargs):
    trimesters = Trimester.objects \
        .prefetch_related(
        Prefetch('contribution_set', Contribution.objects.filter(company_id=kwargs.get('company_id'))),
    ).all()
    serializer = TrimesterSerializer(trimesters, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)


@login_required(login_url='/')
def update_localization(request):
    company = Company.objects.filter(id=request.POST["id_company"]).get()
    latitude = request.POST["latitude"]
    longitude = request.POST["longitude"]
    Localization.objects.create(latitude=latitude, longitude=longitude, company=company)
    messages.success(request, 'Company marker updated successfully.')
    return redirect(company_view)


@login_required(login_url='/')
def get_company_location(request):
    company_id = request.GET.get('company_id', None)
    company = Company.objects.filter(id=company_id).get()
    marker = Localization.objects.filter(company=company).values()
    data = {
        'data': list(marker)
    }
    return JsonResponse(data)


@login_required(login_url='/')
def trimester_view(data):
    pass


def getTrimestersUnsolvePerYear(request):
    trimesters = Trimester.objects \
        .filter(trimester_begin__year=request.GET["year_value"]) \
        .prefetch_related(
        Prefetch('contribution_set', Contribution.objects.filter(company_id=request.GET["company_id"])),
        Prefetch('payment_set', Payment.objects.filter(company_id=request.GET["company_id"])),
    ).all()
    serializer = TrimesterSerializer(trimesters, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)


def selectTrimesterContributionPayment(request):
    trimesters = Trimester.objects \
        .filter(id=request.GET["trimester_id"]) \
        .prefetch_related(
        Prefetch('contribution_set', Contribution.objects.filter(company_id=request.GET["company_id"])),
        Prefetch('payment_set', Payment.objects.filter(company_id=request.GET["company_id"])),
    ).all()
    serializer = TrimesterSerializer(trimesters, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)


@login_required(login_url='/')
def agent_view(request):
    agents = Agent.objects.all()
    template = loader.get_template('agent_view/agent.html')
    context = {
        'agents': agents,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def add_agent(request):
    if request.method == "POST":
        registration_number = request.POST["registration_number"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        agent = Agent.objects.create(registration_number=registration_number, firstname=firstname, lastname=lastname,
                                     email=email, phone_number=phone_number)
        messages.success(request, 'Agent created successfully.')
        return redirect(reverse("agents"))
    template = loader.get_template('agent_view/add_agent.html')
    context = {
        'registration_number': get_random_code("CN"),
    }
    return HttpResponse(template.render(context, request))


def get_agent(request):
    agent = Agent.objects.filter(id=request.GET["agent_id"]).values()
    data = {
        'agent': list(agent),
    }
    return JsonResponse(data)


@login_required(login_url='/')
def update_agent(request):
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    email = request.POST["email"]
    phone_number = request.POST["phone_number"]
    Agent.objects.filter(pk=request.POST["id_agent"]).update(firstname=firstname, lastname=lastname, email=email,
                                                             phone_number=phone_number)
    messages.success(request, 'Agent updated successfully.')
    return redirect(agent_view)


@login_required(login_url='/')
def mission_view(request):
    missions = Mission.objects.prefetch_related("agentappointedmission_set", "companyappointedmission_set").all()
    template = loader.get_template('missions/list_missions.html')
    context = {
        'missions': missions,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def add_mission(request):
    if request.method == "POST":
        # print(request.POST)
        mission_order_number = request.POST["order_number"]
        mission_date = parse_date(request.POST["mission_date"])
        mission_objective = request.POST["mission_objective"]
        mission_agents = request.POST.getlist("agents_selected")
        mission_companies = request.POST.getlist("companies_selected")
        mission = Mission.objects.create(mission_order_number=mission_order_number, mission_date=mission_date,
                                         mission_objective=mission_objective)
        for mission_agent in mission_agents:
            AgentAppointedMission.objects.create(agent_id=mission_agent, mission=mission)
        for mission_company in mission_companies:
            CompanyAppointedMission.objects.create(company_id=mission_company, mission=mission)
            Inspect.objects.create(inspection_date=mission_date, mission=mission, company_id=mission_company)
        messages.success(request, 'Mission created successfully.')
        return redirect(reverse("missions"))
    template = loader.get_template('missions/add_mission.html')
    agents = Agent.objects.all()
    companies = Company.objects.all()
    context = {
        'mission_number': get_random_code("MI"),
        'agents': agents,
        'companies': companies,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def payment_view(request):
    template = loader.get_template('payments/payments.html')
    return HttpResponse(template.render({}, request))


def load_payments(request):
    payments = Payment.objects.select_related('trimester', 'company'). \
        values('trimester__id', 'company__id', 'trimester__trimester_begin', 'trimester__trimester_end',
               'company__company_name'). \
        annotate(total=Sum('payment_amount'))
    contributions = Contribution.objects.select_related('trimester', 'company'). \
        values('trimester__id', 'company__id', 'trimester__trimester_begin', 'trimester__trimester_end',
               'company__company_name'). \
        annotate(total=Sum('total_amount'))
    context = {
        'payments': list(payments),
        'contributions': list(contributions),
    }
    return JsonResponse(context)


def load_payment(request):
    company = Company.objects.all()
    serializer = CompanyPaymentTrimesterSerializer(company, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)


@login_required(login_url='/')
def detail_payment_view(request, **kwargs):
    print(kwargs.get('company_id'))
    company = Company.objects.filter(pk=kwargs.get('company_id')).get()
    trimester = Trimester.objects.filter(pk=kwargs.get('trimester_id')).get()
    payments = Payment.objects.filter(company=company, trimester=trimester).all()
    template = loader.get_template('payments/detail-payment.html')
    context = {
        'company': company,
        'trimester': trimester,
        'payments': payments,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def add_payment(request):
    template = loader.get_template('payments/add_payment.html')
    trimesters = Trimester.objects.all()
    companies = Company.objects.all()
    context = {
        'payment_number': get_random_code("FA"),
        'trimesters': trimesters,
        'companies': companies,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/')
def save_payment(request):
    print(request.FILES)
    if request.POST.get('action') == 'post':
        Payment.objects.create(
            payment_number=request.POST.get('payment_number'),
            payment_date=request.POST.get('payment_date'),
            payment_amount=request.POST.get('payment_amount'),
            company_id=request.POST.get('company'),
            trimester_id=request.POST.get('trimester'),
        )
        files = request.FILES.getlist('files[]', None)
        for file in files:
            print(file)
            uploadFile = PaymentFiles(file=file)
            uploadFile.save()
        return JsonResponse({'msg': '<span style="color: green;">Payment successfully uploaded</span>'}, safe=False)
    else:
        return JsonResponse({'msg': '<span style="color: green;">Payment failed to uploaded</span>'}, safe=False)


@login_required(login_url='/')
def inspection_view(request):
    inspections = Inspect.objects.all()
    template = loader.get_template('inspections/inspections.html')
    return HttpResponse(template.render({"inspections": inspections}, request))


@login_required(login_url='/')
def inspection_detail_view(request, **kwargs):
    answers = ValidAnswer.objects.filter(inspect_id=kwargs.get('inspection_id')).all()
    serializer = ValidAnswersSerializer(answers, many=True)
    inspection = Inspect.objects.get(id=kwargs.get('inspection_id'))
    serializer2 = InspectionSerializer(inspection)
    template = loader.get_template('inspections/inspection-detail.html')
    return HttpResponse(template.render({"answers": serializer.data, "inspection": serializer2.data}, request))


@login_required(login_url='/')
def report_view(request):
    companies = Company.objects.all()
    template = loader.get_template('reports/reports.html')
    return HttpResponse(template.render({"companies": companies}, request))


@login_required(login_url='/')
def search_report_content(request):
    if request.GET["company_id"] == "all":
        company = Company.objects.all().select_related('sector')
    else:
        company = Company.objects.select_related('sector').filter(id=request.GET["company_id"]).all()

    if request.GET["trimester_id"] == "all":
        trimesters = Trimester.objects.filter(trimester_begin__year=request.GET["year_value"]).all()
    else:
        trimesters = Trimester.objects.filter(id=request.GET["trimester_id"]).all()

    array_payments = []
    array_contributions = []
    for comp in company:
        for trimester in trimesters:
            payments = Payment.objects.filter(company=comp, trimester=trimester). \
                select_related('company').values('payment_amount', 'company_id')
            contributions = Contribution.objects.filter(company=comp, trimester=trimester). \
                select_related('company').values('total_amount', 'company_id')
            array_payments.append(list(payments))
            array_contributions.append(list(contributions))
    data = {
        'company': list(company.values('id', 'company_name', 'sector__sector_name')),
        'trimesters': list(trimesters.values()),
        "payments": array_payments,
        "contributions": array_contributions
    }
    return JsonResponse(data)


@login_required(login_url='/')
def user_list_view(request):
    template = loader.get_template('users/users-list.html')
    return HttpResponse(template.render({}, request))


@login_required(login_url='/')
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    serialized_data = serializer.data
    # print(serialized_data)
    return JsonResponse(serialized_data, safe=False)


@login_required(login_url='/')
def user_registration_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            if request.POST.get('role') == 'ACCOUNTANT':
                Accountant(username=username, first_name=first_name, last_name=last_name, email=email,
                           password=make_password(password)).save()
            elif request.POST.get('role') == 'MANAGER':
                Manager(username=username, first_name=first_name, last_name=last_name, email=email,
                        password=make_password(password)).save()
            else:
                form.save()
            return redirect(reverse("users"))
        else:
            print(form.errors.as_data())
    template = loader.get_template('users/users-add.html')
    form = UserRegistrationForm()
    return HttpResponse(template.render({"form": form}, request))


def analyse_view(request):
    template = loader.get_template('reports/analyses.html')
    return HttpResponse(template.render({}, request))
