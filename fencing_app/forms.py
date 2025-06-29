from django import forms

class PoseAnalysisForm(forms.Form):
    POSE_CHOICES = [
        ('en_garde', 'En Garde'),
        ('lunge', 'Lunge'),
    ]
    
    pose_type = forms.ChoiceField(
        choices=POSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    ) 