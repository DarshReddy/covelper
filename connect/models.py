from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, phone, name, password=None):
        if not phone:
            raise ValueError('Users must have an phone')

        user = self.model(
            name = name,
            phone = phone
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone=phone,
            name=name,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
  name = models.CharField(max_length=32)
  phone = models.CharField(max_length=32,unique=True,primary_key=True)
  is_doc = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = MyUserManager()

  USERNAME_FIELD = 'phone'
  REQUIRED_FIELDS = ['name']

  def __str__(self):
        return self.name

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return True

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin

class Patient(models.Model):
  pat = models.OneToOneField(MyUser, on_delete=models.CASCADE)
  bed_no = models.IntegerField()
  age = models.IntegerField()

class HealthWorker(models.Model):
  doc = models.OneToOneField(MyUser, on_delete=models.CASCADE)
  is_free = models.BooleanField(default=True)
  is_doc = models.BooleanField(default=False)
  req_cnt = models.IntegerField(default=0)

class Request(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  hworker = models.ForeignKey(HealthWorker, on_delete=models.CASCADE, null=True)
  is_done = models.BooleanField(default=False)
  is_critical = models.BooleanField(default=False)
  req_at = models.DateTimeField(auto_now=True)