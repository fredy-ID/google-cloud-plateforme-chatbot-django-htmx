from django.urls import path

from . import views

app_name = "subjects"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:subject_id>/vote/", views.vote, name="vote"),
]