# Django packages
from django.db.models import Model
from django.db.models import SmallIntegerField, BigIntegerField, \
    CharField, UUIDField

# import for uuid_pk
import uuid


class CSV(Model):

    class Meta:
        db_table = 'csv'

    # i don't see reason for PK in this case, but Django ORM can't without PK
    uuid_pk = UUIDField(primary_key=True, default=uuid.uuid4, db_column='pk')

    city_code = SmallIntegerField(null=True, db_column='city_code')
    start = BigIntegerField(null=True, db_column='start')
    finish = BigIntegerField(null=True, db_column='finish')
    operator = CharField(max_length=4096, null=True, db_column='operator')
    geo = CharField(max_length=4096, null=True, db_column='geo')
