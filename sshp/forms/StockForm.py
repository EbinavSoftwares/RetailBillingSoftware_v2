import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from babel.numbers import format_currency
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.Product import Product
from sshp.models.Stock import Stock
from sshp.models.StockTimeline import StockTimeline
from sshp.utilities.MaxLengthEntry import MaxLengthEntry


class StockForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - Stocks")

        # variables
        self.selected_row = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()

        # widgets
        self.ety_filter_product_name = None
        self.ety_filter_product_type = None
        self.ety_filter_product_size = None
        self.ety_filter_product_sell_price = None
        self.ety_filter_quantity = None
        self.ety_filter_product_code_1 = None
        self.ety_filter_product_code_2 = None
        self.ety_filter_product_code_3 = None
        self.ety_filter_product_code_4 = None
        self.products_tree = None
        self.stock_value_tree = None
        self.low_stock_tree = None
        self.timeline_window = None
        self.timeline_tree = None

        # widget variables
        self.var_total_quantity = tk.IntVar()
        self.var_total_stock_value = tk.DoubleVar()
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        self.var_quantity = tk.IntVar()
        self.var_search_product_code_1 = tk.StringVar()
        self.var_search_product_code_2 = tk.StringVar()
        self.var_search_product_code_3 = tk.StringVar()
        self.var_search_product_code_4 = tk.StringVar()
        self.var_filter_quantity = tk.IntVar()

        self.load_stock_form()

        # shortcuts
        self.window.bind("<Control-T>", lambda event: self.show_stock_timeline(event))
        self.window.bind("<Control-t>", lambda event: self.show_stock_timeline(event))

    def load_stock_form(self):
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
        left_container = tk.Frame(self.content_container, bd=5, padx=2, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        left_container.pack(fill='both', expand=True, side=tk.LEFT)

        right_container = tk.Frame(self.content_container, bd=5, padx=2, relief=tk.RIDGE, bg=self.clr_yellow)
        right_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container main elements
        button_container = tk.Frame(left_container, padx=2, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        button_container.pack(fill='both', expand=True, side=tk.TOP)

        products_tree_container = tk.Frame(left_container, padx=2, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        products_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        # button_container
        stats_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        stats_container.pack(fill='both', expand=True, anchor='w', side=tk.LEFT)

        name_filter_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        name_filter_container.pack(fill='both', expand=True, anchor='w', side=tk.TOP)

        code_filter_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        code_filter_container.pack(fill='both', expand=True, anchor='w', side=tk.LEFT)

        quantity_filter_container = tk.Frame(button_container, bd=2, relief=tk.RIDGE, bg=self.clr_yellow)
        quantity_filter_container.pack(fill='both', expand=True, anchor='w', side=tk.RIGHT)

        # # tree container elements
        # products_tree_container = tk.Frame(tree_container, pady=3, bg=self.clr_yellow, relief=tk.RIDGE)
        # products_tree_container.pack(fill='x', expand=True, side=tk.TOP)

        # ********** button_container elements *********
        lbl_total_quantity = tk.Label(stats_container, text='Quantity: ', bg=self.clr_yellow)
        lbl_total_quantity.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        ety_total_quantity = tk.Entry(stats_container, width=5, textvariable=self.var_total_quantity, state='disabled')
        ety_total_quantity.grid(row=1, column=0, sticky="nw", padx=3, pady=1)

        lbl_total_stock_value = tk.Label(stats_container, text='Stock Value: ', bg=self.clr_yellow)
        lbl_total_stock_value.grid(row=2, column=0, sticky="nw", padx=1, pady=1)
        ety_total_stock_value = tk.Entry(stats_container, width=12, textvariable=self.var_total_stock_value,
                                         state='disabled')
        ety_total_stock_value.grid(row=3, column=0, sticky="nw", padx=3, pady=1)

        # name_filter_container elements
        filter_lbl_product_name = tk.Label(name_filter_container, text="Name: ", bg=self.clr_yellow)
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_name = AutocompleteEntry(name_filter_container, width=18,
                                                         completevalues=self.product_name_list)
        self.ety_filter_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_name.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_type = tk.Label(name_filter_container, text="Type: ", bg=self.clr_yellow)
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_type = AutocompleteEntry(name_filter_container, width=20,
                                                         completevalues=self.product_type_list)
        self.ety_filter_product_type.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_type.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_size = tk.Label(name_filter_container, text="Size: ", bg=self.clr_yellow)
        filter_lbl_product_size.grid(row=0, column=2, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_size = AutocompleteEntry(name_filter_container, width=12,
                                                         completevalues=self.product_size_list)
        self.ety_filter_product_size.grid(row=1, column=2, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_size.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_price = tk.Label(name_filter_container, text="Price: ", bg=self.clr_yellow)
        filter_lbl_product_price.grid(row=0, column=3, sticky="nw", padx=1, pady=1)
        self.ety_filter_product_sell_price = AutocompleteEntry(name_filter_container, width=10,
                                                               completevalues=self.product_sell_price_list)
        self.ety_filter_product_sell_price.grid(row=1, column=3, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_product_sell_price.bind("<Return>", lambda event: self.filter_product(event))

        btn_filter = tk.Button(name_filter_container, text="Apply Filter", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_product)
        btn_filter.grid(row=1, column=4, sticky="sw", padx=2, pady=1)

        btn_clear_filter = tk.Button(name_filter_container, text="Clear", command=self.reload_stock)
        btn_clear_filter.grid(row=1, column=5, sticky="news", padx=2, pady=1)

        lbl_search_product_code = tk.Label(code_filter_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_search_product_code.grid(row=0, column=0, columnspan=3, sticky="nw", padx=1, pady=1)

        self.ety_filter_product_code_1 = MaxLengthEntry(code_filter_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_1)
        self.ety_filter_product_code_1.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=5)
        self.ety_filter_product_code_1.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_filter_product_code_2 = MaxLengthEntry(code_filter_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_2)
        self.ety_filter_product_code_2.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=5)
        # self.ety_search_product_code_2.bind('<Return>', lambda event: self.search_product(event))
        self.ety_filter_product_code_2.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_filter_product_code_3 = MaxLengthEntry(code_filter_container, maxlength=2, width=3,
                                                        textvariable=self.var_search_product_code_3)
        self.ety_filter_product_code_3.grid(row=1, column=2, sticky="nw", padx=2, pady=1, ipady=5)
        # self.ety_search_product_code_2.bind('<Return>', lambda event: self.search_product(event))
        self.ety_filter_product_code_3.bind('<Return>', lambda event: self.validate_entry(event, 2))

        self.ety_filter_product_code_4 = MaxLengthEntry(code_filter_container, maxlength=4, width=5,
                                                        textvariable=self.var_search_product_code_4)
        self.ety_filter_product_code_4.grid(row=1, column=3, sticky="nw", padx=2, pady=1, ipady=5)
        self.ety_filter_product_code_4.bind('<Return>', lambda event: self.validate_entry(event, 4))

        btn_filter_product_code = tk.Button(code_filter_container, text="Apply Filter",
                                            bg=self.clr_fuchsia, fg='white', command=self.filter_by_product_code)
        btn_filter_product_code.grid(row=1, column=4, sticky="sw", padx=2, pady=1)
        btn_filter_product_code.bind('<Return>', lambda event: self.filter_by_product_code(event))

        btn_clear_filter = tk.Button(code_filter_container, text="Clear", command=self.reload_stock)
        btn_clear_filter.grid(row=1, column=5, sticky="news", padx=2, pady=1)

        # quantity_filter_container elements
        lbl_filter_quantity = tk.Label(quantity_filter_container, text="Quantity: ", bg=self.clr_yellow)
        lbl_filter_quantity.grid(row=0, column=0, sticky="nw", padx=1, pady=1)

        self.ety_filter_quantity = tk.Entry(quantity_filter_container, width=8, textvariable=self.var_filter_quantity)
        self.ety_filter_quantity.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.ety_filter_quantity.bind("<Return>", lambda event: self.filter_by_quantity(event))

        btn_apply_filter = tk.Button(quantity_filter_container, text="Apply Filter",
                                     bg=self.clr_fuchsia, fg='white', command=self.filter_by_quantity)
        btn_apply_filter.grid(row=1, column=1, sticky="news", padx=2, pady=1)
        btn_apply_filter.bind('<Return>', lambda event: self.filter_by_quantity(event))

        btn_clear_filter = tk.Button(quantity_filter_container, text="Clear", command=self.reload_stock)
        btn_clear_filter.grid(row=1, column=2, sticky="news", padx=2, pady=1)

        # ********** tree_containers elements *********
        products_tree_container = tk.Frame(left_container, pady=1, bg=self.clr_yellow)
        products_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE', 'SIZE', 'SELL_PRICE',
                  'QTY', '')
        self.products_tree = ttk.Treeview(products_tree_container, columns=header, show="headings", height=7,
                                          selectmode="browse")
        vsb = ttk.Scrollbar(products_tree_container, orient="vertical", command=self.products_tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.products_tree.xview)

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
        self.products_tree.column(2, anchor=tk.W, width="130")
        self.products_tree.column(3, anchor=tk.W, width="150")
        self.products_tree.column(4, anchor='center', width="100")
        self.products_tree.column(5, anchor=tk.E, width="80")
        self.products_tree.column(6, anchor='center', width="50")
        self.products_tree.column(7, anchor='center', width="2")

        self.reload_stock()

        numeric_cols = ['#', 'SELL_PRICE', 'QTY']
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

        self.products_tree.tag_configure("evenrow", background='#fbefcc')
        self.products_tree.tag_configure("oddrow", background='white', foreground='black')
        self.products_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # ********** Stock Details *********
        stock_details_container = tk.Frame(left_container, bd=2, pady=1, padx=3, relief=tk.RIDGE, bg=self.clr_yellow)
        stock_details_container.pack(fill='both', expand=True, side=tk.LEFT)

        stock_details_container.grid_columnconfigure(0, weight=1)
        stock_details_container.grid_columnconfigure(3, weight=1)

        lbl_stock_details = tk.Label(stock_details_container, text="Stock Details", bg=self.clr_blueiris, fg="white")
        lbl_stock_details.grid(row=0, column=1, columnspan=2, sticky="news", padx=3, pady=4)
        lbl_stock_details.config(font=("Calibri bold", 12))

        lbl_product_id = tk.Label(stock_details_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_id.grid(row=1, column=1, sticky="nw", padx=3, pady=1)
        product_id = tk.Entry(stock_details_container, width=15, textvariable=self.var_product_code, state='disabled')
        product_id.grid(row=1, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(stock_details_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=2, column=1, sticky="nw", padx=3, pady=1)
        product_name = tk.Entry(stock_details_container, textvariable=self.var_product_name, state='disabled')
        product_name.grid(row=2, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(stock_details_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=3, column=1, sticky="nw", padx=3, pady=1)
        product_type = tk.Entry(stock_details_container, textvariable=self.var_product_type, state='disabled')
        product_type.grid(row=3, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(stock_details_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=4, column=1, sticky="nw", padx=3, pady=1)
        product_size = tk.Entry(stock_details_container, width=15, textvariable=self.var_product_size, state='disabled')
        product_size.grid(row=4, column=2, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(stock_details_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=5, column=1, sticky="nw", padx=3, pady=1)
        selling_price = tk.Entry(stock_details_container, width=10, textvariable=self.var_selling_price,
                                 state='disabled')
        selling_price.grid(row=5, column=2, sticky="nw", padx=3, pady=1)

        lbl_quantity = tk.Label(stock_details_container, text="Quantity: ", bg=self.clr_yellow)
        lbl_quantity.grid(row=6, column=1, sticky="nw", padx=3, pady=1)
        ety_quantity = tk.Entry(stock_details_container, width=10, textvariable=self.var_quantity, state='disabled')
        ety_quantity.grid(row=6, column=2, sticky="nw", padx=3, pady=1)

        btn_stock_timeline = tk.Button(stock_details_container, text="Stock [T]imeline", bg=self.clr_fuchsia, fg='white',
                                       command=self.show_stock_timeline)
        btn_stock_timeline.grid(row=7, column=2, sticky="sw", padx=2, pady=4)

        # ********** Stock Value Tree Details *********
        stock_value_tree_container = tk.Frame(left_container, bd=2, pady=3, relief=tk.RIDGE, bg=self.clr_yellow)
        stock_value_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'PRODUCT', 'QTY', 'STOCK_VALUE', '')
        self.stock_value_tree = ttk.Treeview(stock_value_tree_container, columns=header, show="headings",
                                             selectmode="browse")
        vsb = ttk.Scrollbar(stock_value_tree_container, orient="vertical", command=self.stock_value_tree.yview)
        hsb = ttk.Scrollbar(stock_value_tree_container, orient="horizontal", command=self.stock_value_tree.xview)

        self.stock_value_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.stock_value_tree.grid(column=0, row=0, sticky='nsew', in_=stock_value_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=stock_value_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=stock_value_tree_container)

        stock_value_tree_container.grid_columnconfigure(0, weight=1)
        stock_value_tree_container.grid_rowconfigure(0, weight=1)

        self.stock_value_tree.heading("0", text="#")
        self.stock_value_tree.heading("1", text="PRODUCT")
        self.stock_value_tree.heading("2", text="QTY")
        self.stock_value_tree.heading("3", text="STOCK_VALUE")

        self.stock_value_tree.column(0, anchor='center', minwidth=30, width=30)
        self.stock_value_tree.column(1, anchor=tk.W, minwidth=150, width=150)
        self.stock_value_tree.column(2, anchor='center', minwidth=80, width=80)
        self.stock_value_tree.column(3, anchor=tk.E, minwidth=120, width=120)
        self.stock_value_tree.column(4, anchor='center', width=5)
        self.stock_value_tree["displaycolumns"] = (0, 1, 2, 3, 4)

        self.load_stock_value_details()

        numeric_cols = ['#', 'QTY', 'STOCK_VALUE']
        for col in header:
            if col in numeric_cols:
                self.stock_value_tree.heading(col, text=col,
                                              command=lambda _col=col: self.sort_treeview(
                                                self.stock_value_tree, _col,
                                                numeric_sort=True, reverse=False))
            else:
                self.stock_value_tree.heading(col, text=col,
                                              command=lambda _col=col: self.sort_treeview(
                                                self.stock_value_tree, _col,
                                                numeric_sort=False, reverse=False))

        self.stock_value_tree.tag_configure("evenrow", background='#fbefcc')
        self.stock_value_tree.tag_configure("oddrow", background='white', foreground='black')

        # ********** Low Stock Tree Container *********
        lbl_product_details = tk.Label(right_container, text="Low Stock Details", bg=self.clr_blueiris, fg="white")
        lbl_product_details.pack(fill='x', expand=True, side=tk.TOP)
        lbl_product_details.config(font=("Calibri bold", 14))

        low_stock_tree_container = tk.Frame(right_container, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        low_stock_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'PRODUCT', 'TYPE', 'SIZE', 'PRICE', 'QTY', '')
        self.low_stock_tree = ttk.Treeview(low_stock_tree_container, columns=header, height=21, show="headings",
                                           selectmode="browse")
        vsb = ttk.Scrollbar(low_stock_tree_container, orient="vertical", command=self.low_stock_tree.yview)
        hsb = ttk.Scrollbar(low_stock_tree_container, orient="horizontal", command=self.low_stock_tree.xview)

        self.low_stock_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.low_stock_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        stock_value_tree_container.grid_columnconfigure(0, weight=1)
        stock_value_tree_container.grid_rowconfigure(0, weight=1)

        self.low_stock_tree.heading("0", text="#")
        self.low_stock_tree.heading("1", text="PRODUCT")
        self.low_stock_tree.heading("2", text="TYPE")
        self.low_stock_tree.heading("3", text="SIZE")
        self.low_stock_tree.heading("4", text="PRICE")
        self.low_stock_tree.heading("5", text="QTY")

        self.low_stock_tree.column(0, anchor='center', minwidth=40, width=40)
        self.low_stock_tree.column(1, anchor=tk.W, minwidth=120, width=120)
        self.low_stock_tree.column(2, anchor=tk.W, minwidth=140, width=140)
        self.low_stock_tree.column(3, anchor='center', minwidth=100, width=100)
        self.low_stock_tree.column(4, anchor=tk.E, minwidth=80, width=80)
        self.low_stock_tree.column(5, anchor='center', minwidth=50, width=50)
        self.low_stock_tree["displaycolumns"] = (0, 1, 2, 3, 4, 5)

        self.load_low_stock_details()

        numeric_cols = ['#', 'PRICE', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.low_stock_tree.heading(col, text=col,
                                            command=lambda _col=col: self.sort_treeview(
                                               self.low_stock_tree, _col,
                                               numeric_sort=True, reverse=False))
            else:
                self.low_stock_tree.heading(col, text=col,
                                            command=lambda _col=col: self.sort_treeview(
                                               self.low_stock_tree, _col,
                                               numeric_sort=False, reverse=False))

        self.low_stock_tree.tag_configure("evenrow", background='#fbefcc')
        self.low_stock_tree.tag_configure("oddrow", background='white', foreground='black')

    def show_stock_timeline(self, event=None):
        self.window.wm_attributes("-disabled", True)

        self.timeline_window = tk.Toplevel(self.window)
        self.timeline_window.overrideredirect(True)

        # Gets the requested values of the height and width.
        window_width = self.window.winfo_reqwidth() / 2
        window_height = self.window.winfo_reqheight() / 2

        # Gets both half the screen width/height and window width/height
        position_right = int(self.timeline_window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.timeline_window.winfo_screenheight() / 2 - window_height / 2)

        # Positions the window in the center of the page.
        self.timeline_window.geometry("+{}+{}".format(position_right, position_down))

        main_container = tk.Frame(self.timeline_window, bd=20, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_limegreen)
        main_container.pack(expand=True, side=tk.TOP, anchor="n")

        label_container = tk.Frame(main_container, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_yellow)
        label_container.pack(expand=True, side=tk.TOP, anchor="n")

        tree_container = tk.Frame(main_container, padx=10, pady=5, relief=tk.RIDGE, bg=self.clr_limegreen)
        tree_container.pack(expand=True, side=tk.TOP, anchor="n")

        lbl_product_code = tk.Label(label_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_code.grid(row=0, column=0, sticky="nw", padx=3, pady=1)
        ety_product_code = tk.Entry(label_container, width=15, textvariable=self.var_product_code,
                                    state='disabled')
        ety_product_code.grid(row=1, column=0, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(label_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=0, column=1, sticky="nw", padx=3, pady=1)
        ety_product_name = tk.Entry(label_container, textvariable=self.var_product_name,
                                    state='disabled')
        ety_product_name.grid(row=1, column=1, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(label_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=0, column=2, sticky="nw", padx=3, pady=1)
        ety_product_type = tk.Entry(label_container, textvariable=self.var_product_type,
                                    state='disabled')
        ety_product_type.grid(row=1, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(label_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=0, column=3, sticky="nw", padx=3, pady=1)
        ety_product_size = tk.Entry(label_container, width=10, textvariable=self.var_product_size,
                                    state='disabled')
        ety_product_size.grid(row=1, column=3, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(label_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=0, column=4, sticky="nw", padx=3, pady=1)
        ety_selling_price = tk.Entry(label_container, width=10, textvariable=self.var_selling_price,
                                     state='disabled')
        ety_selling_price.grid(row=1, column=4, sticky="nw", padx=3, pady=1)

        header = ('#', 'entry_date', 'activity', 'change', 'available', 'dummy')
        self.timeline_tree = ttk.Treeview(tree_container, columns=header, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.stock_value_tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.stock_value_tree.xview)

        self.timeline_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.timeline_tree.grid(column=0, row=0, sticky='nsew', in_=tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=tree_container)

        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)

        self.timeline_tree.heading("0", text="#")
        self.timeline_tree.heading("1", text="ENTRY_DATE")
        self.timeline_tree.heading("2", text="ACTIVITY")
        self.timeline_tree.heading("3", text="CHANGE")
        self.timeline_tree.heading("4", text="AVAILABLE")

        self.timeline_tree.column(0, anchor='center', minwidth=50, width=50)
        self.timeline_tree.column(1, anchor=tk.W)
        self.timeline_tree.column(2, anchor=tk.W)
        self.timeline_tree.column(3, anchor='center', minwidth=100, width=100)
        self.timeline_tree.column(4, anchor='center', minwidth=100, width=100)
        self.timeline_tree.column(5, anchor='center', width=5)
        self.timeline_tree["displaycolumns"] = (0, 1, 2, 3, 4, 5)

        self.timeline_tree.tag_configure("evenrow", background='#fbefcc')
        self.timeline_tree.tag_configure("oddrow", background='white', foreground='black')

        btn_close = tk.Button(tree_container, text='Close', width=10, bg=self.clr_fuchsia, fg='white',
                              command=lambda: self.clean_timeline_window())
        btn_close.grid(row=2, column=0, padx=5, pady=20)

        self.timeline_window.bind('<Return>', lambda event: self.clean_timeline_window(event))
        self.timeline_window.bind('<Escape>', lambda event: self.clean_timeline_window(event))

        selected_row = self.products_tree.item(self.products_tree.selection())['values']
        if selected_row:
            product_code = selected_row[1]
            self.load_stock_timeline(product_code=product_code)

            btn_close.focus_set()

    def load_stock_timeline(self, product_code):
        self.timeline_tree.delete(*self.timeline_tree.get_children())

        rows = StockTimeline.get_timeline(product_code=product_code)
        row_num = 0
        for row in rows:
            row_num += 1

            rw = (row_num, row.entry_date, row.activity, row.change, row.available)
            if row_num % 2 == 0:
                self.timeline_tree.insert("", tk.END, values=rw, tags=('evenrow', row.product_code))
            else:
                self.timeline_tree.insert("", tk.END, values=rw, tags=('oddrow', row.product_code))

    def clean_timeline_window(self, event=None):
        self.window.wm_attributes("-disabled", False)
        self.timeline_window.destroy()

    def load_stock_value_details(self, event=None):
        total_quantity, total_stock_value = Stock.get_total_stock_value()
        self.var_total_quantity.set(total_quantity)
        self.var_total_stock_value.set(format_currency(total_stock_value, 'INR', locale='en_IN'))

        rows = Stock.get_stock_value_by_product()
        sl_no = 0
        for row in rows:
            product_name, stock_quantity, stock_value = row

            sl_no = sl_no + 1
            rw = (sl_no, product_name, stock_quantity, round(float(stock_value), 2))

            if sl_no % 2 == 0:
                self.stock_value_tree.insert("", tk.END, values=rw, tags=('evenrow', product_name))
            else:
                self.stock_value_tree.insert("", tk.END, values=rw, tags=('oddrow', product_name))

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

        rows = Stock.search_stock(product_name=product_name,
                                  product_type=product_type,
                                  product_size=product_size,
                                  selling_price=selling_price)

        self.products_tree.delete(*self.products_tree.get_children())

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

    def filter_by_quantity(self, event=None):
        try:
            self.var_filter_quantity.get()
        except:
            self.var_filter_quantity.set(0)

        quantity = int(self.var_filter_quantity.get())
        if quantity >= 0 and quantity != "":
            rows = Stock.get_stocks_by_quantity(quantity=quantity)

            self.products_tree.delete(*self.products_tree.get_children())
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
            self.reload_stock()

    def filter_by_product_code(self, event=None):
        product_code = f"{self.ety_filter_product_code_1.get().strip()}" \
                       f"-{self.ety_filter_product_code_2.get().strip()}" \
                       f"-{self.ety_filter_product_code_3.get().strip()}" \
                       f"-{self.ety_filter_product_code_4.get().strip()}"

        if product_code != "---":
            rows = Stock.search_stock(product_code=product_code)

            if rows:
                product, stock = rows

                self.products_tree.delete(*self.products_tree.get_children())
                sl_no = 1
                quantity = "-"
                if stock:
                    quantity = stock.quantity

                rw = (sl_no, product.product_code, product.product_name, product.product_type, product.product_size,
                      round(product.selling_price, 2), quantity)

                if sl_no % 2 == 0:
                    self.products_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
                else:
                    self.products_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))

                self.products_tree.selection_set(self.products_tree.tag_has(str(product.product_code)))
                self.products_tree.focus_set()
                self.selected_row = self.products_tree.selection()
                self.products_tree.focus(self.selected_row)
            else:
                messagebox.showerror("SS Fashion Tuty", f"Product_code: {product_code} not found!")
                print(f"Product_code: {product_code} not found!")

    def load_low_stock_details(self):
        rows = Stock.get_stocks_by_quantity(quantity=self.low_stock_quantity)
        sl_no = 0
        for row in rows:
            product = row.Product
            stock = row.Stock

            sl_no = sl_no + 1
            quantity = "-"
            if stock:
                quantity = stock.quantity

            rw = (sl_no, product.product_name, product.product_type, product.product_size,
                  round(product.selling_price, 2), quantity)

            if sl_no % 2 == 0:
                self.low_stock_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_name))
            else:
                self.low_stock_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_name))

    def reload_stock(self):
        self.ety_filter_product_name.delete(0, tk.END)
        self.ety_filter_product_type.delete(0, tk.END)
        self.ety_filter_product_size.delete(0, tk.END)
        self.ety_filter_product_sell_price.delete(0, tk.END)

        self.ety_filter_product_code_1.delete(0, tk.END)
        self.ety_filter_product_code_2.delete(0, tk.END)
        self.ety_filter_product_code_3.delete(0, tk.END)
        self.ety_filter_product_code_4.delete(0, tk.END)

        self.ety_filter_quantity.delete(0, tk.END)

        self.products_tree.delete(*self.products_tree.get_children())

        rows = Stock.get_all_active_stocks()
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

    def on_tree_select(self, event):
        self.selected_row = event.widget.selection()

        sales = self.products_tree.item(self.selected_row)['values']

        if sales:
            self.var_product_code.set(sales[1])
            self.var_product_name.set(sales[2])
            self.var_product_type.set(sales[3])
            self.var_product_size.set(sales[4])
            self.var_selling_price.set(sales[5])
            self.var_quantity.set(sales[6])
