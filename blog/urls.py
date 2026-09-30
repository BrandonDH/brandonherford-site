from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="list"),
    # Must come before the slug route so it isn't swallowed as a post slug.
    path("martor/uploader/", views.martor_uploader, name="martor_uploader"),
    path("<slug:slug>/", views.post_detail, name="detail"),
]
