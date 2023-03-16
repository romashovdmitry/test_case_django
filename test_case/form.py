from django.forms import Form, CharField, TextInput


class PhoneNumber(Form):
    phone_number = CharField(
        widget=TextInput(
            attrs={
                'type': 'number',
                'placeholder': '9992024611'
            }
        )
    )
