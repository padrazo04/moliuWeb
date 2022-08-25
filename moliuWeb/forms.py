from django import forms
from .models import Activity, Game, Posture
from django.contrib.auth import forms as authForms
from django.core.exceptions import ValidationError
from django.conf import settings
import magic
import os


class LoginForm(authForms.AuthenticationForm):
    username = authForms.UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "class": "form-control", "placeholder": "Usuario"}
        )
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Contraseña",
            }
        ),
    )


class AddActivity(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddActivity, self).__init__(*args, **kwargs)

        self.fields["background"] = forms.CharField(max_length=255)
        self.fields["background"].widget = forms.TextInput(
            attrs={"class": "form-control", "style": "display: none;"}
        )

    class Meta:
        model = Activity
        fields = ["name", "description", "points"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la actividad"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Descripción de la actividad"}
            ),
            "points": forms.Textarea(attrs={"class": "form-control", "style": "display: none;"}),
        }


class ImportGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["video", "joints"]
        widgets = {
            "video": forms.ClearableFileInput(
                attrs={"class": "custom-file-input", "style": "cursor: pointer;"}
            ),
            "joints": forms.ClearableFileInput(
                attrs={"class": "custom-file-input", "style": "cursor: pointer;"}
            ),
        }

    def clean_video(self):
        data = self.cleaned_data["video"]
        if magic.from_buffer(data.read(2048), mime=True) != "video/x-msvideo":
            raise (ValidationError('El archivo de la partida debe ser ".avi"'))
        return data

    def clean_joints(self):
        data = self.cleaned_data["joints"]
        if magic.from_buffer(data.read(2048), mime=True) != "text/plain":
            raise (ValidationError('El archivo de los joints debe ser ".txt"'))
        return data


class ClassifyPosture(forms.ModelForm):
    class Meta:
        model = Posture
        fields = "__all__"
        widgets = {
            "score": forms.Select(attrs={"style": "display:none"}),
            "game": forms.Select(attrs={"style": "display:none"}),
            "image": forms.TextInput(attrs={"style": "display:none"}),
            "isScored": forms.CheckboxInput(attrs={"style": "display:none"}),
        }


class CreateTrainingSet(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateTrainingSet, self).__init__(*args, **kwargs)
        games = Game.objects.all()

        for game in games:
            exportedDataDir = os.path.join(
                settings.MEDIA_ROOT, "games", game.directoryName, "exportedData"
            )
            if os.path.isdir(exportedDataDir) and os.listdir(exportedDataDir):
                dataFiles = sorted(os.listdir(exportedDataDir))
                dataFiles.insert(0, "No usar")
                dataFilesChoices = [(file, file) for file in dataFiles]

                self.fields[game.directoryName] = forms.ChoiceField()
                self.fields[game.directoryName].widget = forms.Select(
                    attrs={"class": "form-control"}
                )
                self.fields[game.directoryName].choices = dataFilesChoices
