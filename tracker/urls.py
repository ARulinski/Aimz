from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("aimz", views.aimz, name="aimz"),
    path("dash", views.dash, name="dash"),
    path("update_challenge/<challenge_id>", views.update_challenge, name="update_challenge"),
    path("delete_challenge/<challenge_id>", views.delete_challenge, name="delete_challenge"),
    path("delete_challenge_index/<challenge_id>", views.delete_challenge_index, name="delete_challenge_index"),
    path("status/<challenge_id>", views.status, name="status"),
    path("Dchallenge", views.Dchallenge, name="Dchallenge"),
    path("phone_verification", views.phone_verification, name="phone_verification"),
    path("verify_code", views.verify_code, name="verify_code"),
    path("notificaions", views.notifications, name="notifications"),
]

