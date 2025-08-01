from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('minecraft_app', '0017_add_companion_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeitem',
            name='pet_image',
            field=models.CharField(
                blank=True,
                help_text='Nom du fichier image pour les compagnons (ex: dragon.png, chat.png). L\'image doit être dans static/images/pets/',
                max_length=255,
                null=True
            ),
        ),
    ]