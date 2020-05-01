"""
Project Definition of forms
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioSelect
import argon2, binascii

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["quizanswers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label =_('Password'),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))

hash = argon2.hash_password_raw(
    time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32,
    password=b'password', salt=b'some salt', type=argon2.low_level.Type.ID)
print("Argon2 raw hash:", binascii.hexlify(hash))

argon2Hasher = argon2.PasswordHasher(
    time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
hash = argon2Hasher.hash("password")
print("Argon2 hash (random salt):", hash)

verifyValid = argon2Hasher.verify(hash, "password")
print("Argon2 verify (correct password):", verifyValid)

try:
    argon2Hasher.verify(hash, "wrong123")
except:
    print("Argon2 verify (incorrect password):", False)
