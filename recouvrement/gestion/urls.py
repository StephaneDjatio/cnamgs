from django.urls import path
from . import views


urlpatterns = [
    path('', views.connect_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('map/', views.index, name='index'),
    path('users/', views.user_list_view, name='users'),
    path('get_users/', views.get_users, name='get_users'),
    path('users/add', views.user_registration_view, name='users_add'),

    path('provinces/', views.province_view, name='provinces'),
    path('provinces/create/', views.province_create, name='provinces_create'),

    path('departements/', views.department_view, name='departements'),
    path('departements/create/', views.department_create, name='departements_create'),

    path('villes/', views.city_view, name='villes'),
    path('villes/create/', views.city_create, name='villes_create'),

    path('secteurs/', views.sector_view, name='secteurs'),
    path('secteurs/create/', views.sector_create, name='secteurs_create'),

    path('questions/', views.question_view, name='questions'),
    path('questions/create/', views.question_create, name='questions_create'),

    path('getTrimesters/', views.get_trimesters_view, name='getTrimesters'),
    path('getTrimestersUnsolvePerYear/', views.getTrimestersUnsolvePerYear, name='getTrimestersUnsolvePerYear'),
    path('selectTrimesterContributionPayment/', views.selectTrimesterContributionPayment, name='selectTrimesterContributionPayment'),
    path('getCompany/', views.get_company_per_year, name='getCompany'),
    path('getCompanyDetail/', views.get_company_detail_from_map, name='getCompanyDetail'),
    path('companies/', views.company_view, name='companies'),
    path('company/add/', views.add_company, name='add_company'),
    path('company/edit/', views.edit_company, name='edit_company'),
    path('companies/delete/', views.delete_company, name='delete_company'),
    path('companies/company-contact/', views.add_company_contact, name='add_company_contact'),
    path('companies/update_company/', views.update_company, name='update_company'),
    path('companies/updateLocalization/', views.update_localization, name='updateLocalization'),
    path('company/getLocation/', views.get_company_location, name='get_company_location'),
    path('companies/contributions/<int:company_id>', views.list_company_contributions, name='list_company_contributions'),
    path('contributions/<int:company_id>', views.get_company_contributions, name='get_company_contributions'),
    path('agents/', views.agent_view, name='agents'),
    path('agent/add/', views.add_agent, name='add_agent'),
    path('agent/edit/', views.get_agent, name='get_agent'),
    path('agents/account/', views.get_agent_account, name='agent_account'),
    path('agents/update_agent/', views.update_agent, name='update_agent'),
    path('missions/', views.mission_view, name='missions'),
    path('missions/add/', views.add_mission, name='add_mission'),
    path('payments/', views.payment_view, name='payments'),
    path('load_payments/', views.load_payments, name='load_payments'),
    path('load_payment/', views.load_payment, name='load_payment'),
    path('payments/details/<int:company_id>/<int:trimester_id>', views.detail_payment_view, name='payments_details'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/save/', views.save_payment, name='save_payment'),
    path('inspections/', views.inspection_view, name='inspections'),
    path('inspections/<int:inspection_id>', views.inspection_detail_view, name='inspection_detail'),
    path('reports/', views.report_view, name='reports'),
    path('search_report_content/', views.search_report_content, name='search_report_content'),
    path('analyses/', views.analyse_view, name='analyse_view'),
    path('import_export/', views.importExport_view, name='import_export'),
    path('get_payment_per_sector/', views.getTotalPaymentsBySector, name='get_payment_per_sector'),
    path('get_contribution_payment_per_sector/', views.getTotalContributionsAndPaymentsBySector, name='get_contribution_payment_per_sector'),
]
