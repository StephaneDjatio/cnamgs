import threading
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create a thread-local object to store custom data
thread_local_data = threading.local()


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        MANAGER = "MANAGER", "Manager"
        AGENT = "AGENT", "Agent"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class Agent(models.Model):
    registration_number = models.CharField(max_length=10)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150)
    phone_number = models.IntegerField(null=True)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstname


class AccountantManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ACCOUNTANT)


class Accountant(User):
    base_role = User.Role.ACCOUNTANT

    accountant = AccountantManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for accountants"

    def save(self, *args, **kwargs):
        # Do something with the kwargs if needed
        agent_id = kwargs.pop('agent_id', None)

        # Set custom data in thread-local storage
        thread_local_data.agent_id = agent_id

        return super(Accountant, self).save(*args, **kwargs)


@receiver(post_save, sender=Accountant)
def create_user_profile(sender, instance, created, **kwargs):
    agent_id = getattr(thread_local_data, 'agent_id', None)
    if created and instance.role == "ACCOUNTANT":
        AccountantProfile.objects.create(user=instance, agent_id=agent_id)


class AccountantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)


class ManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MANAGER)


class Manager(User):
    base_role = User.Role.MANAGER

    manager = ManagerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for managers"

    def save(self, *args, **kwargs):
        # Do something with the kwargs if needed
        agent_id = kwargs.pop('agent_id', None)

        # Set custom data in thread-local storage
        thread_local_data.agent_id = agent_id

        return super(Manager, self).save(*args, **kwargs)


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)


@receiver(post_save, sender=Manager)
def create_user_profile(sender, instance, created, **kwargs):
    agent_id = getattr(thread_local_data, 'agent_id', None)
    if created and instance.role == "MANAGER":
        ManagerProfile.objects.create(user=instance, agent_id=agent_id)


class AgentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.AGENT)


class AgentUser(User):
    base_role = User.Role.AGENT

    agent = AgentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for agents"

    def save(self, *args, **kwargs):
        # Do something with the kwargs if needed
        agent_id = kwargs.pop('agent_id', None)

        # Set custom data in thread-local storage
        thread_local_data.agent_id = agent_id

        return super(AgentUser, self).save(*args, **kwargs)


class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)


@receiver(post_save, sender=AgentUser)
def create_user_profile(sender, instance, created, **kwargs):
    agent_id = getattr(thread_local_data, 'agent_id', None)
    if created and instance.role == "AGENT":
        AgentProfile.objects.create(user=instance, agent_id=agent_id)


class Sector(models.Model):
    sector_name = models.CharField(max_length=255)
    sector_description = models.CharField(max_length=255, null=True)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sector_name


class Province(models.Model):
    province_name = models.CharField(max_length=255)
    create_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.province_name


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


class City(models.Model):
    city_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.city_name


class Contact(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return self.firstname


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.company_name


class Localization(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)


class Trimester(models.Model):
    trimester_begin = models.DateField()
    trimester_end = models.DateField()
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.trimester_begin.strftime('%d/%m/%Y') + ' to ' + self.trimester_end.strftime('%d/%m/%Y')


class Contribution(models.Model):
    total_amount = models.FloatField(default=0.0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    trimester = models.ForeignKey(Trimester, on_delete=models.CASCADE)


class Payment(models.Model):
    payment_number = models.CharField(max_length=10, default="null")
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.FloatField(default=0.0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    trimester = models.ForeignKey(Trimester, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)


class PaymentFiles(models.Model):
    filename = models.CharField(max_length=100, blank=True)
    filetype = models.CharField(max_length=10, blank=True)
    file = models.FileField(upload_to='%Y/%m/%d')
    create_on = models.DateTimeField(auto_now_add=True)


class Mission(models.Model):
    mission_order_number = models.CharField(max_length=15)
    mission_date = models.DateField()
    mission_objective = models.TextField(null=True, max_length=500)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mission_order_number


class AgentAppointedMission(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)


class CompanyAppointedMission(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)


class Inspect(models.Model):
    inspection_date = models.DateField(auto_now_add=True)
    inspection_report = models.TextField(max_length=500, null=True)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    create_on = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    question = models.TextField(max_length=500)
    selectedValue = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, null=True)


class ValidAnswer(models.Model):
    inspect = models.ForeignKey(Inspect, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=255, null=True)
