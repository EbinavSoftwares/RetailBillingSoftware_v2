import tkinter as tk
from datetime import date
from tkinter import TclError
from tkinter import messagebox
from tkinter import ttk

from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.LkpProductName import LkpProductName
from sshp.models.LkpProductSize import LkpProductSize
from sshp.models.LkpProductType import LkpProductType
from sshp.models.Product import Product
from sshp.models.ProductCategory import ProductCategory
from sshp.models.Stock import Stock
from sshp.models.StockTimeline import StockTimeline
from sshp.utilities.MaxLengthEntry import MaxLengthEntry


class ProductForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - Products")

        # variables
        self.selected_row = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()

        # widgets
        self.update_product_window = None
        self.filter_ety_product_name = None
        self.filter_ety_product_type = None
        self.filter_ety_product_size = None
        self.filter_ety_product_sell_price = None

        self.ety_search_product_code_1 = None
        self.ety_search_product_code_2 = None
        self.ety_search_product_code_3 = None
        self.ety_search_product_code_4 = None

        self.products_tree = None
        self.cbo_activity = None

        # widget variables
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        self.var_quantity = tk.IntVar()
        self.var_change_quantity = tk.IntVar()
        self.var_activity_type = tk.StringVar()

        self.var_search_product_code_1 = tk.StringVar()
        self.var_search_product_code_2 = tk.StringVar()
        self.var_search_product_code_3 = tk.StringVar()
        self.var_search_product_code_4 = tk.StringVar()

        self.var_old_product_code = tk.StringVar()
        self.var_old_product_name = tk.StringVar()
        self.var_old_product_type = tk.StringVar()
        self.var_old_product_size = tk.StringVar()
        self.var_old_selling_price = tk.DoubleVar()

        self.var_new_product_code = tk.StringVar()
        self.var_new_product_name = tk.StringVar()
        self.var_new_product_type = tk.StringVar()
        self.var_new_product_size = tk.StringVar()
        self.var_new_selling_price = tk.DoubleVar()

        self.load_product_form()

        # shortcuts
        self.window.bind("<F1>", lambda event: self.select_first_row(event))

    def load_product_form(self):
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.show_menu(MainForm.is_admin_user)
        self.update_username()

        products = Product.get_product_name_list()
        for product in products:
            self.product_name_list.append(product.product_name)

        products = Product.get_product_type_list()
        for product in products:
            self.product_type_list.append(product.product_type)

        products = Product.get_product_size_list()
        for product in products:
            self.product_size_list.append(product.product_size)

        products = Product.get_product_sell_price_list()
        for product in products:
            self.product_sell_price_list.append(str(round(product.selling_price, 2)))

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        right_container = tk.Frame(self.content_container, bd=5, padx=4, pady=5, relief=tk.RIDGE, bg=self.clr_yellow)
        right_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container elements
        top_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg=self.clr_yellow)
        top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        search_container = tk.Frame(top_button_container, relief=tk.RIDGE, bg=self.clr_yellow)
        search_container.pack(fill='x', expand=True, side=tk.LEFT)

        filter_container = tk.Frame(top_button_container, relief=tk.RIDGE, bg=self.clr_yellow)
        filter_container.pack(fill='x', expand=True, side=tk.RIGHT)

        # ********** left_search_container elements *********
        lbl_search_product_code = tk.Label(search_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_search_product_code.grid(row=0, column=0, columnspan=3, sticky="nw", padx=1, pady=1)

        self.ety_search_product_code_1 = MaxLengthEntry(search_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_1)
        self.ety_search_product_code_1.grid(row=1, column=0, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_1.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_search_product_code_2 = MaxLengthEntry(search_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_2)
        self.ety_search_product_code_2.grid(row=1, column=1, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_2.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_search_product_code_3 = MaxLengthEntry(search_container, maxlength=2, width=3,
                                                        textvariable=self.var_search_product_code_3)
        self.ety_search_product_code_3.grid(row=1, column=2, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_3.bind('<Return>', lambda event: self.validate_entry(event, 2))

        self.ety_search_product_code_4 = MaxLengthEntry(search_container, maxlength=4, width=5,
                                                        textvariable=self.var_search_product_code_4)
        self.ety_search_product_code_4.grid(row=1, column=3, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_4.bind('<Return>', lambda event: self.validate_entry(event, 4))

        btn_search = tk.Button(search_container, text="Search", bg=self.clr_fuchsia, fg='white',
                               command=self.search_product)
        btn_search.grid(row=1, column=4, sticky="sw", padx=2, pady=1)
        btn_search.bind('<Return>', lambda event: self.search_product(event))

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg=self.clr_yellow)
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, width=18,
                                                         completevalues=self.product_name_list)
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg=self.clr_yellow)
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, width=20,
                                                         completevalues=self.product_type_list)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_size = tk.Label(filter_container, text="Size: ", bg=self.clr_yellow)
        filter_lbl_product_size.grid(row=0, column=2, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_size = AutocompleteEntry(filter_container, width=15,
                                                         completevalues=self.product_size_list)
        self.filter_ety_product_size.grid(row=1, column=2, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_size.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_price = tk.Label(filter_container, text="Price: ", bg=self.clr_yellow)
        filter_lbl_product_price.grid(row=0, column=3, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_sell_price = AutocompleteEntry(filter_container, width=10,
                                                               completevalues=self.product_sell_price_list)
        self.filter_ety_product_sell_price.grid(row=1, column=3, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_sell_price.bind("<Return>", lambda event: self.filter_product(event))

        btn_filter = tk.Button(filter_container, text="Apply Filter", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_product)
        btn_filter.grid(row=1, column=4, sticky="news", padx=2, pady=1)
        btn_filter.bind("<Return>", lambda event: self.filter_product(event))

        btn_clear_filter = tk.Button(filter_container, text="Clear", command=self.reload_products)
        btn_clear_filter.grid(row=1, column=5, sticky="news", padx=2, pady=1)
        btn_clear_filter.bind("<Return>", lambda event: self.reload_products(event))

        # ********** tree_containers elements *********
        products_tree_container = tk.Frame(left_container, pady=3, bg=self.clr_yellow, relief=tk.RIDGE)
        products_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE', 'SIZE', 'SELL_PRICE',
                  'QTY', '')
        self.products_tree = ttk.Treeview(products_tree_container, columns=header, height=20, show="headings",
                                          selectmode="browse")
        vsb = ttk.Scrollbar(products_tree_container, orient="vertical", command=self.products_tree.yview)
        hsb = ttk.Scrollbar(products_tree_container, orient="horizontal", command=self.products_tree.xview)

        self.products_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.products_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.products_tree.grid(column=0, row=0, sticky='nsew', in_=products_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=products_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=products_tree_container)

        products_tree_container.grid_columnconfigure(0, weight=1)
        products_tree_container.grid_rowconfigure(0, weight=1)

        self.products_tree.heading("0", text="#")
        self.products_tree.heading("1", text="PRODUCT_CODE")
        self.products_tree.heading("2", text="PRODUCT_NAME")
        self.products_tree.heading("3", text="PRODUCT_TYPE")
        self.products_tree.heading("4", text="SIZE")
        self.products_tree.heading("5", text="SELL_PRICE")
        self.products_tree.heading("6", text="QTY")

        self.products_tree.column(0, anchor='center', width="20")
        self.products_tree.column(1, anchor='center', width="120")
        self.products_tree.column(2, anchor=tk.W, width="120")
        self.products_tree.column(3, anchor=tk.W, width="150")
        self.products_tree.column(4, anchor='center', width="80")
        self.products_tree.column(5, anchor=tk.E, width="80")
        self.products_tree.column(6, anchor='center', width="50")
        self.products_tree.column(7, anchor='center', width="2")

        self.reload_products()

        numeric_cols = ['#', 'PRICE', 'QTY']
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

        self.products_tree.tag_configure("evenrow_active", background='#fbefcc')
        self.products_tree.tag_configure("oddrow_active", background='white', foreground='black')
        self.products_tree.tag_configure("evenrow_inactive", background='#fbefcc', foreground='red')
        self.products_tree.tag_configure("oddrow_inactive", background='white', foreground='red')
        self.products_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # ********** Product Details *********
        product_details_container = tk.Frame(right_container, pady=3, padx=3, relief=tk.RIDGE, bg=self.clr_yellow)
        product_details_container.pack(fill='both', expand=True, side=tk.LEFT)

        product_details_container.grid_columnconfigure(0, weight=1)
        product_details_container.grid_columnconfigure(4, weight=1)

        lbl_product_details = tk.Label(product_details_container, text="Product Details", bg=self.clr_blueiris,
                                       fg="white")
        lbl_product_details.grid(row=0, column=0, columnspan=3, sticky="news", padx=3, pady=5)
        lbl_product_details.config(font=("Calibri bold", 14))

        lbl_product_code = tk.Label(product_details_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_code.grid(row=1, column=0, sticky="nw", padx=3, pady=1)
        product_code = tk.Entry(product_details_container, width=15, textvariable=self.var_product_code,
                                state='disabled')
        product_code.grid(row=1, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(product_details_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=2, column=0, sticky="nw", padx=3, pady=1)
        product_name = tk.Entry(product_details_container, textvariable=self.var_product_name,
                                state='disabled')
        product_name.grid(row=2, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(product_details_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=3, column=0, sticky="nw", padx=3, pady=1)
        product_type = tk.Entry(product_details_container, textvariable=self.var_product_type, state='disabled')
        product_type.grid(row=3, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(product_details_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=4, column=0, sticky="nw", padx=3, pady=1)
        product_size = tk.Entry(product_details_container, width=12, textvariable=self.var_product_size,
                                state='disabled')
        product_size.grid(row=4, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(product_details_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=5, column=0, sticky="nw", padx=3, pady=1)
        selling_price = tk.Entry(product_details_container, width=8, textvariable=self.var_selling_price,
                                 state='disabled')
        selling_price.grid(row=5, column=1, sticky="nw", padx=3, pady=1)

        lbl_quantity = tk.Label(product_details_container, text="Quantity: ", bg=self.clr_yellow)
        lbl_quantity.grid(row=8, column=0, sticky="nw", padx=3, pady=1)
        quantity = tk.Entry(product_details_container, width=8, textvariable=self.var_quantity, state='disabled')
        quantity.grid(row=8, column=1, sticky="nw", padx=3, pady=1)

        # since self.load_activity has to be called
        lbl_activity = tk.Label(product_details_container, text="Activity: ", bg=self.clr_yellow)
        lbl_activity.grid(row=10, column=0, sticky="nw", padx=3, pady=1)
        self.cbo_activity = ttk.Combobox(product_details_container, width=15, values=self.plus_activity)
        self.cbo_activity.grid(row=10, column=1, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_activity_type = tk.Label(product_details_container, text="Activity Type: ", bg=self.clr_yellow)
        lbl_activity_type.grid(row=9, column=0, sticky="nw", padx=3, pady=1)
        rdo_plus = tk.Radiobutton(product_details_container, text="Plus", variable=self.var_activity_type,
                                  value="plus", command=lambda: self.load_activity("plus"), bg=self.clr_yellow)
        rdo_plus.grid(row=9, column=1, sticky="nw", padx=3, pady=1)
        rdo_plus.invoke()

        rdo_minus = tk.Radiobutton(product_details_container, text="Minus", variable=self.var_activity_type,
                                   value="minus", command=lambda: self.load_activity("minus"), bg=self.clr_yellow)
        rdo_minus.grid(row=9, column=2, sticky="nw", padx=3, pady=1)

        lbl_change = tk.Label(product_details_container, text="Change: ", bg=self.clr_yellow)
        lbl_change.grid(row=11, column=0, sticky="nw", padx=3, pady=1)
        change = tk.Entry(product_details_container, width=8, textvariable=self.var_change_quantity)
        change.grid(row=11, column=1, sticky="nw", padx=3, pady=1)

        btn_update_stock = tk.Button(product_details_container, text="Update [S]tock",  bg=self.clr_fuchsia, fg='white',
                                     command=self.update_stock)
        btn_update_stock.grid(row=12, column=1, columnspan=2, sticky="news", padx=3, pady=1)

        btn_update_product = tk.Button(product_details_container, text="Update [P]roduct", bg=self.clr_blueiris,
                                       fg='white', command=self.load_update_product_window)
        btn_update_product.grid(row=13, column=1, columnspan=2, sticky="news", padx=3, pady=1)

        btn_update_product_status = tk.Button(product_details_container, text="Activate / De-Activate",
                                              bg=self.clr_limegreen, fg='white', command=self.update_product_status)
        btn_update_product_status.grid(row=14, column=1, columnspan=2, sticky="news", padx=3, pady=1)

        btn_delete_product = tk.Button(product_details_container, text="Delete Product",
                                       bg=self.clr_fuchsia, fg='white', command=self.delete_product)
        btn_delete_product.grid(row=15, column=1, columnspan=2, sticky="news", padx=3, pady=1)

    def delete_product(self):
        product_code = self.var_product_code.get().strip()

        try:
            quantity = self.var_quantity.get()
        except TclError:
            quantity = 0

        if product_code == "":
            return

        if quantity != 0:
            messagebox.showerror("SS Fashion Tuty", f"Existing quantity must be '0'")
            print(f"Existing quantity must be '0'")
            return

        activity = "Delete Product"
        StockTimeline.add_timeline(entry_date=date.today(), product_code=product_code, activity=activity,
                                   change="+0")
        Stock.delete_stock_entry(product_code=product_code)
        Product.delete_product_entry(product_code=product_code)

        messagebox.showerror("SS Fashion Tuty", f"Product Code: '{product_code}' has been deleted!")
        print(f"Product Code: '{product_code}' has been deleted!")

        self.reload_products()

    def update_product_status(self):
        product_code = self.var_product_code.get().strip()
        quantity = self.var_quantity.get()

        if product_code == "":
            return

        if quantity != 0:
            messagebox.showerror("SS Fashion Tuty", f"Existing quantity must be '0'")
            print(f"Existing quantity must be '0'")
            return

        status = Product.get_product_status(product_code=product_code)
        if status:
            Product.deactivate_product(product_code)
        else:
            Product.activate_product(product_code)

        self.reload_products()

    def load_update_product_window(self, event=None):
        selected_row = self.products_tree.item(self.products_tree.selection())['values']
        if isinstance(selected_row, str):
            return

        self.var_old_product_code.set(selected_row[1])
        self.var_old_product_name.set(selected_row[2])
        self.var_old_product_type.set(selected_row[3])
        self.var_old_product_size.set(selected_row[4])
        self.var_old_selling_price.set(selected_row[5])

        self.var_new_product_code.set(selected_row[1])
        self.var_new_product_name.set(selected_row[2])
        self.var_new_product_type.set(selected_row[3])
        self.var_new_product_size.set(selected_row[4])
        self.var_new_selling_price.set(selected_row[5])

        self.window.wm_attributes("-disabled", True)

        self.update_product_window = tk.Toplevel(self.window)
        self.update_product_window.overrideredirect(True)
        self.update_product_window.bind("<FocusOut>", self.on_focus_out_update_product_window)

        main_container = tk.Frame(self.update_product_window, bd=20, padx=10, pady=5, relief=tk.RIDGE,
                                  bg=self.clr_limegreen)
        main_container.pack(expand=True, side=tk.TOP, anchor="n")

        top_container = tk.Frame(main_container, bd=5, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_blueiris)
        top_container.pack(fill='x', expand=True, side=tk.TOP, anchor="n")

        lbl_heading = tk.Label(top_container, text="Update Product Details", bg=self.clr_blueiris, fg="white")
        lbl_heading.grid(row=0, column=0, sticky="news", pady=3)
        lbl_heading.config(font=("Calibri bold", 14))

        content_container = tk.Frame(main_container, relief=tk.RIDGE)
        content_container.pack(expand=True, side=tk.TOP, anchor="n")

        left_container = tk.Frame(content_container, bd=5, padx=10, pady=5, relief=tk.RIDGE, bg="light grey")
        left_container.pack(expand=True, side=tk.LEFT, anchor="n")

        right_container = tk.Frame(content_container, bd=5, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_yellow)
        right_container.pack(expand=True, side=tk.RIGHT, anchor="n")

        bottom_container = tk.Frame(main_container, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_limegreen)
        bottom_container.pack(expand=True, side=tk.BOTTOM, anchor="n")

        lbl_product_details = tk.Label(left_container, text="Old Product Details", bg=self.clr_blueiris, fg="white")
        lbl_product_details.grid(row=0, column=0, columnspan=2, sticky="news", pady=3)
        lbl_product_details.config(font=("Calibri bold", 14))

        lbl_product_code = tk.Label(left_container, text="Product Code: ", bg="light grey")
        lbl_product_code.grid(row=1, column=0, sticky="nw", padx=3, pady=1)
        ety_product_code = tk.Entry(left_container, text=self.var_old_product_code, state='disabled')
        ety_product_code.grid(row=1, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(left_container, text="Product Name: ", bg="light grey")
        lbl_product_name.grid(row=2, column=0, sticky="nw", padx=3, pady=1)
        ety_product_name = tk.Entry(left_container, text=self.var_old_product_name, state='disabled')
        ety_product_name.grid(row=2, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(left_container, text="Product Type: ", bg="light grey")
        lbl_product_type.grid(row=3, column=0, sticky="nw", padx=3, pady=1)
        ety_product_type = tk.Entry(left_container, textvariable=self.var_old_product_type,
                                    state='disabled')
        ety_product_type.grid(row=3, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(left_container, text="Size: ", bg="light grey")
        lbl_product_size.grid(row=4, column=0, sticky="nw", padx=3, pady=1)
        ety_product_size = tk.Entry(left_container, width=10, textvariable=self.var_old_product_size,
                                    state='disabled')
        ety_product_size.grid(row=4, column=1, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(left_container, text="Price: ", bg="light grey")
        lbl_selling_price.grid(row=5, column=0, sticky="nw", padx=3, pady=1)
        ety_selling_price = tk.Entry(left_container, width=10, textvariable=self.var_old_selling_price,
                                     state='disabled')
        ety_selling_price.grid(row=5, column=1, sticky="nw", padx=3, pady=1)

        # New Product Details
        lbl_product_details = tk.Label(right_container, text="New Product Details", bg=self.clr_blueiris, fg="white")
        lbl_product_details.grid(row=0, column=0, columnspan=2, sticky="news", padx=3, pady=3)
        lbl_product_details.config(font=("Calibri bold", 14))

        lbl_product_code = tk.Label(right_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_code.grid(row=1, column=0, sticky="nw", padx=3, pady=1)
        ety_product_code = tk.Entry(right_container, text=self.var_new_product_code, state='disabled')
        ety_product_code.grid(row=1, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(right_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=2, column=0, sticky="nw", padx=3, pady=1)
        ety_product_name = tk.Entry(right_container, textvariable=self.var_new_product_name)
        ety_product_name.grid(row=2, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(right_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=3, column=0, sticky="nw", padx=3, pady=1)
        ety_product_type = tk.Entry(right_container, textvariable=self.var_new_product_type)
        ety_product_type.grid(row=3, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(right_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=4, column=0, sticky="nw", padx=3, pady=1)
        ety_product_size = tk.Entry(right_container, width=10, textvariable=self.var_new_product_size)
        ety_product_size.grid(row=4, column=1, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(right_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=5, column=0, sticky="nw", padx=3, pady=1)
        ety_selling_price = tk.Entry(right_container, width=10, textvariable=self.var_new_selling_price)
        ety_selling_price.grid(row=5, column=1, sticky="nw", padx=3, pady=1)

        btn_close = tk.Button(bottom_container, text='Close', width=10,
                              command=self.close_update_product_window)
        btn_close.grid(row=0, column=0, padx=5, pady=20)

        btn_save_changes = tk.Button(bottom_container, text='Save Changes', bg=self.clr_fuchsia, fg='white',
                                     command=self.update_product)
        btn_save_changes.grid(row=0, column=1, padx=5, pady=20)

        # Gets the requested values of the height and width.
        window_width = self.window.winfo_reqwidth() / 2
        window_height = self.window.winfo_reqheight() / 2

        # Gets both half the screen width/height and window width/height
        position_right = int(self.update_product_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.update_product_window.winfo_screenheight() / 2 - window_height / 2)
        # print(window_width, window_height, position_right, position_down)

        # Positions the window in the center of the page.
        self.update_product_window.geometry("+{}+{}".format(position_right, position_down))

    def on_focus_out_update_product_window(self):
        print("on_focus_out_update_product_window")
        self.window.wm_attributes("-disabled", False)
        self.update_product_window.destroy()

    def update_product(self):
        old_product_code = self.var_old_product_code.get().strip()
        old_product_name = self.var_old_product_name.get().strip()
        old_product_type = self.var_old_product_type.get().strip()
        old_product_size = self.var_old_product_size.get().strip()
        old_selling_price = self.var_old_selling_price.get()

        new_product_name = self.var_new_product_name.get().strip()
        new_product_type = self.var_new_product_type.get().strip()
        new_product_size = self.var_new_product_size.get().strip()

        try:
            new_selling_price = round(float(self.var_new_selling_price.get()), 2)
        except (ValueError, TclError):
            new_selling_price = 0.0

        actual_price = 0.0

        if old_product_name == new_product_name and old_product_type == new_product_type \
                and old_product_size == new_product_size and old_selling_price == new_selling_price:
            print(f"No Change detected!")
            return

        if len(new_product_name) == 0:
            messagebox.showerror("SS Fashion Tuty", f"Product_Name is missing!")
            print(f"Product_Name is missing!")
            return

        if new_selling_price == "" or new_selling_price <= 0:
            messagebox.showerror("SS Fashion Tuty", f"Selling Price is missing!")
            print(f"selling price is missing!")
            return

        if len(new_product_type) == 0:
            new_product_type = "-"

        if len(new_product_size) == 0:
            new_product_size = "-"

        product_name_code = LkpProductName.get_code(product_name=new_product_name)
        if product_name_code is None:
            product_category = ProductCategory.get_category_by_code(old_product_code[:3])
            product_name_code = LkpProductName.create_lookup(new_product_name, product_category)

        product_type_code = LkpProductType.get_code(product_type=new_product_type)
        if product_type_code is None:
            product_type_code = LkpProductType.create_lookup(new_product_type)

        product_size_code = LkpProductSize.get_code(product_size=new_product_size)
        if product_size_code is None:
            product_size_code = LkpProductSize.create_lookup(new_product_size)

        product_price_code = str(int(new_selling_price)).zfill(4)
        new_product_code = f"{product_name_code}-{product_type_code}-{product_size_code}-{product_price_code}"

        product = (new_product_code, new_product_name, new_product_type, new_product_size, new_selling_price,
                   actual_price)
        product_list = Product.search_products(new_product_code, new_product_name, new_product_type, new_product_size,
                                               new_selling_price)
        if product_list:
            print(f"Product: '{product}' is already exists!")
            messagebox.showerror("SS Fashion Tuty", f"Product already exists! \nProduct_Code: {new_product_code}")

            self.close_update_product_window()
        else:
            # New Product update
            Product.add_product(product)

            old_product = Stock.get_stock(old_product_code)
            old_product_quantity = old_product.quantity
            stock = (new_product_code, old_product_quantity)
            Stock.update_stock(stock)

            change = str(old_product_quantity)
            StockTimeline.add_timeline(date.today(), new_product_code, "Product Update", change)

            # Old Product update
            stock = (old_product_code, 0)
            Stock.update_stock(stock)

            Product.deactivate_product(old_product_code)

            if str(old_product_quantity)[:1] == "-":
                change = '+' + str(old_product_quantity)[1:]
            else:
                change = '-' + str(old_product_quantity)

            StockTimeline.add_timeline(date.today(), old_product_code, "Product Update", change)

            self.reload_products()

            print(f"Product: {product} is updated!")
            messagebox.showinfo("SS Fashion Tuty", f"Product details are updated! \nProduct_Code: {new_product_code}")

            self.close_update_product_window()

            product = Product.search_products(product_code=new_product_code)
            if product:
                self.products_tree.selection_set(self.products_tree.tag_has(product.product_code))
                self.products_tree.focus_set()

    def close_update_product_window(self):
        self.window.wm_attributes("-disabled", False)
        self.update_product_window.destroy()

    def load_activity(self, activity_type):
        self.cbo_activity.set("")
        self.var_change_quantity.set(0)

        if activity_type == "plus":
            self.cbo_activity['values'] = self.plus_activity
        elif activity_type == "minus":
            self.cbo_activity['values'] = self.minus_activity
        else:
            self.cbo_activity['values'] = list()

    def select_first_row(self, event=None):
        element_id = self.products_tree.get_children()[0]
        self.products_tree.focus_set()
        self.products_tree.focus(element_id)
        self.products_tree.selection_set(element_id)

    @staticmethod
    def validate_entry(event=None, length=0):
        if len(event.widget.get().strip()) == length:
            event.widget.tk_focusNext().focus()

    def filter_product(self, event=None):
        product_name = self.filter_ety_product_name.get().strip()
        product_type = self.filter_ety_product_type.get().strip()
        product_size = self.filter_ety_product_size.get().strip()
        selling_price = str(self.filter_ety_product_sell_price.get().strip())
        if selling_price:
            selling_price = float(selling_price)
        else:
            selling_price = 0.0

        rows = Stock.search_stock(product_name=product_name,
                                  product_type=product_type,
                                  product_size=product_size,
                                  selling_price=selling_price)
        self.products_tree.delete(*self.products_tree.get_children())

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
                      round(product.selling_price, 2), quantity)

                if sl_no % 2 == 0:
                    self.products_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
                else:
                    self.products_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))
        else:
            pass

    def update_stock(self):
        product_code = self.var_product_code.get().strip()
        activity = self.cbo_activity.get().strip()
        try:
            quantity = self.var_quantity.get()
        except TclError:
            quantity = 0

        if product_code == "":
            return

        if activity not in self.plus_activity and activity not in self.minus_activity:
            messagebox.showerror("SS Fashion Tuty", f"Invalid Activity Type! Please select from drop-down!")
            print(f"Invalid Activity Type! Please select from drop-down!")
            return

        try:
            change_quantity = round(self.var_change_quantity.get(), 0)
        except TclError:
            change_quantity = 0

        if change_quantity == "" or change_quantity < 1:
            messagebox.showerror("SS Fashion Tuty", f"Invalid Change Quantity!")
            print(f"Invalid Change Quantity!")
            return

        new_quantity = 0
        change = ""
        if self.var_activity_type.get() == "plus":
            new_quantity = quantity + change_quantity
            change = '+' + str(change_quantity)
        elif self.var_activity_type.get() == "minus":
            new_quantity = quantity - change_quantity
            change = '-' + str(change_quantity)

        stock = (product_code, new_quantity)
        Stock.update_stock(stock)

        StockTimeline.add_timeline(date.today(), product_code, activity, change)

        self.reload_products()

        self.var_quantity.set(new_quantity)

        messagebox.showinfo("SS Fashion Tuty", f"Product: '{product_code}' is updated!")
        print(f"product: '{product_code}' is updated!")

    def search_product(self, event=None):
        product_code = f"{self.ety_search_product_code_1.get().strip()}" \
                       f"-{self.ety_search_product_code_2.get().strip()}" \
                       f"-{self.ety_search_product_code_3.get().strip()}" \
                       f"-{self.ety_search_product_code_4.get().strip()}"

        if product_code != "---":
            products = Product.search_products(product_code=product_code)
            if products is None:
                messagebox.showerror("SS Fashion Tuty", f"Product_code: {product_code} not found!")
                print(f"Product_code: {product_code} not found!")
            else:
                if isinstance(products, Product):
                    self.products_tree.selection_set(self.products_tree.tag_has(str(products.product_code)))
                    self.products_tree.focus_set()
                    self.products_tree.focus(self.selected_row)
                else:
                    self.products_tree.delete(*self.products_tree.get_children())
                    row_num = 0
                    for product in products:
                        row_num += 1
                        row = (product.product_code, product.product_name, product.product_type, product.product_size,
                               round(product.selling_price, 2), round(product.actual_price, 2))

                        if row_num % 2 == 0:
                            self.products_tree.insert("", tk.END, values=row, tags=('evenrow', product.product_code))
                        else:
                            self.products_tree.insert("", tk.END, values=row, tags=('oddrow', product.product_code))

    def reload_products(self, event=None):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)
        self.filter_ety_product_size.delete(0, tk.END)
        self.filter_ety_product_sell_price.delete(0, tk.END)

        self.products_tree.delete(*self.products_tree.get_children())

        rows = Stock.get_all_stocks()
        row_num = 0
        for row in rows:
            product = row.Product
            stock = row.Stock

            row_num = row_num + 1
            quantity = "-"
            if stock:
                quantity = stock.quantity

            rw = (row_num, product.product_code, product.product_name, product.product_type, product.product_size,
                  round(product.selling_price, 2), quantity)

            if row_num % 2 == 0:
                if product.is_active:
                    self.products_tree.insert("", tk.END, values=rw, tags=(
                        'evenrow_active',
                        product.product_code
                    ))
                else:
                    self.products_tree.insert("", tk.END, values=rw, tags=(
                        'evenrow_inactive',
                        product.product_code
                    ))
            else:
                if product.is_active:
                    self.products_tree.insert("", tk.END, values=rw, tags=(
                        'oddrow_active', product.product_code
                    ))
                else:
                    self.products_tree.insert("", tk.END, values=rw, tags=(
                        'oddrow_inactive',
                        product.product_code
                    ))

    def on_tree_select(self, event):
        self.selected_row = event.widget.selection()

        product = self.products_tree.item(self.selected_row)['values']

        if product:
            self.var_product_code.set(product[1])
            self.var_product_name.set(product[2])
            self.var_product_type.set(product[3])
            self.var_product_size.set(product[4])
            self.var_selling_price.set(product[5])
            self.var_quantity.set(product[6])
