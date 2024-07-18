from django.db.models.signals import pre_save
from django.contrib.auth.models import User

def updateUser(sender,instance,**kwargs):
    #print('signal Triggered')
    user=instance #here instance will be userModelbecause we gave sender=UserModel  instance is the actual object of the model that is about to be saved or updated. It contains all the fields and data for that particular model instance. For example, if a new user is being created with specific details, instance will hold these details during the signal processing.
    if user.email !='':
        user.username=user.email
        
        
        
pre_save.connect(updateUser,sender=User) #updateuser will be called whem we save the data i.e in admin website sender: The model class that sent the signal. In this case, it will be the User model.
