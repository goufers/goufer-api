from rest_framework import status
import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestCreateCategory:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        
        response = api_client.post('/api/v1/main/categories/', {'category_name': 'Entertainment', 'Description': 'Entertainment Description'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
    def test_if_user_is_not_admin_returns_403(self, api_client):
        
        api_client.force_authenticate(user=User(is_staff=False))
        
        response = api_client.post('/api/v1/main/categories/', {'category_name': 'Entertainment', 'Description': 'Entertainment Description'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_user_is_admin_but_sends_invalid_data_returns_400(self, api_client):
        
        api_client.force_authenticate(user=User(is_staff=True))
        
        response = api_client.post('/api/v1/main/categories/', {})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_if_user_is_admin_and_sends_valid_data_returns_201(self, api_client):
        
        api_client.force_authenticate(user=User(is_staff=True))
        
        response = api_client.post('/api/v1/main/categories/', {'category_name': 'Entertainment', 'description': 'Entertainment Description', 'created_at': '2024-05-30T22:30:57.768126Z'})
        
        assert response.status_code == status.HTTP_201_CREATED