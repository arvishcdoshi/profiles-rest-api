from django.urls import path, include

from rest_framework.routers import DefaultRouter  # router is a class provided by the Django-restframework in order to generate the different routes that are available for our view set

from profiles_api import views


router = DefaultRouter()

router.register('hello_viewset',views.HelloViewSet,base_name="hello-viewset") #last argument(base_name) is used for retrieving the url's
                                                                               #in our router if we ever need to do that using the url
                                                                               # retrieving function provided by the Django...
# we don't use forward slash '/' after hello_viewset because routers will create all 4 url's for us,

router.register('profile',views.UserProfileViewset)
router.register('feed',views.UserProfileFeedViewSet)

urlpatterns = [


   path('hello_view',views.HelloApiView.as_view()),
   path('login/',views.UserLoginApiView.as_view()),
   path('',include(router.urls))

]
