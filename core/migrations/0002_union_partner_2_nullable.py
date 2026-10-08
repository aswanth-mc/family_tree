from django.db import migrations, models
from django.db.models import F
import django.db.models.deletion


def clear_self_unions(apps, schema_editor):
    Union = apps.get_model('core', 'Union')
    Union.objects.filter(partner_1=F('partner_2')).update(partner_2=None)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='union',
            name='partner_2',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='union_as_p2',
                to='core.person',
            ),
        ),
        migrations.RunPython(clear_self_unions, migrations.RunPython.noop),
    ]
