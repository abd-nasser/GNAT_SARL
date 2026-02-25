from django import forms

from auth_app.models import Personnel

class PersonnelRegisterForm(forms.Form):
    date_de_naissance = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date"})
    )
    
    class Meta:
        model = Personnel
        fields = [
            "first_name",
            "last_name",
            'email',
            "post",
            "telephone",
            'date_de_naissance',
            "lieu_de_naissance",
            "personne_a_prevenir_en_cas",
        ]
        


class ChangeCredentialsForm(forms.Form):
    new_username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class":"input input-bordered w-300"}),
        label="Nouveau nom d'utilisateur"
    )
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"input input-bordered w-300"}),
        label="Mot de passe actuel"
    )
    
    new_password = forms.CharField(
        widget = forms.PasswordInput(attrs={"class":"input input-bordered w-300"}),
        required= True,
        label="Nouveau mot de passe"
    )
    
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"input input-bordered w-300"}),
        required= True,
        label="Confirmez nouveau mot de passe "
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    def clean(self):
       cleaned_data = super().clean()    
       current_password = cleaned_data.get('current_password')
       new_password = cleaned_data.get('new_password')
       confirm_new_password = cleaned_data.get("confirm_new_password")
       
       #Verification du mot de passe actuel
       if not self.user.check_password(current_password):
           raise forms.ValidationError("mot de passe actuel incorrect")
       
       #correspondance de mot de passe 
       if new_password and new_password != confirm_new_password:
           raise forms.ValidationError("Les nouveaux mot de passe de correspondent pas")
       
       return cleaned_data


