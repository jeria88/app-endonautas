from django.urls import path
from . import views

app_name = "terapeuta"

urlpatterns = [
    path("", views.consulta_lista, name="lista"),
    path("nueva/", views.wizard_paso0, name="paso0"),
    path("<int:consulta_id>/paso1/", views.wizard_paso1, name="paso1"),
    path("<int:consulta_id>/paso2/", views.wizard_paso2, name="paso2"),
    path("<int:consulta_id>/paso3/", views.wizard_paso3, name="paso3"),
    path("<int:consulta_id>/paso4/", views.wizard_paso4, name="paso4"),
    path("<int:consulta_id>/paso5/", views.wizard_paso5, name="paso5"),
    path("<int:consulta_id>/detalle/", views.consulta_detalle, name="detalle"),
    path("<int:consulta_id>/eliminar/", views.consulta_eliminar, name="eliminar"),
]
