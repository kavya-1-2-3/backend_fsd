from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AuthUser, Review 


# =================================================================
# 1. AUTHENTICATION FORM (CustomUserCreationForm)
# =================================================================
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label, 
            })

    class Meta:
        model = AuthUser
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AuthUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


# =================================================================
# 2. REVIEW FORM (ReviewForm)
# =================================================================
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (5, '★★★★★ (Excellent)'),
        (4, '★★★★☆ (Very Good)'),
        (3, '★★★☆☆ (Good)'),
        (2, '★★☆☆☆ (Fair)'),
        (1, '★☆☆☆☆ (Poor)'),
    )

    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        label='Your Rating',
        coerce=int   # ✅ ensures rating is saved as integer, not string
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': 'min-height: 100px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({
            'class': 'form-select',
            'style': 'min-width: 150px;'
        })
