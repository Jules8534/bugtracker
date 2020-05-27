from django import forms


class LogInForm(forms.Form):
    username = forms.CharField(
        max_length=150
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class NewCustomUser(forms.Form):
    username = forms.CharField(
        max_length=150
        )
    password = forms.CharField(
        widget=forms.PasswordInput()
        )
    display_name = forms.CharField(
        max_length=150
        )
    first_name = forms.CharField(
        max_length=30
        )
    last_name = forms.CharField(
        max_length=150
        )
    email = forms.EmailField()

class SubmitTicket(forms.Form):
    title = forms.CharField(
        max_length=200
    )
    description = forms.CharField(
        widget=forms.Textarea
    )