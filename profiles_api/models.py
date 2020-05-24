from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings





class UserProfileManager(BaseUserManager):
    """Manager for users profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name) #Crea un nuevo model object y le da email y name
        
        user.set_password(password) #Hacemos esto porque la password esta encriptada
        user.save(using=self._db) # Para guardar el user model en la base de datos

        return user   # devuelve la creacion del user


    def create_superuser(self, email, name, password):
        """ Create a new superuser"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


#Este model aparece en adminsite dentro de la app profiles_api
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email=models.EmailField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)
    #Para determinar si un usuario esta activo
    is_staff=models.BooleanField(default=False)
    #Para determinar si el usuario es un staff y tiene acceso al admin site

    objects = UserProfileManager()

    USERNAME_FIELD='email' #PARA AUTENTICAR EN VEZ DE PEDIR USERNAME PIDE EMAIL
    REQUIRED_FIELDS= ['name'] 

    def get_full_name(self):
        """Retrieve Full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve Short name of user"""
        return self.name
    
    def __str__(self):
        """ return string representation of our user"""
        return self.email



class ProfileFeedItem(models.Model):
    """Profile status update"""
    #Este model aparece en adminsite dentro de la app profiles_api
    user_profile= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """Return the model as a string"""
        return self.status_text
    
