from django import forms
from .models import Consulta


class Paso0Form(forms.Form):
    """Paso 0: Seleccion del rol."""
    modo = forms.ChoiceField(
        choices=Consulta.MODO_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-radio"}),
        initial="autoconsulta",
    )


DURACION_CHOICES = [
    ("", "— selecciona —"),
    ("agudo", "Agudo (menos de 2 semanas)"),
    ("subagudo", "Subagudo (2 a 6 semanas)"),
    ("cronico", "Crónico (más de 6 semanas)"),
]

ALARMA_CHOICES = [
    ("fiebre_alta", "Fiebre alta (>38.5°C)"),
    ("perdida_peso", "Pérdida de peso inexplicable"),
    ("sangrado", "Sangrado inusual"),
    ("dolor_torax", "Dolor en el pecho o dificultad para respirar"),
    ("confusion", "Confusión o alteración del estado de consciencia"),
    ("paralisis", "Parálisis o debilidad súbita"),
]


class Paso1Form(forms.Form):
    """Paso 1: Datos del paciente y motivo de consulta."""
    nombre_paciente = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Nombre del paciente (opcional en autoconsulta)",
        }),
    )
    edad = forms.IntegerField(
        required=False,
        min_value=1, max_value=150,
        widget=forms.NumberInput(attrs={
            "class": "form-input",
            "placeholder": "Edad",
        }),
    )
    ocupacion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Ocupacion",
        }),
    )
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-textarea",
            "placeholder": "Describe el motivo de consulta con el mayor detalle posible...",
            "rows": 5,
        }),
    )
    intensidad = forms.IntegerField(
        required=False,
        min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "class": "form-range",
            "type": "range",
            "min": "1",
            "max": "10",
            "step": "1",
            "id": "id_intensidad",
        }),
    )
    duracion = forms.ChoiceField(
        choices=DURACION_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={"class": "form-radio"}),
    )
    medicamentos_actuales = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-textarea",
            "placeholder": "Medicamentos, suplementos u otras terapias actuales (opcional)...",
            "rows": 2,
        }),
    )
    senales_alarma = forms.MultipleChoiceField(
        choices=ALARMA_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
    )


class Paso4ConfirmacionForm(forms.Form):
    """Paso 4: Confirmacion de diagnosticos."""
    diagnosticos_confirmados = forms.MultipleChoiceField(
        choices=[],  # Se popula dinamicamente
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-checkbox"}),
    )

    def __init__(self, *args, diagnosticos=None, **kwargs):
        super().__init__(*args, **kwargs)
        if diagnosticos:
            self.fields["diagnosticos_confirmados"].choices = [
                (str(d.id), d.titulo) for d in diagnosticos
            ]


class Paso5ResultadoForm(forms.Form):
    """Paso 5: Notas finales y guardado."""
    diagnostico_final = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-textarea",
            "placeholder": "Escribe aqui tu diagnostico integral final, integrando las visiones contrastantes...",
            "rows": 6,
        }),
    )
