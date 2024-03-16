from database_manager import DatabaseManager

import peewee
import logging
import local_settings

FILE_ADDRESS = "sample.json"

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)


class Item(peewee.Model):
    item_name = peewee.CharField(max_length=255,
                                 null=False,
                                 verbose_name='Item name',
                                 )

    class Meta:
        database = database_manager.db


class SaleInfo(peewee.Model):
    item = peewee.ForeignKeyField(model=Item,
                                  null=False,
                                  verbose_name='Item',
                                  )
    customer_id = peewee.CharField(max_length=255,
                                   null=False,
                                   verbose_name='Customer id',
                                   )
    month = peewee.CharField(max_length=100,
                             null=False,
                             verbose_name='Month',
                             )
    count = peewee.CharField(max_length=100,
                             null=False,
                             verbose_name='Count',
                             )
    total_price = peewee.CharField(max_length=100,
                                   null=False,
                                   verbose_name='Total price',
                                   )

    class Meta:
        database = database_manager.db


# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


def main():

    database_manager.drop_tables(models=[SaleInfo, Item])
    database_manager.create_tables(models=[SaleInfo, Item])


if __name__ == "__main__":
    main()
