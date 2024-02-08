# Generated by Django 3.1.14 on 2024-01-25 15:37

from django.db import migrations


SPLIT_CHAR = ';'


def split_thesaurus(thesaurus_model, thesaurus_field, relation_model,
                    relation_thesaurus_field, relation_record_field):

    qs = relation_model.objects.filter(**{
        f'{relation_thesaurus_field}__{thesaurus_field}__contains': SPLIT_CHAR,
    }).values_list(
        'id',
        f'{relation_thesaurus_field}_id',
        f'{relation_thesaurus_field}__{thesaurus_field}',
        f'{relation_record_field}_id',
    )

    old_relation_ids = set()
    old_thesaurus_ids = set()
    new_thesaurus_ids = {}

    for old_relation_id, old_thesaurus_id, old_thesaurus_name, record_id in qs:
        for new_thesaurus_name in old_thesaurus_name.split(SPLIT_CHAR):
            # découpage du nom
            new_thesaurus_name = new_thesaurus_name.strip()
            if not new_thesaurus_name:
                continue

            # lecture ou création du nouveau nom dans le thésaurus
            thesaurus_id = new_thesaurus_ids.get(new_thesaurus_name)
            if not thesaurus_id:
                thesaurus_id = thesaurus_model.objects.get_or_create(**{
                    thesaurus_field: new_thesaurus_name,
                })[0].id
                new_thesaurus_ids[new_thesaurus_name] = thesaurus_id

            # association du nouveau nom à l’enregistrement principal
            relation_model.objects.get_or_create(**{
                f'{relation_thesaurus_field}_id': thesaurus_id,
                f'{relation_record_field}_id': record_id,
            })

        # mémorisation de l’ancienne relation et de l’ancien thésaurus à supprimer
        old_relation_ids.add(old_relation_id)
        old_thesaurus_ids.add(old_thesaurus_id)

    #suppression des anciennes relations et des anciens thésaurus
    if old_relation_ids:
        relation_model.objects.filter(id__in=old_relation_ids).delete()
    if old_thesaurus_ids:
        thesaurus_model.objects.filter(id__in=old_thesaurus_ids).delete()


def split_many_thesaurus(apps, schema_editor):
    split_thesaurus(
        thesaurus_model=apps.get_model('francoralite_api', 'Civility'),
        thesaurus_field='name',
        relation_model=apps.get_model('francoralite_api', 'AuthorityCivility'),
        relation_thesaurus_field='civility',
        relation_record_field='authority',
    )
    split_thesaurus(
        thesaurus_model=apps.get_model('francoralite_api', 'CulturalArea'),
        thesaurus_field='name',
        relation_model=apps.get_model('francoralite_api', 'CollectionCulturalArea'),
        relation_thesaurus_field='cultural_area',
        relation_record_field='collection',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('francoralite_api', '0014_cultural_area'),
    ]

    operations = [
        migrations.RunPython(
            code=split_many_thesaurus,
            reverse_code=migrations.RunPython.noop,
            atomic=True,
        ),
    ]