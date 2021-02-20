import tkinter as tk
from collections import defaultdict
from tkinter import ttk

import pandas as pd
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.Product import Product
from sshp.models.Sales import Sales
from sshp.models.Stock import Stock


class PurchaseReportForm(MainForm):
    def __init__(self):
        super().__init__()

        self.search_product_id = tk.StringVar()

        self.filter_ety_product_name = None
        self.filter_ety_product_type = None

        self.ety_search_product_id = None

        # local variables
        self.tree = None
        self.selected = list()
        self.product_name_list = list()
        self.product_type_list = list()

        self.load_view_report_form()

    def load_view_report_form(self):
        self.update_username()

        products = Product.get_product_name_list()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = Product.get_product_type_list()
        for product in products:
            self.product_type_list.append(product.product_type)

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg='#62b6e2')
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        left_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg='#62b6e2')
        left_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(left_button_container, relief=tk.RIDGE, bg='#62b6e2')
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(left_button_container, relief=tk.RIDGE, bg='#62b6e2')
        filter_container.pack(fill='x', expand=True, side=tk.LEFT)

        # ********** left_search_container elements *********
        search_lbl_product_id = tk.Label(search_container, text="ID: ", bg='#62b6e2')
        search_lbl_product_id.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_search_product_id = tk.Entry(search_container, width=10, textvariable=self.search_product_id)
        self.ety_search_product_id.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_search_product_id.bind('<Return>', lambda event: self.search_report(event))

        btn_search = tk.Button(search_container, text="Search", command=self.search_report)
        btn_search.grid(row=1, column=1, sticky="sw", padx=2, pady=1)

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg='#62b6e2')
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, completevalues=self.product_name_list,
                                                         state='disabled')
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_report(event))

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg='#62b6e2')
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, completevalues=self.product_type_list,
                                                         state='disabled')
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=5, pady=5, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_report(event))

        btn_filter = tk.Button(filter_container, text="Apply Filter", command=self.filter_report, state='disabled')
        btn_filter.grid(row=1, column=2, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(filter_container, text="Clear Filter", command=self.reload_report)
        btn_clear_filter.grid(row=1, column=3, sticky="sw", padx=2, pady=1)

        btn_export = tk.Button(filter_container, text="Export to Excel", command=self.export_data)
        btn_export.grid(row=1, column=4, sticky="se", padx=15, pady=1)

        # ********** left_container *********
        tree_container = tk.Frame(left_container, pady=3, bg='#62b6e2')
        tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'date', 'product_id', 'product_name', 'product_type', 'product_size',
                  'selling_price', 'actual_price', 'quantity', 'total_amount', 'dummy')
        self.tree = ttk.Treeview(tree_container, columns=header, show="headings", height=15, selectmode="browse")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=tree_container)

        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)

        self.tree.heading("0", text="#")
        self.tree.heading("1", text="DATE")
        self.tree.heading("2", text="ID")
        self.tree.heading("3", text="PRODUCT_NAME")
        self.tree.heading("4", text="PRODUCT_TYPE")
        self.tree.heading("5", text="SIZE")
        self.tree.heading("6", text="SELL_PRICE")
        self.tree.heading("7", text="ACTUAL_PRICE")
        self.tree.heading("8", text="QTY")
        self.tree.heading("9", text="TOTAL_AMOUNT")

        self.tree.column(0, anchor='center', width="50")
        self.tree.column(1, anchor=tk.W, width="100")
        self.tree.column(2, anchor='center', width="50")
        self.tree.column(3, anchor=tk.W, width="150")
        self.tree.column(4, anchor=tk.W, width="200")
        self.tree.column(5, anchor='center', width="100")
        self.tree.column(6, anchor=tk.E, width="120")
        self.tree.column(7, anchor=tk.E, width="120")
        self.tree.column(8, anchor='center', width="80")
        self.tree.column(9, anchor=tk.E, width="120")
        self.tree.column(10, anchor='center', width="5")

        self.reload_report()

        btn_close = tk.Button(self.footer_container, text="Close", width='20', command=self.window.destroy)
        btn_close.pack(padx=5, pady=5)

        self.tree.tag_configure("evenrow", background='#fbefcc')
        self.tree.tag_configure("oddrow", background='white', foreground='black')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def filter_report(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()

        rows = Stock.search_stock(product_name=product_name, product_type=product_type)
        self.tree.delete(*self.tree.get_children())

        if len(rows):
            sl_no = 0
            for row in rows:
                product = row.Product
                stock = row.Stock

                sl_no = sl_no + 1
                quantity = "-"
                if stock:
                    quantity = stock.quantity

                rw = (sl_no, product.product_code, product.product_name, product.product_type, product.product_size,
                      round(product.selling_price, 2), round(product.actual_price, 2), quantity)

                if sl_no % 2 == 0:
                    self.tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
                else:
                    self.tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))
        else:
            pass

    def export_data(self):
        rows = self.tree.get_children()
        my_dict = defaultdict(list)
        for row in rows:
            my_dict["SL_NO"].append(self.tree.item(row)["values"][0])
            my_dict["DATE"].append(self.tree.item(row)["values"][1])
            my_dict["P_ID"].append(self.tree.item(row)["values"][2])
            my_dict["PRODUCT_NAME"].append(self.tree.item(row)["values"][3])
            my_dict["PRODUCT_TYPE"].append(self.tree.item(row)["values"][4])
            my_dict["SIZE"].append(self.tree.item(row)["values"][5])
            my_dict["SELL_PRICE"].append(self.tree.item(row)["values"][6])
            my_dict["ACTUAL_PRICE"].append(self.tree.item(row)["values"][7])
            my_dict["QUANTITY"].append(self.tree.item(row)["values"][8])
            my_dict["TOTAL_AMOUNT"].append(self.tree.item(row)["values"][9])

        my_dict = pd.DataFrame.from_dict(my_dict)
        try:
            my_dict.to_excel('SalesReport.xlsx', engine='xlsxwriter', index=False)
        except:
            print("Close the file than retry")

    def reload_report(self):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)

        self.tree.delete(*self.tree.get_children())

        sales = Sales.sales_report_daily()
        sl_no = 0
        for sale in sales:
            sl_no += 1
            product = Product.get_product(sale.product_code)
            rw = (sl_no, sale.sales_date, product.product_code, product.product_name,
                  product.product_type, product.product_size,
                  round(product.selling_price, 2), round(product.actual_price, 2),
                  sale.quantity, round(product.selling_price * sale.quantity, 2))

            if sl_no % 2 == 0:
                self.tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
            else:
                self.tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))

    def search_report(self, event=None):
        product_id = self.search_product_id.get().strip()

        row = Stock.search_stock(product_id=product_id)
        if len(row):
            self.tree.selection_set(self.tree.tag_has(str(product_id)))
            self.tree.focus_set()
            self.tree.focus(self.selected)
        else:
            print('No items matched!')

    def on_tree_select(self, event):
        self.selected = event.widget.selection()
