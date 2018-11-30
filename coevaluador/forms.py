from django import forms


class LoginForm(forms.Form):
    rut = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs={
                              'id': 'input-user',
                              'class': 'form-control',
                              'placeholder': 'RUT',
                              'required': True,
                              'autofocus': True
                          }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'input-password',
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'required': True
    }))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'old_password',
        'class': 'form-control',
        'placeholder': 'Contraseña Antigua',
        'required': True,
        'autofocus': True
    }))

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'new_password',
        'class': 'form-control',
        'placeholder': 'Contraseña Nueva',
        'required': True
    }))

    rep_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'rep_password',
        'class': 'form-control',
        'placeholder': 'Contraseña Nueva',
        'required': True
    }))