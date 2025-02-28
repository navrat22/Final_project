import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from medicines.models import Medicine


@pytest.mark.django_db
def test_add_new_medicine_view_post_valid(client):

    user = User.objects.create_user(username='testuser3', password='testpassword3')
    client.force_login(user)

    form_data = {
        'name': 'TestLék'

    }

    url = reverse('add_new_medicine')
    response = client.post(url, data=form_data)

    assert response.status_code == 302

    expected_url = reverse('add_medicine')
    assert response.url == expected_url

    from medicines.models import Medicine
    assert Medicine.objects.filter(name='TestLék').exists()



@pytest.mark.django_db
def test_medicine_detail_view(client):

    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_login(user)
    medicine = Medicine.objects.create(name="TestLék")
    url = reverse('medicine_detail', kwargs={'medicine_id': medicine.id})
    response = client.get(url)

    assert response.status_code == 200
    assert 'medicine' in response.context
    assert response.context['medicine'] == medicine


@pytest.mark.django_db
def test_medicine_selection_view(client):

    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_login(user)

    med1 = Medicine.objects.create(name="Lék A")
    med2 = Medicine.objects.create(name="Lék B")

    url = reverse('medicine_selection')
    response = client.get(url)
    assert response.status_code == 200
    assert 'medicines' in response.context

    medicines = list(response.context['medicines'])
    assert med1 in medicines
    assert med2 in medicines