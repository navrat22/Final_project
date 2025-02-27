import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

from medicines.models import UserMedicine, MedicineHistory, Medicine


@pytest.mark.django_db
def test_take_dose_too_soon(client):
    # Vytvoření testovacího uživatele
    user = User.objects.create_user(username="testuser", password="testpassword")
    client.login(username="testuser", password="testpassword")

    # Vytvoření instance léku
    medicine = Medicine.objects.create(name="Paralen")  # Správně vytváříme lék

    # Vytvoření záznamu UserMedicine (přiřazení léku k uživateli)
    user_medicine = UserMedicine.objects.create(user=user, medicine=medicine, remaining_doses=5)

    # Simulace užití dávky v historii
    MedicineHistory.objects.create(user=user, medicine=user_medicine, taken_at=now())

    # Odeslání POST požadavku na užití další dávky
    url = reverse("take_dose", args=[user_medicine.id])
    response = client.post(url)

    # Obnovíme data z databáze
    user_medicine.refresh_from_db()

    # Ověření, že dávka nebyla odebrána (uživatel ji vzal před méně než 1 hodinou)
    assert user_medicine.remaining_doses == 5
    assert response.status_code == 302  # Očekáváme přesměrování


@pytest.mark.django_db
def test_take_dose_unauthenticated(client):
    """Testuje, zda nepřihlášený uživatel nemůže užít dávku."""
    medicine = UserMedicine.objects.create(name="Paralen", remaining_doses=5)
    url = reverse("take_dose", args=[medicine.id])

    response = client.post(url)

    assert response.status_code == 302