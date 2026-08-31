from django.urls import path

from .views import (
    ContactAdminDetailView,
    ContactAdminListView,
    ContactMessageCreateView,
    NewsletterSubscribeView,
    NewsletterUnsubscribeView,
)

urlpatterns = [
    path('', ContactMessageCreateView.as_view(), name='contact-create'),
    path('admin/', ContactAdminListView.as_view(), name='contact-admin-list'),
    path('admin/<int:pk>/', ContactAdminDetailView.as_view(), name='contact-admin-detail'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('newsletter/unsubscribe/', NewsletterUnsubscribeView.as_view(), name='newsletter-unsubscribe'),
]
