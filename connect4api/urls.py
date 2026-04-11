from django.urls import path

from connect4api.views import NextMoveView

urlpatterns = [
    path('next_move/', NextMoveView.as_view(), name='next_move'),
]