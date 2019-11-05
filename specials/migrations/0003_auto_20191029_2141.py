# Generated by Django 2.2.6 on 2019-10-29 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specials', '0002_category_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offeritem',
            old_name='new_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='offeritem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='offeritem',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='offeritem',
            name='offer_expired',
        ),
        migrations.RemoveField(
            model_name='offeritem',
            name='offer_expiry_date',
        ),
        migrations.RemoveField(
            model_name='offeritem',
            name='original_price',
        ),
        migrations.AddField(
            model_name='offeritem',
            name='deal_title',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offeritem',
            name='deal_url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='offeritem',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offeritem',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store', to='specials.Store'),
        ),
    ]