from django.conf.urls import url, include

from budget import api_views
from budget import views

api_urlpatterns = [
    url(r'^latest.json$', api_views.latest_as_json),
    url(r'^add/(?P<year>.+)/$', api_views.add_budget)
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns), name='budget-api-latest'),
    url(r'^overview/$', views.budget_overview, name='budget-overview'),
]
