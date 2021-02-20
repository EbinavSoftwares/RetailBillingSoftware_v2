import tkinter as tk
from datetime import datetime
from tkinter import TclError
from tkinter import messagebox
from tkinter import ttk

from babel.numbers import format_currency, format_decimal
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.LkpProductName import LkpProductName
from sshp.models.LkpProductSize import LkpProductSize
from sshp.models.LkpProductType import LkpProductType
from sshp.models.Product import Product
from sshp.models.ProductCategory import ProductCategory
from sshp.models.Purchase import Purchase
from sshp.models.Stock import Stock
from sshp.models.StockTimeline import StockTimeline


class AddPurchaseForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - Add Purchase")

        # variables
        self.select_first_row_threshold = 10
        self.selected_row = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()
        self.product_category_list = list()
        self.product_actual_price_list = list()
        self.purchase_counter = 0

        # widgets
        self.filter_ety_product_name = None
        self.filter_ety_product_type = None
        self.filter_ety_product_size = None
        self.filter_ety_product_sell_price = None
        self.filter_ety_product_actual_price = None
        self.cbo_product_category = None
        self.products_tree = None
        self.purchase_tree = None
        self.purchase_date = None
        self.ety_garment_name = None
        self.qty_window = None

        # widget variables
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        self.var_actual_price = tk.DoubleVar()
        self.var_purchase_amount = tk.StringVar()
        self.var_purchase_quantity = tk.IntVar()
        self.var_available_quantity = tk.IntVar()
        self.var_quantity = tk.IntVar(value=1)

        self.load_add_purchase_form()

        # shortcuts
        self.window.bind("<F3>", lambda event: self.copy_to_new(event))
        self.window.bind("<F4>", lambda event: self.add_new_product(event))
        self.window.bind("<F5>", lambda event: self.filter_product(event))
        self.window.bind("<F1>", lambda event: self.select_first_row(event))

    def load_add_purchase_form(self):
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.show_menu(MainForm.is_admin_user)
        self.update_username()

        products = LkpProductName.get_all_product_names()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = LkpProductType.get_all_product_types()
        for product in products:
            self.product_type_list.append(product.product_type)

        products = LkpProductSize.get_all_product_sizes()
        for product in products:
            self.product_size_list.append(product.product_size)

        products = Product.get_product_sell_price_list()
        for product in products:
            self.product_sell_price_list.append(str(round(product.selling_price, 2)))

        categories = ProductCategory.get_all_categories()
        for category in categories:
            self.product_category_list.append(category.category)

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        right_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg=self.clr_yellow)
        right_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container elements
        left_top_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg=self.clr_yellow)
        left_top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        products_tree_container = tk.Frame(left_container, pady=3, bg=self.clr_yellow, relief=tk.RIDGE)
        products_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        # right_container elements
        right_top_button_container = tk.Frame(right_container, relief=tk.RIDGE, bg=self.clr_yellow)
        right_top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        right_tree_container = tk.Frame(right_container, relief=tk.RIDGE, bg=self.clr_yellow)
        right_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        right_bottom_button_container = tk.Frame(right_container, relief=tk.RIDGE, bg=self.clr_yellow)
        right_bottom_button_container.pack(fill='both', expand=True, side=tk.TOP)

        # ********** left_search_container elements *********
        filter_lbl_product_name = tk.Label(left_top_button_container, text="Name: ", bg=self.clr_yellow)
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_name = AutocompleteEntry(left_top_button_container, width=15,
                                                         completevalues=self.product_name_list)
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_type = tk.Label(left_top_button_container, text="Type: ", bg=self.clr_yellow)
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_type = AutocompleteEntry(left_top_button_container, width=18,
                                                         completevalues=self.product_type_list)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_size = tk.Label(left_top_button_container, text="Size: ", bg=self.clr_yellow)
        filter_lbl_product_size.grid(row=0, column=2, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_size = AutocompleteEntry(left_top_button_container, width=12,
                                                         completevalues=self.product_size_list)
        self.filter_ety_product_size.grid(row=1, column=2, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_size.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_price = tk.Label(left_top_button_container, text="Sell Price: ", bg=self.clr_yellow)
        filter_lbl_product_price.grid(row=0, column=3, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_sell_price = AutocompleteEntry(left_top_button_container, width=8,
                                                               completevalues=self.product_sell_price_list)
        self.filter_ety_product_sell_price.grid(row=1, column=3, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_sell_price.bind("<Return>", lambda event: self.filter_product(event))

        # filter_lbl_product_actual_price = tk.Label(left_top_button_container, text="Act. Price: ", bg=self.clr_yellow)
        # filter_lbl_product_actual_price.grid(row=0, column=4, sticky="nw", padx=1, pady=1)
        # self.filter_ety_product_actual_price = AutocompleteEntry(left_top_button_container, width=8,
        #                                                          completevalues=self.product_actual_price_list)
        # self.filter_ety_product_actual_price.grid(row=1, column=4, sticky="nw", padx=2, pady=1, ipady=6)
        # self.filter_ety_product_actual_price.bind("<Return>", lambda event: self.filter_product(event))

        lbl_product_category = tk.Label(left_top_button_container, text="Category:", bg=self.clr_yellow)
        lbl_product_category.grid(row=0, column=4, sticky="nw", padx=1, pady=1)
        self.cbo_product_category = ttk.Combobox(left_top_button_container, width=7, values=self.product_category_list)
        self.cbo_product_category.grid(row=1, column=4, sticky="nw", padx=2, pady=1, ipady=6)

        btn_filter = tk.Button(left_top_button_container, text="Apply Filter [F5]", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_product)
        btn_filter.grid(row=1, column=5, sticky="news", padx=2, pady=1)

        btn_clear_filter = tk.Button(left_top_button_container, text="Clear", command=self.reload_products)
        btn_clear_filter.grid(row=1, column=6, sticky="news", padx=2, pady=1)

        btn_add_new = tk.Button(left_top_button_container, text="Add New [F4]", bg=self.clr_limegreen,
                                command=self.add_new_product)
        btn_add_new.grid(row=0, column=5, sticky="news", padx=1, pady=1)

        btn_copy = tk.Button(left_top_button_container, text="Copy [F3]", bg=self.clr_blueiris, fg='white',
                             command=self.copy_to_new)
        btn_copy.grid(row=0, column=6, sticky="news", padx=1, pady=1)

        # ********** tree_containers elements *********
        header = ('CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE', 'SIZE', 'PRICE', 'QTY', '')
        self.products_tree = ttk.Treeview(products_tree_container, columns=header, height=20, show="headings",
                                          selectmode="browse")
        vsb = ttk.Scrollbar(products_tree_container, orient="vertical", command=self.products_tree.yview)
        hsb = ttk.Scrollbar(products_tree_container, orient="horizontal", command=self.products_tree.xview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 10), rowheight=25)

        self.products_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.products_tree.grid(column=0, row=0, sticky='nsew', in_=products_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=products_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=products_tree_container)

        products_tree_container.grid_columnconfigure(0, weight=1)
        products_tree_container.grid_rowconfigure(0, weight=1)

        self.products_tree.heading("0", text="CODE")
        self.products_tree.heading("1", text="PRODUCT_NAME")
        self.products_tree.heading("2", text="PRODUCT_TYPE")
        self.products_tree.heading("3", text="SIZE")
        self.products_tree.heading("4", text="PRICE")
        self.products_tree.heading("5", text="QTY")

        self.products_tree.column(0, anchor='center', width="100")
        self.products_tree.column(1, anchor=tk.W, width="120")
        self.products_tree.column(2, anchor=tk.W, width="150")
        self.products_tree.column(3, anchor='center', width="50")
        self.products_tree.column(4, anchor=tk.E, width="50")
        self.products_tree.column(5, anchor='center', width="20")
        self.products_tree.column(6, anchor='center', width="1")

        self.products_tree.bind("<F3>", lambda event: self.copy_to_new(event))

        self.reload_products()

        numeric_cols = ['PRICE', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.products_tree.heading(col, text=col,
                                           command=lambda _col=col: self.sort_treeview(
                                               self.products_tree, _col,
                                               numeric_sort=True, reverse=False))
            else:
                self.products_tree.heading(col, text=col,
                                           command=lambda _col=col: self.sort_treeview(
                                               self.products_tree, _col,
                                               numeric_sort=False, reverse=False))

        # ********** Right Tree Details *********
        lbl_purchase_date = tk.Label(right_top_button_container, text='Purchase Date: ', bg=self.clr_yellow)
        lbl_purchase_date.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.purchase_date = DateEntry(right_top_button_container, date_pattern='yyyy-mm-dd', background='yellow',
                                       foreground='black', borderwidth=2)
        self.purchase_date.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=3)

        lbl_garment_name = tk.Label(right_top_button_container, text='Garment Name: ', bg=self.clr_yellow)
        lbl_garment_name.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.ety_garment_name = tk.Entry(right_top_button_container)
        self.ety_garment_name.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=3)

        btn_add_purchase = tk.Button(right_top_button_container, text="Add Purchase", bg=self.clr_fuchsia, fg='white',
                                     command=self.add_purchase)
        btn_add_purchase.grid(row=0, column=2, rowspan=2, sticky="se", padx=2, pady=1)

        btn_clear = tk.Button(right_top_button_container, text="Clear", command=self.clear_all)
        btn_clear.grid(row=0, column=3, rowspan=2, sticky="se", padx=2, pady=1)

        purchase_tree_container = tk.Frame(right_tree_container, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        purchase_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'product_code', 'product_name', 'type', 'size', 'selling_price', 'quantity', 'amount', 'dummy')
        self.purchase_tree = ttk.Treeview(purchase_tree_container, columns=header, height=15, show="headings",
                                          selectmode="browse")
        vsb = ttk.Scrollbar(purchase_tree_container, orient="vertical", command=self.purchase_tree.yview)
        hsb = ttk.Scrollbar(purchase_tree_container, orient="horizontal", command=self.purchase_tree.xview)

        self.purchase_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.purchase_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        purchase_tree_container.grid_columnconfigure(0, weight=1)
        purchase_tree_container.grid_rowconfigure(0, weight=1)

        self.purchase_tree.heading("0", text="#")
        self.purchase_tree.heading("1", text="Code")
        self.purchase_tree.heading("2", text="Product")
        self.purchase_tree.heading("3", text="Type")
        self.purchase_tree.heading("4", text="Size")
        self.purchase_tree.heading("5", text="Price")
        self.purchase_tree.heading("6", text="Qty")
        self.purchase_tree.heading("7", text="Amount")
        self.purchase_tree.heading("8", text="")

        self.purchase_tree.column(0, anchor='center', minwidth=25, width=25)
        self.purchase_tree.column(1, anchor=tk.W, minwidth=40, width=110)
        self.purchase_tree.column(2, anchor=tk.W, minwidth=80, width=100)  # Product
        self.purchase_tree.column(3, anchor=tk.W, minwidth=110, width=110)  # Type
        self.purchase_tree.column(4, anchor='center', minwidth=50, width=50)    # Size
        self.purchase_tree.column(5, anchor=tk.E, minwidth=50, width=50)  # Price
        self.purchase_tree.column(6, anchor='center', minwidth=40, width=40)  # Qty
        self.purchase_tree.column(7, anchor=tk.E, minwidth=60, width=60)  # Amount
        self.purchase_tree.column(8, anchor='center', width=1)
        self.purchase_tree["displaycolumns"] = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        self.purchase_tree.bind('<Double-1>', lambda event: self.remove_product(event))

        self.products_tree.tag_configure("evenrow_active", background='#fbefcc')
        self.products_tree.tag_configure("oddrow_active", background='white', foreground='black')
        self.products_tree.tag_configure("evenrow_inactive", background='#fbefcc', foreground='red')
        self.products_tree.tag_configure("oddrow_inactive", background='white', foreground='red')

        self.products_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.products_tree.bind('<Double-1>', lambda event: self.get_quantity(event))
        self.products_tree.bind('<Return>', lambda event: self.get_quantity(event))

        # ********** bottom_button_container elements *********
        lbl_purchase_quantity = tk.Label(right_bottom_button_container, fg=self.clr_limegreen, relief=tk.RAISED,
                                         textvariable=self.var_purchase_quantity)
        lbl_purchase_quantity.pack(side=tk.LEFT, fill='x', expand=True, padx=1, pady=1)
        lbl_purchase_quantity.config(font=("calibri bold", 30))

        lbl_purchase_amount = tk.Label(right_bottom_button_container, fg=self.clr_blueiris, relief=tk.RAISED,
                                       textvariable=self.var_purchase_amount)
        lbl_purchase_amount.pack(side=tk.LEFT, fill='x', expand=True, padx=1, pady=1)
        lbl_purchase_amount.config(font=("calibri bold", 30))

    def remove_product(self, event):
        selected_row = event.widget.selection()[0]
        self.purchase_tree.delete(selected_row)

        self.purchase_counter = 0
        for child in self.purchase_tree.get_children():
            self.purchase_counter = self.purchase_counter + 1
            row = self.purchase_tree.item(child)["values"]
            row[0] = self.purchase_counter

            self.purchase_tree.delete(child)
            self.purchase_tree.insert("", tk.END, values=row)

        self.calculate_total_amount_and_quantity()

    def select_first_row(self, event=None):
        element_id = self.products_tree.get_children()[0]
        self.products_tree.focus_set()
        self.products_tree.focus(element_id)
        self.products_tree.selection_set(element_id)

    def copy_to_new(self, event=None):
        if self.selected_row:
            product = self.products_tree.item(self.selected_row)['values']

            if product:
                self.filter_ety_product_name.delete(0, tk.END)
                self.filter_ety_product_name.insert(0, product[1])

                self.filter_ety_product_type.delete(0, tk.END)
                self.filter_ety_product_type.insert(0, product[2])

                self.filter_ety_product_size.delete(0, tk.END)
                self.filter_ety_product_size.insert(0, product[3])

                self.filter_ety_product_sell_price.delete(0, tk.END)
                self.filter_ety_product_sell_price.insert(0, product[4])

                product_category = ProductCategory.get_category_by_code(product[0][:3])
                self.cbo_product_category.current(self.product_category_list.index(product_category))

    def add_new_product(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()
        product_size = self.filter_ety_product_size.get().strip()
        product_category = self.cbo_product_category.get().strip()

        try:
            selling_price = round(float(self.filter_ety_product_sell_price.get().strip()), 2)
        except (ValueError, TclError):
            selling_price = 0.0

        try:
            actual_price = round(self.var_actual_price.get(), 2)
        except TclError:
            actual_price = 0.0

        if len(product_name) == 0:
            messagebox.showerror("SS Fashion Tuty", f"Product_Name is missing!")
            print(f"Product_Name is missing!")
            return

        if selling_price == "" or selling_price <= 0:
            messagebox.showerror("SS Fashion Tuty", f"Selling Price is missing!")
            print(f"selling price is missing!")
            return

        if product_category == "" or product_category is None:
            messagebox.showerror("SS Fashion Tuty", f"Category is missing!")
            print(f"Category is missing!")
            return

        if len(product_type) == 0:
            product_type = "-"

        if len(product_size) == 0:
            product_size = "-"

        existing_product_category = LkpProductName.get_product_category(product_name=product_name)
        if existing_product_category and product_category != existing_product_category:
            print(f"'{product_name}' already in '{existing_product_category}' category!")
            messagebox.showerror("SS Fashion Tuty",
                                 f"'{product_name}' already in '{existing_product_category}' category!"
                                 f"\nPlease rename the Product Name and try again!")
            return

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
            messagebox.showerror("SS Fashion Tuty", f"Product already exists! \nProduct_Code: {product_code}")
        else:
            Product.add_product(product)
            self.reload_products()
            print(f"Product: {product} is added!")

            product = Product.search_products(product_code=product_code)
            if product:
                self.products_tree.selection_set(self.products_tree.tag_has(product.product_code))
                self.products_tree.focus_set()

                self.products_tree.event_generate('<Return>')

    def add_purchase(self):
        purchase_date = datetime.strptime(self.purchase_date.get(), "%Y-%m-%d")
        garment_name = self.ety_garment_name.get().strip()

        if garment_name == "" or garment_name is None:
            messagebox.showerror("SS Fashion Tuty", f"Garment Name is missing!")
            print(f"Garment Name is missing!")
            return

        if self.purchase_tree.get_children():
            for child in self.purchase_tree.get_children():
                product_code = self.purchase_tree.item(child)["values"][1]
                quantity = self.purchase_tree.item(child)["values"][6]

                purchase = (purchase_date, garment_name, product_code, quantity)
                Purchase.add_purchase(purchase)

                stock = (product_code, quantity)
                Stock.upload_stock(stock)

                if StockTimeline.get_timeline(product_code=product_code):
                    activity = "Add Purchase"
                else:
                    activity = "Opening Stock"

                StockTimeline.add_timeline(entry_date=purchase_date, product_code=product_code, activity=activity,
                                           change=f"+{quantity}")

            messagebox.showinfo("SS Fashion Tuty", f"Purchase added Successfully!")
            self.clear_all()

    def filter_product(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()
        product_size = self.filter_ety_product_size.get().strip()
        selling_price = str(self.filter_ety_product_sell_price.get().strip())
        if selling_price:
            selling_price = float(selling_price)
        else:
            selling_price = 0.0

        products = Product.search_products(product_name=product_name,
                                           product_type=product_type,
                                           product_size=product_size,
                                           selling_price=selling_price)
        self.products_tree.delete(*self.products_tree.get_children())
        if products:
            row_num = 0
            for product in products:
                stock = Stock.get_stock(product_code=product.product_code)

                quantity = "0"
                if stock:
                    quantity = stock.quantity

                row_num += 1
                row = (product.product_code, product.product_name, product.product_type, product.product_size,
                       round(product.selling_price, 2), quantity)

                if row_num % 2 == 0:
                    if product.is_active:
                        self.products_tree.insert("", tk.END, values=row, tags=(
                            'evenrow_active',
                            product.product_code
                        ))
                    else:
                        self.products_tree.insert("", tk.END, values=row, tags=(
                            'evenrow_inactive',
                            product.product_code
                        ))
                else:
                    if product.is_active:
                        self.products_tree.insert("", tk.END, values=row, tags=(
                            'oddrow_active', product.product_code
                        ))
                    else:
                        self.products_tree.insert("", tk.END, values=row, tags=(
                            'oddrow_inactive',
                            product.product_code
                        ))

            if row_num <= self.select_first_row_threshold:
                self.select_first_row()
        else:
            pass

    def clear_all(self):
        self.ety_garment_name.delete(0, tk.END)
        self.purchase_counter = 0
        self.purchase_tree.delete(*self.purchase_tree.get_children())
        self.var_purchase_amount.set(format_currency(0, 'INR', locale='en_IN'))
        self.var_purchase_quantity.set(format_decimal(0, locale='en_US'))

        self.reload_products()
        self.selected_row = list()

    def calculate_total_amount_and_quantity(self):
        total_amount = 0
        total_quantity = 0
        for child in self.purchase_tree.get_children():
            total_amount += float(self.purchase_tree.item(child)["values"][7])
            total_quantity += int(self.purchase_tree.item(child)["values"][6])

        self.var_purchase_amount.set(format_currency(total_amount, 'INR', locale='en_IN'))
        self.var_purchase_quantity.set(format_decimal(total_quantity, locale='en_US'))

    def get_quantity(self, event):
        self.selected_row = event.widget.selection()
        product = self.products_tree.item(self.selected_row)['values']

        if isinstance(product, str):
            return

        available_quantity = product[5]

        self.var_available_quantity.set(available_quantity)

        self.window.wm_attributes("-disabled", True)

        self.qty_window = tk.Toplevel(self.window)
        self.qty_window.overrideredirect(True)
        self.qty_window.bind("<FocusOut>", self.on_focus_out_qty_window)

        # Gets the requested values of the height and width.
        window_width = self.qty_window.winfo_reqwidth()
        window_height = self.qty_window.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.qty_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.qty_window.winfo_screenheight() / 2 - window_height / 2)

        # Positions the window in the center of the page.
        self.qty_window.geometry("+{}+{}".format(position_right, position_down))

        qty_container = tk.Frame(self.qty_window, bd=20, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_limegreen)
        qty_container.pack(expand=True, side=tk.TOP, anchor="n")

        lbl_quantity = tk.Label(qty_container, text="Quantity:", bg=self.clr_limegreen)
        lbl_quantity.grid(row=0, column=0, columnspan=2, padx=5, pady=2)

        ety_quantity = tk.Entry(qty_container, width=5, textvariable=self.var_quantity)
        ety_quantity.grid(row=1, column=0, padx=5, pady=2)

        if self.var_available_quantity.get() <= self.stock_alert_value:
            ety_available_quantity = tk.Entry(qty_container, width=5, textvariable=self.var_available_quantity,
                                              disabledbackground="red", disabledforeground="white", justify=tk.CENTER,
                                              state='disabled')
        else:
            ety_available_quantity = tk.Entry(qty_container, width=5, textvariable=self.var_available_quantity,
                                              justify=tk.CENTER, state='disabled')

        ety_available_quantity.grid(row=1, column=1, padx=5, pady=2)

        ety_quantity.delete(0, tk.END)
        ety_quantity.insert(tk.END, 1)
        self.var_quantity.set(1)
        ety_quantity.focus()
        ety_quantity.selection_range(0, tk.END)

        btn_ok = tk.Button(qty_container, text='Add', width=10, bg=self.clr_fuchsia, fg='white',
                           command=lambda: self.cleanup_qty_window(event))
        btn_ok.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.qty_window.bind('<Return>', lambda evnt: self.cleanup_qty_window(event))
        self.qty_window.bind('<Escape>', lambda evnt: self.cleanup_qty_window(event, add_quantity=False))

    def on_focus_out_qty_window(self, event=None):
        self.window.wm_attributes("-disabled", False)
        self.qty_window.destroy()

    def cleanup_qty_window(self, event, add_quantity=True):
        quantity = int(self.var_quantity.get())
        self.window.wm_attributes("-disabled", False)
        self.qty_window.destroy()

        if add_quantity:
            self.var_quantity.set(quantity)
            self.add_to_purchase_list(event)

    def add_to_purchase_list(self, event):
        quantity = self.var_quantity.get()

        self.selected_row = event.widget.selection()
        product = self.products_tree.item(self.selected_row)['values']

        active_product = Product.get_product_status(product_code=product[0])
        if not active_product:
            msg_box = messagebox.askquestion(
                "SS Fashion Tuty", "In-Active product! - Do you want to activate this Product?", icon='question'
            )
            if msg_box == 'yes':
                Product.activate_product(product_code=product[0])
                self.reload_products()
            else:
                return

        for child in self.purchase_tree.get_children():
            if self.purchase_tree.item(child)["values"][1] == product[0]:
                prev_quantity = self.purchase_tree.item(child)["values"][6]
                price = self.purchase_tree.item(child)["values"][5]

                quantity += prev_quantity
                self.purchase_tree.set(child, "#7", quantity)
                self.purchase_tree.set(child, "#8", float(price) * quantity)

                break
        else:
            self.purchase_counter = self.purchase_counter + 1
            row = (self.purchase_counter, product[0], product[1], product[2], product[3], round(float(product[4]), 2),
                   quantity, round(float(product[4]), 2) * quantity)

            self.purchase_tree.insert("", tk.END, values=row)

        self.calculate_total_amount_and_quantity()

        if len(self.products_tree.selection()) > 0:
            self.products_tree.selection_remove(self.products_tree.selection()[0])

    def reload_products(self):
        self.cbo_product_category.delete(0, "end")
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)
        self.filter_ety_product_size.delete(0, tk.END)
        self.filter_ety_product_sell_price.delete(0, tk.END)

        self.products_tree.delete(*self.products_tree.get_children())

        products = Product.get_all_products()
        row_num = 0
        for product in products:
            row_num += 1

            stock = Stock.get_stock(product_code=product.product_code)
            quantity = "0"
            if stock:
                quantity = stock.quantity

            row = (product.product_code, product.product_name, product.product_type, product.product_size,
                   round(product.selling_price, 2), quantity)

            if row_num % 2 == 0:
                if product.is_active:
                    self.products_tree.insert("", tk.END, values=row, tags=('evenrow_active', product.product_code))
                else:
                    self.products_tree.insert("", tk.END, values=row, tags=('evenrow_inactive', product.product_code))
            else:
                if product.is_active:
                    self.products_tree.insert("", tk.END, values=row, tags=('oddrow_active', product.product_code))
                else:
                    self.products_tree.insert("", tk.END, values=row, tags=('oddrow_inactive', product.product_code))

    def on_tree_select(self, event):
        self.selected_row = event.widget.selection()

        product = self.products_tree.item(self.selected_row)['values']

        if product:
            self.var_product_code.set(product[0])
            self.var_product_name.set(product[1])
            self.var_product_type.set(product[2])
            self.var_product_size.set(product[3])
            self.var_selling_price.set(product[4])
