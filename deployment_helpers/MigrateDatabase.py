from sshp.models.LkpProductName import LkpProductName
from sshp.models.LkpProductType import LkpProductType
from sshp.models.LkpProductSize import LkpProductSize

from sshp.models.Product import Product
import pandas as pd


def parse_excel_data():
    out_file = open("product_details.txt", "w")
    out_file.writelines("OLD_CODE,NEW_CODE" + "\n")

    lines = list()
    df = pd.read_excel(r'Testing.xlsx',
                       engine='openpyxl',
                       sheet_name='Product_List')

    for index, row in df.iterrows():
        product_id = row['SL_No']
        product_name = row['Product_Name']
        product_type = str(row['Product_Type'])
        product_size = str(row['Size'])
        selling_price = row['Selling_Price']
        product_category = str(row['Category'])

        if pd.notnull(product_name):
            row = add_new_product(product_id, product_name, product_type, product_size, selling_price, product_category)
            lines.append(row + "\n")

    out_file.writelines(lines)
    out_file.close()


def add_new_product(product_id, product_name, product_type, product_size, selling_price, product_category):
    product_name = product_name
    product_type = product_type
    product_size = product_size
    selling_price = selling_price
    actual_price = selling_price
    product_category = product_category

    if product_type == "nan":
        product_type = "-"

    if product_size == "nan":
        product_size = "-"

    product_name_code = LkpProductName.get_code(product_name=product_name)
    if product_name_code is None:
        product_name_code = LkpProductName.create_lookup(product_name, product_category)

    product_type_code = LkpProductType.get_code(product_type=product_type)
    if product_type_code is None:
        product_type_code = LkpProductType.create_lookup(product_type)

    product_size_code = LkpProductSize.get_code(product_size=product_size)
    if product_size_code is None:
        product_size_code = LkpProductSize.create_lookup(product_size)

    product_price_code = str(int(selling_price)).zfill(4)
    product_code = f"{product_name_code}-{product_type_code}-{product_size_code}-{product_price_code}"

    product = (product_code, product_name, product_type, product_size, selling_price, actual_price)

    product_list = Product.search_products(product_code, product_name, product_type, product_size, selling_price)
    if product_list:
        print(f"Product: '{product}' is already exists!")
    else:
        Product.add_product(product)
        print(f"{product_id}, {product_code}")
        return f"{product_id}, {product_code}"
        # print(f"Product: {product} is added!")


if __name__ == '__main__':
    parse_excel_data()
