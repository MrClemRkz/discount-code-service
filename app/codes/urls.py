from django.urls import path

from codes import views


urlpatterns = [path("generate/<int:count>", views.CodeAction.as_view())]
