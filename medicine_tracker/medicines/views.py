from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pytest


from .models import UserMedicine, MedicineHistory, Medicine
from .forms import UserMedicineForm, MedicineForm

@login_required
def medicine_list(request):
    """
       Displays the list of medicines for the logged-in user.

       This view retrieves all medicines that the user is taking.
       It also calculates the last time each medicine was taken and
       fetches the full history of medicine intake.

       Args:
           request (HttpRequest): The request object.

       Returns:
           HttpResponse: Renders 'medicine_list.html' with:
               - medicines: List of medicines the user is taking.
               - history: History of medicine intake.
       """
    medicines = UserMedicine.objects.filter(user=request.user)

    for med in medicines:
        last_dose = MedicineHistory.objects.filter(
            user_medicine=med
        ).order_by('-date').first()
        med.last_taken = last_dose.date.strftime('%d.%m.%Y %H:%M') if last_dose else None

    history = MedicineHistory.objects.filter(
        user_medicine__user=request.user
    ).order_by('-date')

    return render(request, 'medicines/medicine_list.html', {
        'medicines': medicines,
        'history': history
    })


@login_required
def delete_medicine(request, medicine_id):
    """
        Deletes a medicine entry from the logged-in user's list.

        This function retrieves the medicine entry for the current user and
        deletes it. If the medicine does not exist or does not belong to the user,
        it raises a 404 error.

        Args:
            request (HttpRequest): The request object.
            medicine_id (int): The ID of the medicine to be deleted.

        Returns:
            HttpResponseRedirect: Redirects to 'medicine_list'.
        """
    medicine = get_object_or_404(UserMedicine, id=medicine_id, user=request.user)
    medicine.delete()
    return redirect('medicine_list')


@login_required
def add_medicine(request):
    """
        Allows the logged-in user to add a new medicine to their personal list.

        If the request method is POST, the form is processed. If valid, a new
        UserMedicine entry is created and linked to the user.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse:
                - Redirects to 'medicine_list' if form submission is successful.
                - Renders 'add_medicine.html' with the form if request is GET or invalid.
        """
    if request.method == "POST":
        form = UserMedicineForm(request.POST)
        if form.is_valid():
            user_med = form.save(commit=False)
            user_med.user = request.user
            user_med.day = form.cleaned_data.get('day') or None
            user_med.time = form.cleaned_data.get('time') or None
            user_med.notes = form.cleaned_data.get('notes') or None
            user_med.save()
            return redirect('medicine_list')
    else:
        form = UserMedicineForm()

    return render(request, 'medicines/add_medicine.html', {'form': form})


@login_required
def take_dose(request, medicine_id):
    """
        Allows the user to take a dose of a specific medicine.

        Ensures that a user cannot take another dose within one hour of the last recorded dose.
        If a dose is available, it deducts one from the remaining doses and logs the intake in MedicineHistory.

        Args:
            request (HttpRequest): The request object.
            medicine_id (int): The ID of the medicine being taken.

        Returns:
            HttpResponseRedirect: Redirects to 'medicine_list'.
        """
    user_medicine = get_object_or_404(UserMedicine, id=medicine_id, user=request.user)


    if MedicineHistory.objects.filter(
        user_medicine=user_medicine,
        date__gt=now() - timedelta(hours=1)
    ).exists():
        messages.warning(request, " další dávku za hodinu.")
    else:

        if user_medicine.take_dose():
            MedicineHistory.objects.create(user_medicine=user_medicine)
            messages.success(request, "Dávka úspěšně odečtena.")

    return redirect('medicine_list')


@login_required
def medicine_history(request):
    """
        Displays the logged-in user's medicine intake history.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Renders 'medicine_history.html' with:
                - history: A list of the user's medicine intake records.
        """
    history = MedicineHistory.objects.filter(
        user_medicine__user=request.user
    ).order_by('-date')
    return render(request, 'medicines/medicine_history.html', {'history': history})


@login_required
def medicine_selection(request):
    """
        Displays a list of all available medicines.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Renders 'medicine_selection.html' with:
                - medicines: A list of all available medicines.
        """
    medicines = Medicine.objects.all()
    return render(request, 'medicines/medicine_selection.html', {'medicines': medicines})


@login_required
def home_redirect(request):
    """
        Redirects the user to the medicine list page.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponseRedirect: Redirects the user to 'medicine_list'.
        """
    return redirect('medicine_list')


@login_required
def add_new_medicine(request):
    """
        Allows the user to add a new medicine to the database.

        This view handles the creation of new medicine entries. If the request
        method is POST and the form is valid, the new medicine is saved to the
        database.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse:
                - Redirects to 'add_medicine' if the form submission is successful.
                - Renders 'add_new_medicine.html' with the form if the request method is GET or invalid.
        """
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_medicine')
    else:
        form = MedicineForm()

    return render(request, 'medicines/add_new_medicine.html', {'form': form})


@login_required
def edit_medicine(request, medicine_id):
    """
        Allows the logged-in user to edit an existing medicine entry.

        If the request method is POST and the form is valid, the changes are saved,
        and the user is redirected to the 'medicine_list' page.

        Args:
            request (HttpRequest): The request object.
            medicine_id (int): The ID of the medicine entry to be edited.

        Returns:
            HttpResponse:
                - Redirects to 'medicine_list' if the form submission is successful.
                - Renders 'edit_medicine.html' with the form if the request method is GET or invalid.
        """
    medicine = get_object_or_404(UserMedicine, id=medicine_id, user=request.user)

    if request.method == "POST":
        form = UserMedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = UserMedicineForm(instance=medicine)

    return render(request, 'medicines/edit_medicine.html', {'form': form})


@login_required
def medicine_detail(request, medicine_id):
    """
        Displays detailed information about a specific medicine.

        Args:
            request (HttpRequest): The request object.
            medicine_id (int): The ID of the medicine.

        Returns:
            HttpResponse: Renders 'medicine_detail.html' with:
                - medicine: The selected medicine details.
        """
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, 'medicines/medicine_detail.html', {'medicine': medicine})


