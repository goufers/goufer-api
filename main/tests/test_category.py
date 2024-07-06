from rest_framework import status
import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from main.models import Category

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
        
        response = api_client.post('/api/v1/main/categories/', {'category_name': 'entertainment', 'description': 'Entertainment Description', 'created_at': '2024-05-30T22:30:57.768126Z'})
        
        assert response.status_code == status.HTTP_201_CREATED
    
@pytest.mark.django_db
class TestGetCategroyList:
    def test_get_category_list_returns_200(self, api_client):
        
        baker.make(Category, _quantity=50)
        
        response = api_client.get('/api/v1/main/categories/')
        
        assert response.status_code == status.HTTP_200_OK
        
        
class TestRetriveCategory:
    pass
        
     
        
@pytest.mark.django_db
class TestUpdateCategory:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        
        category = baker.make(Category)
        
        response = api_client.put(f'/api/v1/main/categories/{category.id}/', {})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        
        
    def test_if_user_is_not_admin_returns_403(self, api_client):
        
        api_client.force_authenticate(user=User(is_staff=False))
        category = baker.make(Category)
        
        response = api_client.put(f'/api/v1/main/categories/{category.id}/', {})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_user_is_admin_but_sends_invalid_data_for_update_returns_400(self, api_client):
        
        api_client.force_authenticate(user=User(is_staff=True))
        category = baker.make(Category)
        
        response = api_client.put(f'/api/v1/main/categories/{category.id}/', {})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        

    def test_if_user_is_admin_and_sends_valid_data_returns_200(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))
        category = baker.make(Category)
        
        response = api_client.put(f'/api/v1/main/categories/{category.id}/', {'category_name': 'entertainment', 'description': 'Entertainment Description', 'created_at': '2024-05-30T22:30:57.768126Z'})
        
        assert response.status_code == status.HTTP_200_OK
        
        

    
        