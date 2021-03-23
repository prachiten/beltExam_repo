from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.create_user),
    path('login',views.login),
    path('logout',views.logout),
    path('main',views.main),
    path('org/create',views.create_organization),
    path('org/delete/<int:org_id>',views.delete),
    path('org/display_details/<int:org_id>',views.display_details),
    path('org/join_group/<int:org_id>',views.join_group),
    path('org/leave_group/<int:org_id>',views.leave_group),
]