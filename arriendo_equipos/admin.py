from django.contrib import admin
from .models import Arriendo, Equipo


def _formatear_pesos_chilenos(monto):
    return f"CLP {monto:,.0f}".replace(",", ".")


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio_en_pesos", "disponible")
    list_filter = ("disponible",)
    search_fields = ("nombre", "descripcion")

    @admin.display(description="Precio (CLP)", ordering="precio")
    def precio_en_pesos(self, obj):
        return _formatear_pesos_chilenos(obj.precio)


@admin.register(Arriendo)
class ArriendoAdmin(admin.ModelAdmin):
    list_display = ("equipo", "cliente", "fecha_inicio", "fecha_fin", "monto_en_pesos")
    list_filter = ("fecha_inicio", "fecha_fin")
    search_fields = ("equipo__nombre", "cliente")

    @admin.display(description="Monto (CLP)", ordering="monto")
    def monto_en_pesos(self, obj):
        return _formatear_pesos_chilenos(obj.monto)
