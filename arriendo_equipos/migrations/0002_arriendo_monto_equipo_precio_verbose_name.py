from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("arriendo_equipos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipo",
            name="precio",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                verbose_name="Precio (CLP)",
            ),
        ),
        migrations.AddField(
            model_name="arriendo",
            name="monto",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Monto (CLP)",
            ),
            preserve_default=False,
        ),
    ]
