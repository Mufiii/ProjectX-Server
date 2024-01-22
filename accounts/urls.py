from django.urls import path

from accounts import views

urlpatterns = [
    path("register/", views.DeveloperRegistrationAPIView.as_view(), name="register"),
    path("verifyotp/", views.VerifyOtp.as_view(), name="verifyotp"),
    path("hire_talent/", views.VendorRegistrationView.as_view(), name="hire_talent"),
    path("email_verify/", views.VerifyEmail.as_view(), name="email_verify"),
    path("login/", views.UserLoginRequestAPIView.as_view(), name="login"),
    path("otpverify/", views.LoginOtpverification.as_view(), name="loginotp"),
]
