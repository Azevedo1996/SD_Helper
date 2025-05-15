from django.urls import path
from .views import IndexView, FlowView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:aplicacao>/', FlowView.as_view(), name='flow_inicio'),
    path('<str:aplicacao>/<str:node_id>/', FlowView.as_view(), name='flow'),
]