import pytest
from medicines.models import Medicine, UserMedicine, MedicineHistory, MedicineInteraction


@pytest.mark.django_db
def test_take_dose():

    medicine = Medicine.objects.create(remaining_doses=1)

    assert medicine.take_dose() is True
    medicine.refresh_from_db()
    assert medicine.remaining_doses == 0

    assert medicine.take_dose() is False
    medicine.refresh_from_db()
    assert medicine.remaining_doses == 0


@pytest.mark.django_db
def test_medicine_history_str():
    user_medicine = UserMedicine.objects.create(name="TestLek")

    history = MedicineHistory.objects.create(user_medicine=user_medicine)

    history_str = str(history)

    assert "Historie užití:" in history_str
    assert str(user_medicine) in history_str
    assert "dne" in history_str




@pytest.mark.django_db
def test_medicine_interaction_str():

    med1 = Medicine.objects.create(name="Lék A")
    med2 = Medicine.objects.create(name="Lék B")

    interaction = MedicineInteraction.objects.create(description="Popis interakce")

    interaction.medicines.add(med1, med2)

    interaction_str = str(interaction)

    assert "Lék A" in interaction_str
    assert "Lék B" in interaction_str
