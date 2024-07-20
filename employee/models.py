import datetime
from employee.utility import code_format
from django.db import models
from employee.managers import EmployeeManager
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import django.contrib.auth.base_user as auth_base
from django.utils.translation import gettext as _


# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class UserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, username, password=None):
#         if not email:
#             raise ValueError('User requires an email address')
#         # if not username:
#         #     raise ValueError('User requires a username')
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             username=username,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, username, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             username=username,
#             password=password,
#         )
#         user.is_admin = True
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True  # Set is_superuser to True for superusers
#         user.save(using=self._db)
#         return user


# class CustomUser(AbstractUser): #auth_base.AbstractBaseUser
#     HR = 1
#     SUPERVISOR = 2
#     USER = 3

#     ROLE_CHOICES = (
#         (HR, 'hr'),
#         (SUPERVISOR, 'supervisor'),
#         (USER, 'user'),
#     )
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=100)
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

#     # Required fields
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)
#     created_date = models.DateField(auto_now_add=True)
#     modified_date = models.DateField(auto_now=True)
#     is_active = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     def __str__(self):
#         return self.email

# def has_perm(self, perm, obj=None):
#     return self.is_admin

# def has_module_perms(self, app_label):
#     return True

# def get_all_permissions(self):
#     return self.user_permissions.all()

# def save(self, *args, **kwargs):
#     # Assign the appropriate role based on the selected value
#     if self.role == CustomUser.HR:
#         self.is_admin = True
#         self.is_superuser = True
#         self.is_staff = True
#         self.is_active = True
#     elif self.role == CustomUser.SUPERVISOR:
#         self.is_staff = True
#     else:
#         self.is_staff = False
#     super().save(*args, **kwargs)


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    # supervisor_role = Role.objects.create(name='Supervisor', description='Role for supervisors')

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125, null=True, blank=True)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ['name', 'created']

    def __str__(self):
        return self.name


class Employee(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Prefer not to say'

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        (NOT_KNOWN, 'Prefer not to say'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MSS, 'Mss'),
        (DR, 'Dr'),
        (SIR, 'Sir'),
        (MADAM, 'Madam'),
    )

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERN, 'Intern'),
    )

    # PERSONAL DATA

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    image = models.FileField(_('Profile Image'), upload_to='profiles', default='default.png', blank=True, null=True,
                             help_text='upload image size less than 2.0MB')  # work on path username-date/image
    firstname = models.CharField(_('Firstname'), max_length=250, null=False, blank=False)
    lastname = models.CharField(_('Lastname'), max_length=250, null=False, blank=False)
    othername = models.CharField(_('Othername (optional)'), max_length=250, null=True, blank=True)
    birthday = models.DateField(_('Birthday'), blank=False, null=False)
    designation = models.ForeignKey(Department, verbose_name=_('Designation'), on_delete=models.SET_NULL, null=True,
                                    default=None)

    role = models.ForeignKey(Role, verbose_name=_('Role'), on_delete=models.SET_NULL, null=True, default=None)
    startdate = models.DateField(_('Employement Date'), help_text='date of employement', blank=False, null=True)
    employeetype = models.CharField(_('Employee Type'), max_length=115, default=FULL_TIME, choices=EMPLOYEETYPE,
                                    blank=False, null=True)
    peronal_number = models.CharField(_('Personal Number'), max_length=100, null=True, blank=True)
    dateissued = models.DateField(_('Date Issued'), help_text='date staff id was issued', blank=False, null=True)

    # app related
    is_blocked = models.BooleanField(_('Is Blocked'), help_text='button to toggle employee block and unblock',
                                     default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='button to toggle employee deleted and undelete',
                                     default=False)

    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True, null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now=True, null=True)

    # PLUG MANAGERS
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    from datetime import timedelta
    @property
    def get_full_name(self):
        if self.othername:
            return f"{self.firstname} {self.lastname} {self.othername}"
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return self.get_full_name
    # @property
    # def get_full_name(self):
    #     fullname = ''
    #     firstname = self.firstname
    #     lastname = self.lastname
    #     othername = self.othername
    #
    #     if (firstname and lastname) or othername is None:
    #         fullname = firstname + ' ' + lastname
    #         return fullname
    #     elif othername:
    #         fullname = firstname + ' ' + lastname + ' ' + othername
    #         return fullname
    #     return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return

    @property
    def can_apply_leave(self):
        pass

    def save(self, *args, **kwargs):
        get_id = self.peronal_number  # grab employee_id number from submitted form field
        data = code_format(get_id)
        self.personal_number = data  # pass the new code to the employee_id as its orifinal or actual code
        super().save(*args, **kwargs)  # call the parent save method
        # print(self.peronal_number)
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

class Family(models.Model):
    STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)
    spouse = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    children = models.IntegerField(default=0)
    nextofkin = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    father = models.CharField(max_length=100, blank=True)
    foccupation = models.CharField(max_length=100, blank=True)
    mother = models.CharField(max_length=100, blank=True)
    moccupation = models.CharField(max_length=100, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Family information of {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

class Emergency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Assuming you have an Employee model
    fullname = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Emergency information of {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Assuming you have an Employee model
    name = models.CharField(max_length=100, blank=True)
    account = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=255, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bank account information of {self.user.username}"
