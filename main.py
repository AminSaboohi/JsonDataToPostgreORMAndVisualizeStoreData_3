from database_manager import DatabaseManager
import matplotlib.pyplot as plt
import pandas as pd
import argparse
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
# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__} was called")
        return func(*args, **kwargs)

    return wrapper


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


class SalesReport:
    def __init__(self, file_name: str = FILE_ADDRESS):
        self.data_from_db = None
        self.sales_data = self.load_data(file_name)
        database_manager.drop_tables(models=[SaleInfo, Item])
        database_manager.create_tables(models=[SaleInfo, Item])
        self.read_all_datas_and_add_to_db()
        self.load_sales_data_from_db()

    @staticmethod
    @log_decorator
    def load_data(file_name: str = "sample.json"):
        try:
            data_frame = pd.read_json(file_name)
            return data_frame
        except FileNotFoundError:
            logging.error("sample.json file not found.")
            return None

    def read_all_datas_and_add_to_db(self):
        sales_data = self.sales_data
        items = sales_data["title"]
        items_list = list()
        for index in items.keys():
            item_name = items[index]
            if item_name not in items_list:
                Item.create(item_name=item_name)
                items_list.append(item_name)
        customers = sales_data["customer_id"]
        months = sales_data["month"]
        counts = sales_data["count"]
        total_prices = sales_data["total_price"]
        for index in customers.keys():
            item_object = Item.select().where(
                Item.item_name == items[index]).first()
            SaleInfo.create(customer_id=customers[index],
                            item=item_object,
                            month=months[index],
                            count=counts[index],
                            total_price=total_prices[index])

    def load_sales_data_from_db(self):
        sale_info_objects = SaleInfo.select()
        data_sample = {
            "customer_id": [],
            "item": [],
            "month": [],
            "count": [],
            "total_price": []
        }
        self.data_from_db = pd.DataFrame(data_sample)
        for index, sale_info_object in enumerate(sale_info_objects):
            data = {
                "customer_id": sale_info_object.customer_id,
                "item": sale_info_object.item.item_name,
                "month": int(sale_info_object.month),
                "count": int(sale_info_object.count),
                "total_price": int(sale_info_object.total_price)
            }
            self.data_from_db.loc[len(self.data_from_db)] = data
        print(self.data_from_db)

    @log_decorator
    def find_most_sales_item(self) -> list:
        items = self.data_from_db["item"].drop_duplicates().sort_values()

        df_items = pd.DataFrame(index=items,
                                columns=["total_sales"])
        for item in items:
            query_str = f"item == '{item}'"
            total_sale = self.data_from_db.query(query_str)["count"].sum()
            df_items.loc[item] = total_sale
        df_items = df_items.sort_values(by="total_sales", ascending=False)
        return df_items.index[:5]

    @log_decorator
    def plot_sales_per_month(self, most_sales_item: list, axis):
        for item in most_sales_item:
            query_str = f"item == '{item}'"
            product_orders = self.data_from_db.query(query_str)
            if product_orders.empty:
                raise KeyError
            months = product_orders["month"].drop_duplicates().sort_values()

            item_sales_per_month = self.sales_per_month(product_orders,
                                                        months=months,
                                                        )
            axis[0].plot(months, item_sales_per_month, label=item)

            # Naming the x-axis, y-axis and the whole graph
        axis[0].set_xlabel("Month")
        axis[0].set_ylabel("total_sale_count")
        axis[0].set_title("Total sale count per month for items")
        # Adding legend, which helps us recognize the curve according to
        # it's color
        axis[0].legend()

    @log_decorator
    def plot_purchase_per_month(self, most_sales_item: list, axis):
        for item in most_sales_item:
            query_str = f"item == '{item}'"
            product_orders = self.data_from_db.query(query_str)
            if product_orders.empty:
                raise KeyError
            months = product_orders[
                "month"].drop_duplicates().sort_values()
            item_sales_per_month = self.purchase_per_month(product_orders,
                                                           months=months,
                                                           )
            axis[1].plot(months, item_sales_per_month, label=item)

            # Naming the x-axis, y-axis and the whole graph
        axis[1].set_xlabel("Month")
        axis[1].set_ylabel("Purchase")
        axis[1].set_title("Purchase per month for items")
        # Adding legend, which helps us recognize the curve according to
        # it's color
        axis[1].legend()

    @staticmethod
    @log_decorator
    def arg_input_parser() -> int:
        parser = argparse.ArgumentParser(
            description="Sales data visualisation"
        )
        parser.add_argument("-r",
                            "--report",
                            help="Report",
                            action='store_true',
                            )
        args = parser.parse_args()
        flag_value = args.report
        return flag_value

    @staticmethod
    @log_decorator
    def sales_per_month(product_orders_in, months: list):
        total_sales = list()
        for month in months:
            query_str = f"month == {month}"
            total_sale = product_orders_in.query(query_str)["count"].sum()
            total_sales.append(total_sale)
        return pd.DataFrame(total_sales)

    @staticmethod
    @log_decorator
    def purchase_per_month(product_orders_in, months: list):
        total_sales = list()
        for month in months:
            query_str = f"month == {month}"
            total_sale = product_orders_in.query(query_str)[
                "total_price"
            ].sum()
            total_sales.append(total_sale)
        return pd.DataFrame(total_sales)


def main():
    sale_report = SalesReport(file_name=FILE_ADDRESS)
    if sale_report.arg_input_parser():
        most_sale_items = sale_report.find_most_sales_item()
        figure, axis = plt.subplots(nrows=1, ncols=2)
        sale_report.plot_sales_per_month(most_sale_items, axis)
        sale_report.plot_purchase_per_month(most_sale_items, axis)
        # To load the display window
        plt.show()
    else:
        logging.info("No arguments entered")


if __name__ == "__main__":
    main()
