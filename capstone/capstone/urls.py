from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from capstoneapi.views import register_user, login_user, WorkflowViewSet, UserViewSet, CompanyViewSet, StateViewSet, StatusViewSet, NoteViewSet
from django.conf.urls.static import static
from django.conf import settings


"""Router"""
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'workflows', WorkflowViewSet, 'workflow')
router.register(r'users', UserViewSet, 'user')
router.register(r'companies', CompanyViewSet, 'company')
router.register(r'states', StateViewSet, 'state')
router.register(r'statuses', StatusViewSet, 'status')
router.register(r'notes', NoteViewSet, 'note')



urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)