from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api.views import GetUser, registration_view, logout_view, signup, verifyuser


urlpatterns = [
    path('login/', obtain_auth_token, name='login'), 
    path('register/', registration_view, name='register'), 
    path('logout/', logout_view, name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',signup,name='signup'),
    path('verifyuser/',verifyuser,name='verifyuser'),
    path('getuser/',GetUser.as_view(),name='getuser')
 
]    