from django.test import TestCase
from django.contrib import admin
from .admin import ArriendoAdmin, EquipoAdmin
from .models import Arriendo, Equipo


class EquipoArriendoTests(TestCase):
    def test_arriendo_queda_asociado_al_equipo(self):
        equipo = Equipo.objects.create(
            nombre="Taladro",
            descripcion="Taladro percutor",
            precio="10000.00",
        )
        arriendo = Arriendo.objects.create(
            equipo=equipo,
            fecha_inicio="2026-10-14",
            fecha_fin="2026-10-15",
            cliente="Cliente de prueba",
            monto="15000.00",
        )

        self.assertEqual(arriendo.equipo, equipo)
        self.assertEqual(equipo.arriendo_set.get(), arriendo)
        self.assertEqual(str(equipo), "Taladro")
        self.assertEqual(str(arriendo), "Arriendo de Taladro para Cliente de prueba")
        self.assertEqual(str(arriendo.monto), "15000.00")

    def test_eliminar_equipo_elimina_sus_arriendos(self):
        equipo = Equipo.objects.create(
            nombre="Generador",
            descripcion="Generador eléctrico",
            precio="25000.00",
        )
        arriendo = Arriendo.objects.create(
            equipo=equipo,
            fecha_inicio="2026-10-14",
            fecha_fin="2026-10-15",
            cliente="Cliente de prueba",
            monto="30000.00",
        )

        equipo.delete()

        self.assertFalse(Equipo.objects.filter(pk=equipo.pk).exists())
        self.assertFalse(Arriendo.objects.filter(pk=arriendo.pk).exists())

    def test_equipo_y_arriendo_estan_registrados_en_admin(self):
        equipo_admin = admin.site._registry[Equipo]
        arriendo_admin = admin.site._registry[Arriendo]
        self.assertIsInstance(equipo_admin, EquipoAdmin)
        self.assertIsInstance(arriendo_admin, ArriendoAdmin)
        self.assertEqual(equipo_admin.list_filter, ("disponible",))
        self.assertEqual(equipo_admin.search_fields, ("nombre", "descripcion"))
        self.assertEqual(arriendo_admin.list_filter, ("fecha_inicio", "fecha_fin"))
        self.assertEqual(arriendo_admin.search_fields, ("equipo__nombre", "cliente"))

    def test_listados_muestran_varios_datos_y_montos_en_pesos_chilenos(self):
        equipo = Equipo.objects.create(
            nombre="Compresor",
            descripcion="Compresor industrial",
            precio="1250000.00",
        )
        arriendo = Arriendo.objects.create(
            equipo=equipo,
            fecha_inicio="2026-10-14",
            fecha_fin="2026-10-16",
            cliente="Cliente de prueba",
            monto="2500000.00",
        )
        equipo.refresh_from_db()
        arriendo.refresh_from_db()

        equipo_admin = EquipoAdmin(Equipo, admin.site)
        arriendo_admin = ArriendoAdmin(Arriendo, admin.site)

        self.assertGreaterEqual(len(equipo_admin.get_list_display(None)), 3)
        self.assertGreaterEqual(len(arriendo_admin.get_list_display(None)), 5)
        self.assertEqual(equipo_admin.precio_en_pesos(equipo), "CLP 1.250.000")
        self.assertEqual(arriendo_admin.monto_en_pesos(arriendo), "CLP 2.500.000")
