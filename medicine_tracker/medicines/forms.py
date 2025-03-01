from django import forms


from .models import UserMedicine, Medicine, Comment, User
from .models import DOSAGE_CHOICES


class UserCreationForm:
    pass


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Přidali jsme password1 a password2


class UserMedicineForm(forms.ModelForm):
    medicine = forms.ModelChoiceField(
        queryset=Medicine.objects.all(),
        empty_label="Choose a medicine",
        label="Medicine"
    )
    dosage = forms.ChoiceField(
        choices=DOSAGE_CHOICES,
        label="Dávkování"
    )
    day = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Den"
    )
    time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Čas"
    )

    class Meta:
        model = UserMedicine
        fields = ['medicine', 'dosage', 'day', 'time', 'notes', 'remaining_doses']


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name',
            'manufacturer',
            'storage_temp',
            'side_effects',
        ]


class CommentForm(forms.ModelForm):
    medicine = forms.ModelChoiceField(queryset=None,
        empty_label="Vyberte lék",
        label="Lék"
    )

    class Meta:
        model = Comment
        fields = ['medicine', 'text']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }