from django.contrib import admin

from profiles_api import models


admin.site.register(models.UserProfile)
#Dice a django admin  que registre un user profile model con el admin site
# Y lo haga posible acceder desde el admin interface

admin.site.register(models.ProfileFeedItem)




