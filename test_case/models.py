# Django packages
from django.db.models import Model, SmallIntegerField, BigIntegerField, \
    CharField, UUIDField, ForeignKey, TextField, CASCADE

# import for uuid_pk
import uuid


class Region(Model):

    class Meta:
        db_table = 'region'

    region_pk = UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_column='region_pk'
    )

    city_code = SmallIntegerField(
        db_column='city_code',
        db_index=True
    )

    geo = CharField(
        max_length=4096,
        db_column='geo'
    )


class Operator(Model):

    class Meta:
        db_table = 'operator'

    operator = CharField(
        max_length=4096,
        db_column='operator',
        primary_key=True,
        db_index=True
    )


class PhoneNumber(Model):

    class Meta:
        db_table = 'phone_number'
        # https://docs.djangoproject.com/en/4.2/ref/models/options/#index-together
        index_together = ['start', 'finish']

    start = start = BigIntegerField(
        null=True,
        db_column='start'
    )

    finish = BigIntegerField(
        null=True,
        db_column='finish'
    )

    operator = ForeignKey(
        Operator,
        on_delete=CASCADE,
        db_column='operator'
    )

    region_pk = ForeignKey(
        Region,
        to_field='region_pk',
        on_delete=CASCADE,
        db_column='region_pk'
    )

