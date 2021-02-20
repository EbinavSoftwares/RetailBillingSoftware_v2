import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

from babel.numbers import format_currency
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.LkpProductName import LkpProductName
from sshp.models.LkpProductSize import LkpProductSize
from sshp.models.LkpProductType import LkpProductType
from sshp.models.Product import Product
from sshp.models.Purchase import Purchase
from sshp.models.Sales import Sales
from sshp.models.Stock import Stock
from sshp.utilities.MaxLengthEntry import MaxLengthEntry


class ViewPurchaseForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - View Purchase")

        # variables
        self.selected_row = list()
        self.garment_list = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()

        # widgets
        self.from_date = None
        self.to_date = None
        self.ety_filter_product_code_1 = None
        self.ety_filter_product_code_2 = None
        self.ety_filter_product_code_3 = None
        self.ety_filter_product_code_4 = None
        self.ety_filter_garment_name = None
        self.ety_filter_product_name = None
        self.ety_filter_product_type = None
        self.ety_filter_product_size = None
        self.ety_filter_product_sell_price = None
        self.purchase_tree = None
        self.summary_tree = None

        # widget variables
        self.var_purchase_date = tk.StringVar()
        self.var_garment_name = tk.StringVar()
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        self.var_quantity = tk.IntVar()
        self.var_amount = tk.DoubleVar()

        self.var_include_date = tk.IntVar()
        self.var_search_product_code_1 = tk.StringVar()
        self.var_search_product_code_2 = tk.StringVar()
        self.var_search_product_code_3 = tk.StringVar()
        self.var_search_product_code_4 = tk.StringVar()
        self.var_total_quantity = tk.IntVar()
        self.var_total_amount = tk.StringVar()

        self.load_view_purchase_form()

    def load_view_purchase_form(self):
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.show_menu(MainForm.is_admin_user)
        self.update_username()

        self.reload_lookup()

        # ********** Sub Containers *********
        top_container = tk.Frame(self.content_container, padx=2, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        top_container.pack(fill='both', expand=True, side=tk.TOP)

        bottom_container = tk.Frame(self.content_container, padx=2, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        bottom_container.pack(fill='both', expand=True, side=tk.TOP)

        # top_container elements
        top_button_container = tk.Frame(top_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        purchase_tree_container = tk.Frame(top_container, bd=2, pady=3, bg=self.clr_yellow, relief=tk.RIDGE)
        purchase_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        # bottom_container elements
        purchase_details_container = tk.Frame(bottom_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        purchase_details_container.pack(fill='both', expand=True, side=tk.LEFT)

        purchase_summary_container = tk.Frame(bottom_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        purchase_summary_container.pack(fill='both', expand=True, anchor='w', side=tk.RIGHT)

        purchase_summary_tree_container = tk.Frame(bottom_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        purchase_summary_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # ********** top_button_container elements *********
        lbl_from_date = tk.Label(top_button_container, text='From Date:', bg=self.clr_yellow)
        lbl_from_date.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.from_date = DateEntry(top_button_container, date_pattern='yyyy-mm-dd', background='yellow',
                                   foreground='black', borderwidth=2, width=10)
        self.from_date.grid(row=1, column=0, sticky="sw", padx=2, pady=1, ipady=3)

        lbl_to_date = tk.Label(top_button_container, text='To Date:', bg=self.clr_yellow)
        lbl_to_date.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.to_date = DateEntry(top_button_container, date_pattern='yyyy-mm-dd', background='yellow',
                                 foreground='black', borderwidth=2, width=10)
        self.to_date.grid(row=1, column=1, sticky="sw", padx=2, pady=1, ipady=3)

        lbl_search_product_code = tk.Label(top_button_container, text="Product Code:", bg=self.clr_yellow)
        lbl_search_product_code.grid(row=0, column=2, columnspan=3, sticky="nw", padx=1, pady=1)

        self.ety_filter_product_code_1 = MaxLengthEntry(top_button_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_1)
        self.ety_filter_product_code_1.grid(row=1, column=2, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_1.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_filter_product_code_2 = MaxLengthEntry(top_button_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_2)
        self.ety_filter_product_code_2.grid(row=1, column=3, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_2.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_filter_product_code_3 = MaxLengthEntry(top_button_container, maxlength=2, width=3,
                                                        textvariable=self.var_search_product_code_3)
        self.ety_filter_product_code_3.grid(row=1, column=4, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_3.bind('<Return>', lambda event: self.validate_entry(event, 2))

        self.ety_filter_product_code_4 = MaxLengthEntry(top_button_container, maxlength=4, width=5,
                                                        textvariable=self.var_search_product_code_4)
        self.ety_filter_product_code_4.grid(row=1, column=5, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_4.bind('<Return>', lambda event: self.validate_entry(event, 4))

        filter_lbl_garment_name = tk.Label(top_button_container, text="Garment Name:", bg=self.clr_yellow)
        filter_lbl_garment_name.grid(row=0, column=6, sticky="nw", padx=1, pady=1)
        self.ety_filter_garment_name = AutocompleteEntry(top_button_container, width=15,
                                                         completevalues=self.garment_list)
        self.ety_filter_garment_name.grid(row=1, column=6, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_garment_name.bind("<Return>", lambda event: self.filter_purchase(event))

        filter_lbl_product_name = tk.Label(top_button_container, text="Name:", bg=self.clr_yellow)
        filter_lbl_product_name.grid(row=0, column=7, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_name = AutocompleteEntry(top_button_container, width=18,
                                                         completevalues=self.product_name_list)
        self.ety_filter_product_name.grid(row=1, column=7, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_name.bind("<Return>", lambda event: self.filter_purchase(event))

        filter_lbl_product_type = tk.Label(top_button_container, text="Type:", bg=self.clr_yellow)
        filter_lbl_product_type.grid(row=0, column=8, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_type = AutocompleteEntry(top_button_container, width=20,
                                                         completevalues=self.product_type_list)
        self.ety_filter_product_type.grid(row=1, column=8, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_type.bind("<Return>", lambda event: self.filter_purchase(event))

        filter_lbl_product_size = tk.Label(top_button_container, text="Size:", bg=self.clr_yellow)
        filter_lbl_product_size.grid(row=0, column=9, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_size = AutocompleteEntry(top_button_container, width=12,
                                                         completevalues=self.product_size_list)
        self.ety_filter_product_size.grid(row=1, column=9, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_size.bind("<Return>", lambda event: self.filter_purchase(event))

        filter_lbl_product_price = tk.Label(top_button_container, text="Price:", bg=self.clr_yellow)
        filter_lbl_product_price.grid(row=0, column=10, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_sell_price = AutocompleteEntry(top_button_container, width=10,
                                                               completevalues=self.product_sell_price_list)
        self.ety_filter_product_sell_price.grid(row=1, column=10, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_sell_price.bind("<Return>", lambda event: self.filter_purchase(event))

        chk_include_date = tk.Checkbutton(top_button_container, text='Include Date', variable=self.var_include_date,
                                          onvalue=1, offvalue=0, bg=self.clr_yellow)
        chk_include_date.grid(row=0, column=11, columnspan=2, sticky="sw", padx=2, pady=1)

        btn_filter = tk.Button(top_button_container, text="Apply Filter", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_purchase)
        btn_filter.grid(row=1, column=11, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(top_button_container, text="Clear", command=self.reload_purchase)
        btn_clear_filter.grid(row=1, column=12, sticky="news", padx=2, pady=1)

        # ********** tree_containers elements *********
        header = ('#', 'PURCHASE_DATE', 'GARMENT_NAME', 'PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE',
                  'SIZE', 'PRICE', 'QTY', 'AMOUNT', '')
        self.purchase_tree = ttk.Treeview(purchase_tree_container, columns=header, height=8, show="headings",
                                          selectmode="browse")
        vsb = ttk.Scrollbar(purchase_tree_container, orient="vertical", command=self.purchase_tree.yview)
        hsb = ttk.Scrollbar(purchase_tree_container, orient="horizontal", command=self.purchase_tree.xview)

        self.purchase_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.purchase_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.purchase_tree.grid(column=0, row=0, sticky='nsew', in_=purchase_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=purchase_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=purchase_tree_container)

        purchase_tree_container.grid_columnconfigure(0, weight=1)
        purchase_tree_container.grid_rowconfigure(0, weight=1)

        self.purchase_tree.heading("0", text="#")
        self.purchase_tree.heading("1", text="PURCHASE_DATE")
        self.purchase_tree.heading("2", text="GARMENT_NAME")
        self.purchase_tree.heading("3", text="PRODUCT_CODE")
        self.purchase_tree.heading("4", text="PRODUCT_NAME")
        self.purchase_tree.heading("5", text="PRODUCT_TYPE")
        self.purchase_tree.heading("6", text="SIZE")
        self.purchase_tree.heading("7", text="PRICE")
        self.purchase_tree.heading("8", text="QTY")
        self.purchase_tree.heading("9", text="AMOUNT")

        self.purchase_tree.column(0, anchor='center', width="20")
        self.purchase_tree.column(1, anchor=tk.W, width="120")
        self.purchase_tree.column(2, anchor=tk.W, width="200")
        self.purchase_tree.column(3, anchor=tk.W, width="120")
        self.purchase_tree.column(4, anchor=tk.W, width="140")
        self.purchase_tree.column(5, anchor=tk.W, width="180")
        self.purchase_tree.column(6, anchor='center', width="80")
        self.purchase_tree.column(7, anchor=tk.E, width="80")
        self.purchase_tree.column(8, anchor='center', width="50")
        self.purchase_tree.column(9, anchor=tk.E, width="120")
        self.purchase_tree.column(10, anchor='center', width="2")

        self.reload_purchase()

        numeric_cols = ['#', 'PRICE', 'QTY', 'AMOUNT']
        for col in header:
            if col in numeric_cols:
                self.purchase_tree.heading(col, text=col,
                                           command=lambda _col=col: self.sort_treeview(
                                               self.purchase_tree, _col,
                                               numeric_sort=True, reverse=False))
            else:
                self.purchase_tree.heading(col, text=col,
                                           command=lambda _col=col: self.sort_treeview(
                                               self.purchase_tree, _col,
                                               numeric_sort=False, reverse=False))

        self.purchase_tree.tag_configure("evenrow", background='#fbefcc')
        self.purchase_tree.tag_configure("oddrow", background='white', foreground='black')
        self.purchase_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # ********** Purchase Details *********
        purchase_details_container.grid_columnconfigure(0, weight=1)
        purchase_details_container.grid_columnconfigure(3, weight=1)

        lbl_purchase_details = tk.Label(purchase_details_container, text="Product Details", bg=self.clr_blueiris,
                                        fg="white")
        lbl_purchase_details.grid(row=0, column=1, columnspan=2, sticky="news", padx=3, pady=3)
        lbl_purchase_details.config(font=("Calibri bold", 12))

        lbl_purchase_date = tk.Label(purchase_details_container, text="Purchase Date: ", bg=self.clr_yellow)
        lbl_purchase_date.grid(row=1, column=1, sticky="nw", padx=3, pady=1)
        ety_purchase_date = tk.Entry(purchase_details_container, width=15, textvariable=self.var_purchase_date,
                                     state='disabled')
        ety_purchase_date.grid(row=1, column=2, sticky="nw", padx=3, pady=1)

        lbl_garment_name = tk.Label(purchase_details_container, text="Garment Name: ", bg=self.clr_yellow)
        lbl_garment_name.grid(row=2, column=1, sticky="nw", padx=3, pady=1)
        ety_garment_name = tk.Entry(purchase_details_container, textvariable=self.var_garment_name, state='disabled')
        ety_garment_name.grid(row=2, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_code = tk.Label(purchase_details_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_code.grid(row=3, column=1, sticky="nw", padx=3, pady=1)
        ety_product_code = tk.Entry(purchase_details_container, width=15, textvariable=self.var_product_code,
                                    state='disabled')
        ety_product_code.grid(row=3, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(purchase_details_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=4, column=1, sticky="nw", padx=3, pady=1)
        ety_product_name = tk.Entry(purchase_details_container, textvariable=self.var_product_name, state='disabled')
        ety_product_name.grid(row=4, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(purchase_details_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=5, column=1, sticky="nw", padx=3, pady=1)
        ety_product_type = tk.Entry(purchase_details_container, textvariable=self.var_product_type, state='disabled')
        ety_product_type.grid(row=5, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(purchase_details_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=6, column=1, sticky="nw", padx=3, pady=1)
        ety_product_size = tk.Entry(purchase_details_container, width=10, textvariable=self.var_product_size,
                                    state='disabled')
        ety_product_size.grid(row=6, column=2, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(purchase_details_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=7, column=1, sticky="nw", padx=3, pady=1)
        ety_selling_price = tk.Entry(purchase_details_container, width=10, textvariable=self.var_selling_price,
                                     state='disabled')
        ety_selling_price.grid(row=7, column=2, sticky="nw", padx=3, pady=1)

        lbl_quantity = tk.Label(purchase_details_container, text="Quantity: ", bg=self.clr_yellow)
        lbl_quantity.grid(row=8, column=1, sticky="nw", padx=3, pady=1)
        ety_quantity = tk.Entry(purchase_details_container, width=5, textvariable=self.var_quantity, state='disabled')
        ety_quantity.grid(row=8, column=2, sticky="nw", padx=3, pady=1)

        lbl_amount = tk.Label(purchase_details_container, text="Amount: ", bg=self.clr_yellow)
        lbl_amount.grid(row=9, column=1, sticky="nw", padx=3, pady=1)
        ety_amount = tk.Entry(purchase_details_container, width=10, textvariable=self.var_amount, state='disabled')
        ety_amount.grid(row=9, column=2, sticky="nw", padx=3, pady=1)

        purchase_summary_container.grid_columnconfigure(0, weight=1)
        purchase_summary_container.grid_columnconfigure(2, weight=1)

        lbl_purchase_summary = tk.Label(purchase_summary_container, text="Purchase Summary", bg=self.clr_blueiris,
                                        fg="white")
        lbl_purchase_summary.grid(row=0, column=1, sticky="news", padx=3, pady=3)
        lbl_purchase_summary.config(font=("Calibri bold", 14))

        lbl_purchase_date = tk.Label(purchase_summary_container, text="Purchase Date:", bg=self.clr_yellow)
        lbl_purchase_date.grid(row=1, column=1, sticky="nw", padx=3, pady=1)
        ety_purchase_date = tk.Entry(purchase_summary_container, width=12, textvariable=self.var_purchase_date,
                                     state='disabled')
        ety_purchase_date.grid(row=2, column=1, sticky="nw", padx=3, pady=1, ipady=6)

        lbl_total_quantity = tk.Label(purchase_summary_container, text="Total Quantity:", bg=self.clr_yellow)
        lbl_total_quantity.grid(row=3, column=1, sticky="nw", padx=3, pady=1)
        ety_total_quantity = tk.Entry(purchase_summary_container, width=12, textvariable=self.var_total_quantity,
                                      state='disabled')
        ety_total_quantity.grid(row=4, column=1, sticky="nw", padx=3, pady=1, ipady=6)

        lbl_total_amount = tk.Label(purchase_summary_container, text="Total Amount:", bg=self.clr_yellow)
        lbl_total_amount.grid(row=5, column=1, sticky="nw", padx=3, pady=1)
        ety_total_amount = tk.Entry(purchase_summary_container, width=12, textvariable=self.var_total_amount,
                                    state='disabled')
        ety_total_amount.grid(row=6, column=1, sticky="nw", padx=3, pady=1, ipady=6)
        self.var_total_amount.set(format_currency(0, 'INR', locale='en_IN'))

        btn_get_purchase_summary = tk.Button(purchase_summary_container, text="Get Purchase Summary",
                                             bg=self.clr_fuchsia, fg='white', command=self.get_purchase_summary)
        btn_get_purchase_summary.grid(row=7, column=1, sticky="news", padx=3, pady=10)

        # monthly_summary_tree_container
        summary_tree = tk.Frame(purchase_summary_tree_container, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        summary_tree.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'PRODUCT_CODE', 'PRODUCT', 'TYPE', 'SIZE', 'PRICE', 'QTY', 'AMOUNT', '')
        self.summary_tree = ttk.Treeview(summary_tree, columns=header, height=5, show="headings",
                                         selectmode="browse")
        vsb = ttk.Scrollbar(summary_tree, orient="vertical", command=self.summary_tree.yview)
        hsb = ttk.Scrollbar(summary_tree, orient="horizontal", command=self.summary_tree.xview)

        self.summary_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.summary_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        summary_tree.grid_columnconfigure(0, weight=1)
        summary_tree.grid_rowconfigure(0, weight=1)

        self.summary_tree.heading("0", text="#")
        self.summary_tree.heading("1", text="PRODUCT_CODE")
        self.summary_tree.heading("2", text="PRODUCT")
        self.summary_tree.heading("3", text="TYPE")
        self.summary_tree.heading("4", text="SIZE")
        self.summary_tree.heading("5", text="PRICE")
        self.summary_tree.heading("6", text="QTY")
        self.summary_tree.heading("7", text="AMOUNT")
        self.summary_tree.heading("8", text="")

        self.summary_tree.column(0, anchor='center', minwidth=30, width=30)
        self.summary_tree.column(1, anchor=tk.W, minwidth=50, width=120)
        self.summary_tree.column(2, anchor=tk.W, minwidth=80, width=100)  # Product
        self.summary_tree.column(3, anchor=tk.W, minwidth=130, width=130)  # Type
        self.summary_tree.column(4, anchor='center', minwidth=50, width=50)    # Size
        self.summary_tree.column(5, anchor=tk.E, minwidth=60, width=60)  # Price
        self.summary_tree.column(6, anchor='center', minwidth=40, width=40)  # Qty
        self.summary_tree.column(7, anchor=tk.E, minwidth=80, width=80)  # Amount
        self.summary_tree.column(8, anchor='center', width=1)
        self.summary_tree["displaycolumns"] = (0, 1, 2, 3, 4, 5, 6, 7, 8)

        numeric_cols = ['#', 'PRICE', 'QTY', 'AMOUNT']
        for col in header:
            if col in numeric_cols:
                self.summary_tree.heading(col, text=col,
                                          command=lambda _col=col: self.sort_treeview(
                                               self.summary_tree, _col,
                                               numeric_sort=True, reverse=False))
            else:
                self.summary_tree.heading(col, text=col,
                                          command=lambda _col=col: self.sort_treeview(
                                               self.summary_tree, _col,
                                               numeric_sort=False, reverse=False))

        self.summary_tree.tag_configure("evenrow", background='#fbefcc')
        self.summary_tree.tag_configure("oddrow", background='white', foreground='black')

    def get_purchase_summary(self):
        selected_row = self.purchase_tree.item(self.purchase_tree.selection())['values']

        if selected_row:
            sel_purchase_date = str(datetime.strptime(selected_row[1], '%d-%b-%Y'))[:10]
            sel_garment_name = selected_row[2]

            rows = Purchase.get_purchase_summary(purchase_date=sel_purchase_date, garment_name=sel_garment_name)

            self.summary_tree.delete(*self.summary_tree.get_children())
            if rows:
                row_num = 0
                total_quantity = 0
                total_amount = 0.0
                for row in rows:
                    row_num += 1

                    purchase, product = row
                    rw = (
                        row_num, purchase.product_code, product.product_name, product.product_type,
                        product.product_size, round(product.selling_price, 2), purchase.quantity,
                        round(product.selling_price * purchase.quantity, 2))

                    total_quantity = total_quantity + int(purchase.quantity)
                    total_amount = total_amount + float(product.selling_price * purchase.quantity)

                    if row_num % 2 == 0:
                        self.summary_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
                    else:
                        self.summary_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))

                self.var_total_quantity.set(total_quantity)
                self.var_total_amount.set(format_currency(total_amount, 'INR', locale='en_IN'))

    def reload_lookup(self):
        garments = Purchase.get_all_garment_name()
        for garment in garments:
            self.garment_list.append(garment.garment_name)

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

    @staticmethod
    def validate_entry(event=None, length=0):
        if len(event.widget.get().strip()) == length:
            event.widget.tk_focusNext().focus()

    def filter_purchase(self, event=None):
        product_code = f"{self.ety_filter_product_code_1.get().strip()}" \
                       f"-{self.ety_filter_product_code_2.get().strip()}" \
                       f"-{self.ety_filter_product_code_3.get().strip()}" \
                       f"-{self.ety_filter_product_code_4.get().strip()}"
        garment_name = self.ety_filter_garment_name.get().strip()
        product_name = self.ety_filter_product_name.get().strip()
        product_type = self.ety_filter_product_type.get().strip()
        product_size = self.ety_filter_product_size.get().strip()
        selling_price = str(self.ety_filter_product_sell_price.get().strip())

        product_code = product_code.replace("---", "")  # if product code is not entered

        if selling_price:
            selling_price = float(selling_price)
        else:
            selling_price = 0.0

        if product_code == "" and garment_name == "" and product_name == "" and product_type == "" \
                and product_size == "" and selling_price == 0.0 and not self.var_include_date.get():
            self.reload_purchase()
        else:
            if self.var_include_date.get():
                rows = Purchase.search_purchase(from_date=self.from_date.get(),
                                                to_date=self.to_date.get(),
                                                product_code=product_code,
                                                garment_name=garment_name,
                                                product_name=product_name,
                                                product_type=product_type,
                                                product_size=product_size,
                                                selling_price=selling_price)
            else:
                rows = Purchase.search_purchase(product_code=product_code,
                                                garment_name=garment_name,
                                                product_name=product_name,
                                                product_type=product_type,
                                                product_size=product_size,
                                                selling_price=selling_price)

            self.purchase_tree.delete(*self.purchase_tree.get_children())
            if rows:
                row_num = 0
                for row in rows:
                    row_num += 1

                    purchase, product = row
                    purchase_date = datetime.strftime(purchase.purchase_date, '%d-%b-%Y')
                    rw = (
                        row_num, purchase_date, purchase.garment_name, purchase.product_code,
                        product.product_name,
                        product.product_type, product.product_size, round(product.selling_price, 2), purchase.quantity,
                        round(product.selling_price * purchase.quantity, 2))

                    if row_num % 2 == 0:
                        self.purchase_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
                    else:
                        self.purchase_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))
            else:
                pass

    def reload_purchase(self):
        self.var_include_date.set(0)

        self.ety_filter_product_code_1.delete(0, tk.END)
        self.ety_filter_product_code_2.delete(0, tk.END)
        self.ety_filter_product_code_3.delete(0, tk.END)
        self.ety_filter_product_code_4.delete(0, tk.END)

        self.ety_filter_garment_name.delete(0, tk.END)
        self.ety_filter_product_name.delete(0, tk.END)
        self.ety_filter_product_type.delete(0, tk.END)
        self.ety_filter_product_size.delete(0, tk.END)
        self.ety_filter_product_sell_price.delete(0, tk.END)

        self.purchase_tree.delete(*self.purchase_tree.get_children())

        rows = Purchase.get_all_purchase()
        row_num = 0
        for row in rows:
            row_num += 1

            purchase, product = row
            purchase_date = datetime.strftime(purchase.purchase_date, '%d-%b-%Y')
            rw = (row_num, purchase_date, purchase.garment_name, purchase.product_code, product.product_name,
                  product.product_type, product.product_size, round(product.selling_price, 2), purchase.quantity,
                  round(product.selling_price * purchase.quantity, 2))

            if row_num % 2 == 0:
                self.purchase_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
            else:
                self.purchase_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))

    def on_tree_select(self, event):
        self.selected_row = event.widget.selection()

        purchase = self.purchase_tree.item(self.selected_row)['values']

        if purchase:
            self.var_purchase_date.set(purchase[1])
            self.var_garment_name.set(purchase[2])
            self.var_product_code.set(purchase[3])
            self.var_product_name.set(purchase[4])
            self.var_product_type.set(purchase[5])
            self.var_product_size.set(purchase[6])
            self.var_selling_price.set(purchase[7])
            self.var_quantity.set(purchase[8])
            self.var_amount.set(purchase[9])
