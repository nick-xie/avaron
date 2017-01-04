from django import forms
class PlayerForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    game = forms.IntegerField()
    role = forms.BooleanField()

    def clean_role(self): #validation check
    	data=self.cleaned_data['role']
    	if data>1:
    		raise ValidationError(_('Invalid role - Must be 1 or 0'))
    	return data