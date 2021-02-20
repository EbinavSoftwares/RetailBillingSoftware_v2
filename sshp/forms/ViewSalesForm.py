import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

from babel.numbers import format_currency
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.Product import Product
from sshp.models.Sales import Sales
from sshp.utilities.MaxLengthEntry import MaxLengthEntry


class ViewSalesForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - View Sales")

        # variables
        self.selected_row = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()
        self.billno_list = list()

        # widgets
        self.ety_filter_product_name = None
        self.ety_filter_product_type = None
        self.ety_filter_product_size = None
        self.ety_filter_product_sell_price = None
        self.ety_filter_bill_number = None
        self.ety_filter_product_code_1 = None
        self.ety_filter_product_code_2 = None
        self.ety_filter_product_code_3 = None
        self.ety_filter_product_code_4 = None
        self.sales_tree = None
        self.from_date = None
        self.to_date = None
        self.sales_from_date = None
        self.sales_to_date = None

        # widget variables
        self.var_sales_date = tk.StringVar()
        self.var_bill_number = tk.StringVar()
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        self.var_quantity = tk.IntVar()
        self.var_sold_quantity = tk.IntVar()
        self.var_sales_amount = tk.DoubleVar()
        self.var_search_product_code_1 = tk.StringVar()
        self.var_search_product_code_2 = tk.StringVar()
        self.var_search_product_code_3 = tk.StringVar()
        self.var_search_product_code_4 = tk.StringVar()
        self.var_chk_include_date = tk.IntVar()

        self.load_view_sales_form()

    def load_view_sales_form(self):
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

        bills = Sales.get_bill_number_list()
        for bill in bills:
            self.billno_list.append(str(bill.bill_number))

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=2, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        right_container = tk.Frame(self.content_container, padx=2, relief=tk.RIDGE, bg=self.clr_yellow)
        right_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container main elements
        button_container = tk.Frame(left_container, padx=2, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        button_container.pack(fill='both', expand=True, side=tk.TOP)

        sales_tree_container = tk.Frame(left_container, padx=2, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        sales_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        # button_container
        date_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        date_container.pack(fill='both', expand=True, anchor='w', side=tk.LEFT)

        name_filter_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        name_filter_container.pack(fill='both', expand=True, anchor='w', side=tk.TOP)

        code_filter_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        code_filter_container.pack(fill='both', expand=True, anchor='w', side=tk.LEFT)

        billno_filter_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        billno_filter_container.pack(fill='both', expand=True, anchor='w', side=tk.RIGHT)

        # ********** button_container elements *********
        date_container.grid_rowconfigure(0, weight=1)
        date_container.grid_rowconfigure(6, weight=1)

        date_container.grid_columnconfigure(0, weight=1)
        date_container.grid_columnconfigure(2, weight=1)

        lbl_from_date = tk.Label(date_container, text='From Date: ', bg=self.clr_yellow)
        lbl_from_date.grid(row=1, column=1, sticky="nw", padx=1, pady=1)
        self.from_date = DateEntry(date_container, date_pattern='yyyy-mm-dd', background='yellow',
                                   foreground='black', borderwidth=2, width=10)
        self.from_date.grid(row=2, column=1, sticky="sw", padx=2, pady=1, ipady=3)

        lbl_to_date = tk.Label(date_container, text='To Date: ', bg=self.clr_yellow)
        lbl_to_date.grid(row=3, column=1, sticky="nw", padx=1, pady=1)
        self.to_date = DateEntry(date_container, date_pattern='yyyy-mm-dd', background='yellow',
                                 foreground='black', borderwidth=2, width=10)
        self.to_date.grid(row=4, column=1, sticky="sw", padx=2, pady=1, ipady=3)

        include_date = tk.Checkbutton(date_container, text='Include Date', variable=self.var_chk_include_date,
                                      onvalue=1, offvalue=0, bg=self.clr_yellow)
        include_date.grid(row=5, column=1, sticky="sw", padx=2, pady=1)

        # name_filter_container elements
        name_filter_container.grid_rowconfigure(0, weight=1)
        name_filter_container.grid_rowconfigure(3, weight=1)

        name_filter_container.grid_columnconfigure(0, weight=1)
        name_filter_container.grid_columnconfigure(7, weight=1)

        filter_lbl_product_name = tk.Label(name_filter_container, text="Name: ", bg=self.clr_yellow)
        filter_lbl_product_name.grid(row=1, column=1, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_name = AutocompleteEntry(name_filter_container, width=15,
                                                         completevalues=self.product_name_list)
        self.ety_filter_product_name.grid(row=2, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_name.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_type = tk.Label(name_filter_container, text="Type: ", bg=self.clr_yellow)
        filter_lbl_product_type.grid(row=1, column=2, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_type = AutocompleteEntry(name_filter_container, width=20,
                                                         completevalues=self.product_type_list)
        self.ety_filter_product_type.grid(row=2, column=2, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_type.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_size = tk.Label(name_filter_container, text="Size: ", bg=self.clr_yellow)
        filter_lbl_product_size.grid(row=1, column=3, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_size = AutocompleteEntry(name_filter_container, width=8,
                                                         completevalues=self.product_size_list)
        self.ety_filter_product_size.grid(row=2, column=3, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_size.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_price = tk.Label(name_filter_container, text="Price: ", bg=self.clr_yellow)
        filter_lbl_product_price.grid(row=1, column=4, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_sell_price = AutocompleteEntry(name_filter_container, width=8,
                                                               completevalues=self.product_sell_price_list)
        self.ety_filter_product_sell_price.grid(row=2, column=4, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_sell_price.bind("<Return>", lambda event: self.filter_product(event))

        btn_filter = tk.Button(name_filter_container, text="Apply Filter", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_product)
        btn_filter.grid(row=2, column=5, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(name_filter_container, text="Clear Filter", command=self.reload_sales)
        btn_clear_filter.grid(row=2, column=6, sticky="news", padx=2, pady=1)

        code_filter_container.grid_rowconfigure(0, weight=1)
        code_filter_container.grid_rowconfigure(3, weight=1)
        code_filter_container.grid_columnconfigure(0, weight=1)
        code_filter_container.grid_columnconfigure(7, weight=1)

        lbl_search_product_code = tk.Label(code_filter_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_search_product_code.grid(row=1, column=1, columnspan=3, sticky="nw", padx=1, pady=1)

        self.ety_filter_product_code_1 = MaxLengthEntry(code_filter_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_1)
        self.ety_filter_product_code_1.grid(row=2, column=1, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_1.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_filter_product_code_2 = MaxLengthEntry(code_filter_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_2)
        self.ety_filter_product_code_2.grid(row=2, column=2, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_2.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_filter_product_code_3 = MaxLengthEntry(code_filter_container, maxlength=2, width=3,
                                                        textvariable=self.var_search_product_code_3)
        self.ety_filter_product_code_3.grid(row=2, column=3, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_3.bind('<Return>', lambda event: self.validate_entry(event, 2))

        self.ety_filter_product_code_4 = MaxLengthEntry(code_filter_container, maxlength=4, width=5,
                                                        textvariable=self.var_search_product_code_4)
        self.ety_filter_product_code_4.grid(row=2, column=4, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_filter_product_code_4.bind('<Return>', lambda event: self.validate_entry(event, 4))

        btn_filter_product_code = tk.Button(code_filter_container, text="Apply Filter",
                                            bg=self.clr_fuchsia, fg='white', command=self.filter_product_code)
        btn_filter_product_code.grid(row=2, column=5, sticky="sw", padx=2, pady=1)
        btn_filter_product_code.bind('<Return>', lambda event: self.filter_product_code(event))

        btn_clear_filter = tk.Button(code_filter_container, text="Clear Filter", command=self.reload_sales)
        btn_clear_filter.grid(row=2, column=6, sticky="news", padx=2, pady=1)

        # billno_filter_container elements
        billno_filter_container.grid_rowconfigure(0, weight=1)
        billno_filter_container.grid_rowconfigure(3, weight=1)
        billno_filter_container.grid_columnconfigure(0, weight=1)
        billno_filter_container.grid_columnconfigure(4, weight=1)

        filter_lbl_bill_number = tk.Label(billno_filter_container, text="Bill No: ", bg=self.clr_yellow)
        filter_lbl_bill_number.grid(row=1, column=1, sticky="nw", padx=1, pady=1)
        self.ety_filter_bill_number = AutocompleteEntry(billno_filter_container, width=8,
                                                        completevalues=self.billno_list)
        self.ety_filter_bill_number.grid(row=2, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_bill_number.bind("<Return>", lambda event: self.filter_bill_number(event))

        btn_apply_filter = tk.Button(billno_filter_container, text="Apply Filter", bg=self.clr_fuchsia, fg='white',
                                     command=self.filter_bill_number)
        btn_apply_filter.grid(row=2, column=2, sticky="news", padx=2, pady=1)
        btn_apply_filter.bind('<Return>', lambda event: self.filter_bill_number(event))

        btn_clear_filter = tk.Button(billno_filter_container, text="Clear Filter", command=self.reload_sales)
        btn_clear_filter.grid(row=2, column=3, sticky="news", padx=2, pady=1)

        # ********** tree_containers elements *********
        header = ('SALES_DATE', 'BILL_NO', 'PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE', 'SIZE',
                  'PRICE', 'QTY', '')
        self.sales_tree = ttk.Treeview(sales_tree_container, columns=header, height=20, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(sales_tree_container, orient="vertical", command=self.sales_tree.yview)
        hsb = ttk.Scrollbar(sales_tree_container, orient="horizontal", command=self.sales_tree.xview)

        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.sales_tree.grid(column=0, row=0, sticky='nsew', in_=sales_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=sales_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=sales_tree_container)

        sales_tree_container.grid_columnconfigure(0, weight=1)
        sales_tree_container.grid_rowconfigure(0, weight=1)

        self.sales_tree.heading("0", text="SALES_DATE")
        self.sales_tree.heading("1", text="BILL_NO")
        self.sales_tree.heading("2", text="PRODUCT_CODE")
        self.sales_tree.heading("3", text="PRODUCT_NAME")
        self.sales_tree.heading("4", text="PRODUCT_TYPE")
        self.sales_tree.heading("5", text="SIZE")
        self.sales_tree.heading("6", text="PRICE")
        self.sales_tree.heading("7", text="QTY")

        self.sales_tree.column(0, anchor=tk.W, width="140")
        self.sales_tree.column(1, anchor=tk.W, width="80")
        self.sales_tree.column(2, anchor=tk.W, width="120")
        self.sales_tree.column(3, anchor=tk.W, width="140")
        self.sales_tree.column(4, anchor=tk.W, width="180")
        self.sales_tree.column(5, anchor='center', width="50")
        self.sales_tree.column(6, anchor=tk.E, width="80")
        self.sales_tree.column(7, anchor='center', width="50")
        self.sales_tree.column(8, anchor='center', width="2")

        self.reload_sales()

        numeric_cols = ['BILL_NO', 'PRICE', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.sales_tree.heading(col, text=col,
                                        command=lambda _col=col: self.sort_treeview(
                                               self.sales_tree, _col,
                                               numeric_sort=True, reverse=False))
            else:
                self.sales_tree.heading(col, text=col,
                                        command=lambda _col=col: self.sort_treeview(
                                               self.sales_tree, _col,
                                               numeric_sort=False, reverse=False))

        self.sales_tree.tag_configure("evenrow", background='#fbefcc')
        self.sales_tree.tag_configure("oddrow", background='white', foreground='black')
        self.sales_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # ********** Sales Details *********
        sales_details_container = tk.Frame(right_container, bd=5, pady=3, padx=10, relief=tk.RIDGE, bg=self.clr_yellow)
        sales_details_container.pack(fill='both', expand=True, side=tk.TOP)

        sales_stats_container = tk.Frame(right_container, bd=5, pady=3, padx=10, relief=tk.RIDGE, bg=self.clr_yellow)
        sales_stats_container.pack(fill='both', expand=True, side=tk.TOP, anchor='center')

        sales_details_container.grid_columnconfigure(0, weight=1)
        sales_details_container.grid_columnconfigure(3, weight=1)

        lbl_product_details = tk.Label(sales_details_container, text="Sales Details", bg=self.clr_blueiris, fg="white")
        lbl_product_details.grid(row=0, column=1, columnspan=2, sticky="news", padx=3, pady=3)
        lbl_product_details.config(font=("Calibri bold", 14))

        lbl_sales_date = tk.Label(sales_details_container, text="Sales Date: ", bg=self.clr_yellow)
        lbl_sales_date.grid(row=1, column=1, sticky="nw", padx=3, pady=1)
        ety_sales_date = tk.Entry(sales_details_container, textvariable=self.var_sales_date, state='disabled')
        ety_sales_date.grid(row=1, column=2, sticky="nw", padx=3, pady=1)

        lbl_bill_number = tk.Label(sales_details_container, text="Bill No: ", bg=self.clr_yellow)
        lbl_bill_number.grid(row=2, column=1, sticky="nw", padx=3, pady=1)
        ety_bill_number = tk.Entry(sales_details_container, width=8, textvariable=self.var_bill_number, state='disabled')
        ety_bill_number.grid(row=2, column=2, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_code = tk.Label(sales_details_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_code.grid(row=3, column=1, sticky="nw", padx=3, pady=1)
        ety_product_code = tk.Entry(sales_details_container, width=15, textvariable=self.var_product_code, state='disabled')
        ety_product_code.grid(row=3, column=2, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(sales_details_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=4, column=1, sticky="nw", padx=3, pady=1)
        ety_product_name = tk.Entry(sales_details_container, textvariable=self.var_product_name, state='disabled')
        ety_product_name.grid(row=4, column=2, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(sales_details_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=5, column=1, sticky="nw", padx=3, pady=1)
        ety_product_type = tk.Entry(sales_details_container, textvariable=self.var_product_type, state='disabled')
        ety_product_type.grid(row=5, column=2, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(sales_details_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=6, column=1, sticky="nw", padx=3, pady=1)
        ety_product_size = tk.Entry(sales_details_container, width=12, textvariable=self.var_product_size, state='disabled')
        ety_product_size.grid(row=6, column=2, columnspan=2, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(sales_details_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=7, column=1, sticky="nw", padx=3, pady=1)
        ety_selling_price = tk.Entry(sales_details_container, width=8, textvariable=self.var_selling_price,
                                     state='disabled')
        ety_selling_price.grid(row=7, column=2, sticky="nw", padx=3, pady=1)

        lbl_quantity = tk.Label(sales_details_container, text="Quantity: ", bg=self.clr_yellow)
        lbl_quantity.grid(row=8, column=1, sticky="nw", padx=3, pady=1)
        ety_quantity = tk.Entry(sales_details_container, width=5, textvariable=self.var_quantity, state='disabled')
        ety_quantity.grid(row=8, column=2, sticky="nw", padx=3, pady=1)

        # sales_stats_container element
        sales_stats_container.grid_columnconfigure(0, weight=1)
        sales_stats_container.grid_columnconfigure(3, weight=1)

        lbl_sales_stats = tk.Label(sales_stats_container, text="Sales Stats", bg=self.clr_blueiris, fg="white")
        lbl_sales_stats.grid(row=0, column=1, columnspan=2, sticky="news", padx=3, pady=5)
        lbl_sales_stats.config(font=("Calibri bold", 14))

        lbl_from_date = tk.Label(sales_stats_container, text='From Date: ', bg=self.clr_yellow)
        lbl_from_date.grid(row=1, column=1, sticky="nw", padx=1, pady=5)
        self.sales_from_date = DateEntry(sales_stats_container, date_pattern='yyyy-mm-dd', background='yellow',
                                         foreground='black', borderwidth=2, width=10)
        self.sales_from_date.grid(row=1, column=2, sticky="sw", padx=2, pady=5, ipady=3)

        lbl_to_date = tk.Label(sales_stats_container, text='To Date: ', bg=self.clr_yellow)
        lbl_to_date.grid(row=2, column=1, sticky="nw", padx=1, pady=5)
        self.sales_to_date = DateEntry(sales_stats_container, date_pattern='yyyy-mm-dd', background='yellow',
                                       foreground='back', borderwidth=2, width=10)
        self.sales_to_date.grid(row=2, column=2, sticky="sw", padx=2, pady=5, ipady=3)

        lbl_sold_quantity = tk.Label(sales_stats_container, text="Quantity: ", bg=self.clr_yellow)
        lbl_sold_quantity.grid(row=3, column=1, sticky="nw", padx=3, pady=5)
        ety_sold_quantity = tk.Entry(sales_stats_container, width=5, textvariable=self.var_sold_quantity, state='disabled')
        ety_sold_quantity.grid(row=3, column=2, sticky="nw", padx=3, pady=5)

        lbl_sales_amount = tk.Label(sales_stats_container, text="Amount: ", bg=self.clr_yellow)
        lbl_sales_amount.grid(row=4, column=1, sticky="nw", padx=3, pady=5)
        ety_sales_amount = tk.Entry(sales_stats_container, width=10, textvariable=self.var_sales_amount,
                                    state='disabled')
        ety_sales_amount.grid(row=4, column=2, sticky="nw", padx=3, pady=5)

        btn_get_sales_data = tk.Button(sales_stats_container, text="Get Sales Data", bg=self.clr_fuchsia, fg='white',
                                       command=self.get_sales_data)
        btn_get_sales_data.grid(row=5, column=1, columnspan=2, sticky="news", padx=2, pady=5)
        btn_get_sales_data.bind('<Return>', lambda event: self.get_sales_data(event))

    def get_sales_data(self, event=None):
        from_date = self.sales_from_date.get()
        to_date = self.sales_to_date.get()

        sold_quantity, total_sales_amount = Sales.get_sales_data(from_date=from_date, to_date=to_date)
        if sold_quantity is None:
            sold_quantity = 0

        if total_sales_amount is None:
            total_sales_amount = 0

        self.var_sold_quantity.set(sold_quantity)
        self.var_sales_amount.set(format_currency(total_sales_amount, 'INR', locale='en_IN'))

    @staticmethod
    def validate_entry(event=None, length=0):
        if len(event.widget.get().strip()) == length:
            event.widget.tk_focusNext().focus()

    def filter_product(self, event=None):
        product_name = self.ety_filter_product_name.get().strip()
        product_type = self.ety_filter_product_type.get().strip()
        product_size = self.ety_filter_product_size.get().strip()
        selling_price = str(self.ety_filter_product_sell_price.get().strip())
        if selling_price:
            selling_price = float(selling_price)
        else:
            selling_price = 0.0

        if self.var_chk_include_date.get():
            rows = Sales.search_sales(from_date=self.from_date.get(),
                                      to_date=self.to_date.get(),
                                      product_name=product_name,
                                      product_type=product_type,
                                      product_size=product_size,
                                      selling_price=selling_price)
        else:
            rows = Sales.search_sales(product_name=product_name,
                                      product_type=product_type,
                                      product_size=product_size,
                                      selling_price=selling_price)

        self.sales_tree.delete(*self.sales_tree.get_children())

        sl_no = 0
        for row in rows:
            product = row.Product
            sale = row.Sales

            sl_no = sl_no + 1
            rw = (datetime.strftime(sale.sales_date, '%d-%b-%Y %H:%M:%S'), sale.bill_number, sale.product_code,
                  product.product_name, product.product_type, product.product_size,
                  round(product.selling_price, 2), sale.quantity)

            if sl_no % 2 == 0:
                self.sales_tree.insert("", tk.END, values=rw, tags=('evenrow', sale.product_code))
            else:
                self.sales_tree.insert("", tk.END, values=rw, tags=('oddrow', sale.product_code))

    def filter_bill_number(self, event=None):
        bill_number = self.ety_filter_bill_number.get().strip()
        if bill_number and bill_number != "":
            rows = Sales.search_bill_number(bill_number=bill_number)

            if len(rows) == 0:
                messagebox.showerror("SS Fashion Tuty", f"Bill_number: {bill_number} not found!")
                print(f"Bill_number: {bill_number} not found!")
            else:
                self.sales_tree.delete(*self.sales_tree.get_children())

                sl_no = 0
                for row in rows:
                    product = row.Product
                    sale = row.Sales

                    sl_no = sl_no + 1
                    rw = (datetime.strftime(sale.sales_date, '%d-%b-%Y %H:%M:%S'), sale.bill_number, sale.product_code,
                          product.product_name, product.product_type, product.product_size,
                          round(product.selling_price, 2), sale.quantity)

                    if sl_no % 2 == 0:
                        self.sales_tree.insert("", tk.END, values=rw, tags=('evenrow', sale.product_code))
                    else:
                        self.sales_tree.insert("", tk.END, values=rw, tags=('oddrow', sale.product_code))
        else:
            self.reload_sales()

    def filter_product_code(self, event=None):
        product_code = f"{self.ety_filter_product_code_1.get().strip()}" \
                       f"-{self.ety_filter_product_code_2.get().strip()}" \
                       f"-{self.ety_filter_product_code_3.get().strip()}" \
                       f"-{self.ety_filter_product_code_4.get().strip()}"

        if product_code != "---":
            if self.var_chk_include_date.get():
                rows = Sales.search_product_code(product_code=product_code,
                                                 from_date=self.from_date.get(),
                                                 to_date=self.to_date.get(),
                                                 )
            else:
                rows = Sales.search_product_code(product_code=product_code)

            if rows is None:
                messagebox.showerror("SS Fashion Tuty", f"Product_code: {product_code} not found!")
                print(f"Product_code: {product_code} not found!")
            else:
                self.sales_tree.delete(*self.sales_tree.get_children())

                sl_no = 0
                for row in rows:
                    product = row.Product
                    sale = row.Sales

                    sl_no = sl_no + 1
                    rw = (datetime.strftime(sale.sales_date, '%d-%b-%Y %H:%M:%S'), sale.bill_number, sale.product_code,
                          product.product_name, product.product_type, product.product_size,
                          round(product.selling_price, 2), sale.quantity)

                    if sl_no % 2 == 0:
                        self.sales_tree.insert("", tk.END, values=rw, tags=('evenrow', sale.product_code))
                    else:
                        self.sales_tree.insert("", tk.END, values=rw, tags=('oddrow', sale.product_code))

    def reload_sales(self):
        self.ety_filter_product_name.delete(0, tk.END)
        self.ety_filter_product_type.delete(0, tk.END)
        self.ety_filter_product_size.delete(0, tk.END)
        self.ety_filter_product_sell_price.delete(0, tk.END)

        self.ety_filter_product_code_1.delete(0, tk.END)
        self.ety_filter_product_code_2.delete(0, tk.END)
        self.ety_filter_product_code_3.delete(0, tk.END)
        self.ety_filter_product_code_4.delete(0, tk.END)

        self.ety_filter_bill_number.delete(0, tk.END)

        self.sales_tree.delete(*self.sales_tree.get_children())

        rows = Sales.get_all_sales()
        sl_no = 0
        for row in rows:
            product = row.Product
            sale = row.Sales

            sl_no = sl_no + 1
            rw = (datetime.strftime(sale.sales_date, '%d-%b-%Y %H:%M:%S'), sale.bill_number, sale.product_code,
                  product.product_name, product.product_type, product.product_size,
                  round(product.selling_price, 2), sale.quantity)

            if sl_no % 2 == 0:
                self.sales_tree.insert("", tk.END, values=rw, tags=('evenrow', sale.product_code))
            else:
                self.sales_tree.insert("", tk.END, values=rw, tags=('oddrow', sale.product_code))

    def on_tree_select(self, event):
        self.selected_row = event.widget.selection()

        sales = self.sales_tree.item(self.selected_row)['values']

        if sales:
            self.var_sales_date.set(sales[0])
            self.var_bill_number.set(sales[1])
            self.var_product_code.set(sales[2])
            self.var_product_name.set(sales[3])
            self.var_product_type.set(sales[4])
            self.var_product_size.set(sales[5])
            self.var_selling_price.set(sales[6])
            self.var_quantity.set(sales[7])
