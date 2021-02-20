import tkinter as tk
from datetime import datetime, date
from tkinter import TclError
from tkinter import messagebox
from tkinter import ttk

from babel.numbers import format_currency
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.Billing import Billing
from sshp.models.Product import Product
from sshp.models.Sales import Sales
from sshp.models.Stock import Stock
from sshp.models.StockTimeline import StockTimeline
from sshp.utilities.MaxLengthEntry import MaxLengthEntry

from sshp.models.Product_Lookup import Product_Lookup
import time
import cv2
from pyzbar import pyzbar


class AddSalesForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - Add Sales")

        # variables
        self.selected_row = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()
        self.sales_counter = 0

        # widgets
        self.products_tree = None
        self.sales_tree = None
        self.qty_window = None
        self.ety_search_product_id = None
        self.tree_container = None
        self.lbl_total_amount = None
        self.txt_receipt = None
        self.bill_date = None
        self.bill_no = None
        self.btn_save_bill = None
        self.filter_ety_product_name = None
        self.filter_ety_product_type = None
        self.filter_ety_product_size = None
        self.filter_ety_product_sell_price = None
        self.ety_search_product_code_1 = None
        self.ety_search_product_code_2 = None
        self.ety_search_product_code_3 = None
        self.ety_search_product_code_4 = None

        # widget variables
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        self.var_actual_price = tk.DoubleVar()
        self.var_quantity = tk.IntVar(value=1)
        self.var_available_quantity = tk.IntVar()
        self.var_total_amount = tk.StringVar()
        self.var_discount = tk.StringVar(value="0")
        self.var_bill_amount = tk.StringVar()
        self.var_search_product_code_1 = tk.StringVar()
        self.var_search_product_code_2 = tk.StringVar()
        self.var_search_product_code_3 = tk.StringVar()
        self.var_search_product_code_4 = tk.StringVar()

        self.ety_search_old_product_code = None
        self.var_search_old_product_code = tk.StringVar()
        self.ety_scan_product_code = None
        self.var_scan_product_code = tk.StringVar()

        self.load_add_sales_form()

        # shortcuts
        self.window.bind("<Control-s>", lambda event: self.save_bill(event))
        self.window.bind("<Control-S>", lambda event: self.save_bill(event))
        self.window.bind("<Control-p>", lambda event: self.print_bill(event))
        self.window.bind("<Control-P>", lambda event: self.print_bill(event))
        self.window.bind("<Control-n>", lambda event: self.clear_all(event))
        self.window.bind("<Control-N>", lambda event: self.clear_all(event))
        self.window.bind("<Control-e>", lambda event: self.calculate_bill_amount(event))
        self.window.bind("<Control-E>", lambda event: self.calculate_bill_amount(event))
        self.window.bind("<F1>", lambda event: self.select_first_row(event))

    def load_add_sales_form(self):
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

        bottom_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg=self.clr_yellow)
        bottom_button_container.pack(fill='both', expand=True, side=tk.BOTTOM)

        left_button_container = tk.Frame(bottom_button_container, relief=tk.RIDGE, bg=self.clr_yellow)
        left_button_container.pack(fill='x', expand=True, anchor='center', side=tk.LEFT)

        right_button_container = tk.Frame(bottom_button_container, relief=tk.RIDGE, bg=self.clr_yellow)
        right_button_container.pack(fill='x', expand=True, anchor='center', side=tk.RIGHT)

        # ********** left_search_container elements *********
        # lbl_search_product_code = tk.Label(search_container, text="Product Code: ", bg=self.clr_yellow)
        # lbl_search_product_code.grid(row=0, column=0, columnspan=3, sticky="nw", padx=1, pady=1)

        self.var_scan_product_code.trace("w", lambda name, index, mode, var_search_product_code=self.var_scan_product_code: self.callback(self.var_scan_product_code))
        self.ety_scan_product_code = tk.Entry(search_container, width=15, textvariable=self.var_scan_product_code)
        self.ety_scan_product_code.grid(row=0, column=0, columnspan=3, sticky="nw", padx=2, pady=2, ipady=5)
        # self.ety_search_product_code.bind('<Return>', lambda event: self.scan_entry(event, 3))

        btn_scan = tk.Button(search_container, text="Scan", bg=self.clr_blueiris, fg='white', command=self.scan_qr)
        btn_scan.grid(row=0, column=3, sticky="sw", padx=2, pady=1)
        btn_scan.bind('<Return>', lambda event: self.scan_qr(event))

        self.ety_search_old_product_code = MaxLengthEntry(search_container, maxlength=4, width=5,
                                                          textvariable=self.var_search_old_product_code)
        self.ety_search_old_product_code.grid(row=0, column=4, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_old_product_code.bind('<Return>', lambda event: self.search_old_product(event))

        self.ety_search_product_code_1 = MaxLengthEntry(search_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_1)
        self.ety_search_product_code_1.grid(row=1, column=0, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_1.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_search_product_code_2 = MaxLengthEntry(search_container, maxlength=3, width=4,
                                                        textvariable=self.var_search_product_code_2)
        self.ety_search_product_code_2.grid(row=1, column=1, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_2.bind('<Return>', lambda event: self.validate_entry(event, 3))

        self.ety_search_product_code_3 = MaxLengthEntry(search_container, maxlength=2, width=3,
                                                        textvariable=self.var_search_product_code_2)
        self.ety_search_product_code_3.grid(row=1, column=2, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_3.bind('<Return>', lambda event: self.validate_entry(event, 2))

        self.ety_search_product_code_4 = MaxLengthEntry(search_container, maxlength=4, width=5,
                                                        textvariable=self.var_search_product_code_3)
        self.ety_search_product_code_4.grid(row=1, column=3, sticky="nw", padx=2, pady=2, ipady=5)
        self.ety_search_product_code_4.bind('<Return>', lambda event: self.validate_entry(event, 4))

        btn_search = tk.Button(search_container, text="Search", bg=self.clr_fuchsia, fg='white',
                               command=self.search_product)
        btn_search.grid(row=1, column=4, sticky="sw", padx=2, pady=1)
        btn_search.bind('<Return>', lambda event: self.search_product(event))

        filter_lbl_product_name = tk.Label(filter_container, text="Name: ", bg=self.clr_yellow)
        filter_lbl_product_name.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_name = AutocompleteEntry(filter_container, width=15,
                                                         completevalues=self.product_name_list)
        self.filter_ety_product_name.grid(row=1, column=0, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_name.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_type = tk.Label(filter_container, text="Type: ", bg=self.clr_yellow)
        filter_lbl_product_type.grid(row=0, column=1, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_type = AutocompleteEntry(filter_container, width=18,
                                                         completevalues=self.product_type_list)
        self.filter_ety_product_type.grid(row=1, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_type.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_size = tk.Label(filter_container, text="Size: ", bg=self.clr_yellow)
        filter_lbl_product_size.grid(row=0, column=2, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_size = AutocompleteEntry(filter_container, width=12,
                                                         completevalues=self.product_size_list)
        self.filter_ety_product_size.grid(row=1, column=2, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_size.bind("<Return>", lambda event: self.filter_product(event))

        filter_lbl_product_price = tk.Label(filter_container, text="Price: ", bg=self.clr_yellow)
        filter_lbl_product_price.grid(row=0, column=3, sticky="nw", padx=1, pady=1)
        self.filter_ety_product_sell_price = AutocompleteEntry(filter_container, width=10,
                                                               completevalues=self.product_sell_price_list)
        self.filter_ety_product_sell_price.grid(row=1, column=3, sticky="nw", padx=2, pady=1, ipady=6)
        self.filter_ety_product_sell_price.bind("<Return>", lambda event: self.filter_product(event))

        btn_filter = tk.Button(filter_container, text="Filter", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_product)
        btn_filter.grid(row=1, column=4, sticky="news", padx=2, pady=1)
        btn_filter.bind("<Return>", lambda event: self.filter_product(event))

        btn_clear_filter = tk.Button(filter_container, text="Clear", command=self.reload_products)
        btn_clear_filter.grid(row=1, column=5, sticky="news", padx=2, pady=1)
        btn_clear_filter.bind("<Return>", lambda event: self.reload_products(event))

        lbl_bill_date = tk.Label(filter_container, text='Bill Date: ', bg=self.clr_yellow)
        lbl_bill_date.grid(row=0, column=4, sticky="nw", padx=1, pady=1)
        self.bill_date = DateEntry(filter_container, date_pattern='yyyy-mm-dd', background='yellow',
                                   foreground='black', borderwidth=2, width=10)
        self.bill_date.grid(row=0, column=5, sticky="sw", padx=2, pady=1, ipady=3)

        # ********** tree_containers elements *********
        products_tree_container = tk.Frame(left_container, pady=3, bg=self.clr_yellow, relief=tk.RIDGE)
        products_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE', 'SIZE', 'PRICE', '')
        self.products_tree = ttk.Treeview(products_tree_container, columns=header, height=8, show="headings",
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

        self.products_tree.heading("0", text="PRODUCT_CODE")
        self.products_tree.heading("1", text="PRODUCT_NAME")
        self.products_tree.heading("2", text="PRODUCT_TYPE")
        self.products_tree.heading("3", text="SIZE")
        self.products_tree.heading("4", text="PRICE")

        self.products_tree.column(0, anchor='center', width="80")
        self.products_tree.column(1, anchor=tk.W, width="150")
        self.products_tree.column(2, anchor=tk.W, width="200")
        self.products_tree.column(3, anchor='center', width="100")
        self.products_tree.column(4, anchor=tk.E, width="100")
        self.products_tree.column(5, anchor='center', width="5")

        numeric_cols = ['PRICE']
        self.reload_products()

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

        # ********** Product Details *********
        product_details_container = tk.Frame(left_container, bd=5, pady=3, padx=3, relief=tk.RIDGE, bg=self.clr_yellow)
        product_details_container.pack(fill='both', expand=True, side=tk.LEFT)

        product_details_container.grid_columnconfigure(0, weight=1)
        product_details_container.grid_columnconfigure(3, weight=1)

        lbl_product_details = tk.Label(product_details_container, text="Product Details", bg=self.clr_blueiris,
                                       fg="white")
        lbl_product_details.grid(row=0, column=1, columnspan=2, sticky="news", padx=3, pady=5)
        lbl_product_details.config(font=("Calibri bold", 14))

        lbl_product_id = tk.Label(product_details_container, text="Product Code: ", bg=self.clr_yellow)
        lbl_product_id.grid(row=1, column=1, sticky="nw", padx=3, pady=1)
        product_id = tk.Entry(product_details_container, width=15, textvariable=self.var_product_code, state='disabled')
        product_id.grid(row=1, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_name = tk.Label(product_details_container, text="Product Name: ", bg=self.clr_yellow)
        lbl_product_name.grid(row=2, column=1, sticky="nw", padx=3, pady=1)
        product_name = tk.Entry(product_details_container, textvariable=self.var_product_name,
                                state='disabled')
        product_name.grid(row=2, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_type = tk.Label(product_details_container, text="Product Type: ", bg=self.clr_yellow)
        lbl_product_type.grid(row=3, column=1, sticky="nw", padx=3, pady=1)
        product_type = tk.Entry(product_details_container, textvariable=self.var_product_type, state='disabled')
        product_type.grid(row=3, column=2, sticky="nw", padx=3, pady=1)

        lbl_product_size = tk.Label(product_details_container, text="Size: ", bg=self.clr_yellow)
        lbl_product_size.grid(row=4, column=1, sticky="nw", padx=3, pady=1)
        product_size = tk.Entry(product_details_container, width=10, textvariable=self.var_product_size,
                                state='disabled')
        product_size.grid(row=4, column=2, sticky="nw", padx=3, pady=1)

        lbl_selling_price = tk.Label(product_details_container, text="Price: ", bg=self.clr_yellow)
        lbl_selling_price.grid(row=5, column=1, sticky="nw", padx=3, pady=1)
        selling_price = tk.Entry(product_details_container, width=10, textvariable=self.var_selling_price,
                                 state='disabled')
        selling_price.grid(row=5, column=2, sticky="nw", padx=3, pady=1)

        btn_add = tk.Button(product_details_container, text="Add", bg=self.clr_fuchsia, fg='white',
                            command=self.add_sales_by_button)
        btn_add.grid(row=7, column=2, sticky="news", padx=1, pady=2)
        btn_add.config(font=("calibri bold", 12))

        # ********** Sales Tree Details *********
        sales_tree_container = tk.Frame(left_container, bd=5, pady=3, relief=tk.RIDGE, bg=self.clr_yellow)
        sales_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'PRODUCT_ID', 'PRODUCT', 'PRICE', 'QTY', 'AMOUNT', '')
        self.sales_tree = ttk.Treeview(sales_tree_container, columns=header, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(sales_tree_container, orient="vertical", command=self.sales_tree.yview)
        hsb = ttk.Scrollbar(sales_tree_container, orient="horizontal", command=self.sales_tree.xview)

        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.sales_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        sales_tree_container.grid_columnconfigure(0, weight=1)
        sales_tree_container.grid_rowconfigure(0, weight=1)

        self.sales_tree.heading("0", text="#")
        self.sales_tree.heading("1", text="PRODUCT_ID")
        self.sales_tree.heading("2", text="PRODUCT")
        self.sales_tree.heading("3", text="PRICE")
        self.sales_tree.heading("4", text="QTY")
        self.sales_tree.heading("5", text="AMOUNT")

        self.sales_tree.column(0, anchor='center', minwidth=50, width=50)
        self.sales_tree.column(3, anchor='center', minwidth=100, width=100)
        self.sales_tree.column(4, anchor='center', minwidth=100, width=100)
        self.sales_tree.column(5, anchor=tk.E, minwidth=100, width=100)
        self.sales_tree.column(6, anchor='center', width=5)
        self.sales_tree["displaycolumns"] = (0, 2, 3, 4, 5, 6)

        self.sales_tree.bind('<Double-1>', lambda event: self.remove_product(event))
        self.sales_tree.tag_configure("evenrow", background='#fbefcc')
        self.sales_tree.tag_configure("oddrow", background='white', foreground='black')

        self.products_tree.tag_configure("evenrow_active", background='#fbefcc')
        self.products_tree.tag_configure("oddrow_active", background='white', foreground='black')
        self.products_tree.tag_configure("evenrow_inactive", background='#fbefcc', foreground='red')
        self.products_tree.tag_configure("oddrow_inactive", background='white', foreground='red')

        self.products_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.products_tree.bind('<Double-1>', lambda event: self.get_quantity(event))
        self.products_tree.bind('<Return>', lambda event: self.get_quantity(event))

        # ********** bottom_button_container elements *********
        btn_new_bill = tk.Button(left_button_container, text="[N]ew Bill", bg=self.clr_blueiris, fg="white",
                                 command=self.clear_all)
        btn_new_bill.pack(side=tk.LEFT, expand=True, fill='both', padx=5, pady=1)
        btn_new_bill.config(font=("calibri bold", 20))

        btn_close = tk.Button(left_button_container, text="Close", command=self.window.destroy)
        btn_close.pack(side=tk.LEFT, expand=True, fill='both', padx=5, pady=1)
        btn_close.config(font=("calibri bold", 20))

        self.lbl_total_amount = tk.Label(right_button_container, fg='Red', relief=tk.RAISED,
                                         textvariable=self.var_total_amount, width=10)
        self.lbl_total_amount.pack(side=tk.RIGHT, expand=True, fill='both', padx=1, pady=1)
        self.lbl_total_amount.config(font=("calibri bold", 34))
        self.var_total_amount.set(format_currency(0, 'INR', locale='en_IN'))

        btn_calculate = tk.Button(right_button_container, text="Calculat[e]", bg=self.clr_fuchsia, fg='white',
                                  command=self.calculate_bill_amount)
        btn_calculate.pack(side=tk.RIGHT, fill='both', expand=True, padx=5, pady=1)
        btn_calculate.config(font=("calibri bold", 20))

        lbl_discount = tk.Label(right_button_container, text='Discount: ', bg=self.clr_yellow)
        lbl_discount.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=1)

        ety_discount = tk.Entry(right_button_container, width=5, textvariable=self.var_discount)
        ety_discount.pack(side=tk.LEFT, fill='x', expand=True, padx=5, pady=1)
        ety_discount.config(font=("calibri bold", 14))
        ety_discount.bind("<Button-1>", lambda event: self.clear_discount(event))

        # ********** bill_container elements *********
        self.txt_receipt = tk.Text(right_container, height=20, bg='white', bd=4, font=('Courier', 11), spacing1=5)
        self.txt_receipt.pack(side=tk.TOP, expand=True, fill='x', padx=1, pady=1)

        lbl_bill_amount = tk.Label(right_container, fg=self.clr_blueiris, relief=tk.RAISED,
                                   textvariable=self.var_bill_amount)
        lbl_bill_amount.pack(side=tk.TOP, expand=True, fill='x', padx=1, pady=1)
        lbl_bill_amount.config(font=("calibri bold", 46))
        self.var_bill_amount.set(format_currency(0, 'INR', locale='en_IN'))

        self.btn_save_bill = tk.Button(right_container, text="[S]ave Bill", bg=self.clr_limegreen,
                                       command=self.save_bill)
        self.btn_save_bill.pack(side=tk.LEFT, expand=True, fill='x', padx=1, pady=1)
        self.btn_save_bill.config(font=("calibri bold", 22))

        btn_print_bill = tk.Button(right_container, text="[P]rint Bill", bg=self.clr_fuchsia, fg='white',
                                   command=self.print_bill)
        btn_print_bill.pack(side=tk.RIGHT, expand=True, fill='x', padx=1, pady=1)
        btn_print_bill.config(font=("calibri bold", 22))

    def read_qrcodes(self, frame):
        qrcodes = pyzbar.decode(frame)
        for qrcode in qrcodes:
            x, y, w, h = qrcode.rect
            # 1
            qrcode_info = qrcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            self.var_scan_product_code.set(qrcode_info)
        return frame

    def scan_qr(self, event=None):
        self.var_scan_product_code.set("")
        camera = cv2.VideoCapture(0)
        capture_duration = 5
        start_time = time.time()

        while int(time.time() - start_time) < capture_duration:
            ret, frame = camera.read()
            frame = self.read_qrcodes(frame)
            cv2.imshow('QR code reader', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                exit(0)

            if self.var_scan_product_code.get().strip() != "":
                break

        camera.release()
        cv2.destroyAllWindows()

    def callback(self, sv):
        scan_code = sv.get().strip()
        self.search_product(scan_code=scan_code)

        if self.products_tree.tag_has(scan_code):
            self.products_tree.focus_set()
            self.products_tree.event_generate('<Return>')

    def remove_product(self, event):
        selected_row = event.widget.selection()[0]
        self.sales_tree.delete(selected_row)

        self.sales_counter = 0
        for child in self.sales_tree.get_children():
            self.sales_counter = self.sales_counter + 1
            row = self.sales_tree.item(child)["values"]
            row[0] = self.sales_counter

            self.sales_tree.delete(child)
            self.sales_tree.insert("", tk.END, values=row)

        self.calculate_bill_amount()

    @staticmethod
    def clear_discount(event):
        event.widget.delete(0, "end")
        return None

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

        products = Product.search_products(product_name=product_name,
                                           product_type=product_type,
                                           product_size=product_size,
                                           selling_price=selling_price)
        self.products_tree.delete(*self.products_tree.get_children())
        if products:
            row_num = 0
            for product in products:
                row_num += 1
                row = (product.product_code, product.product_name, product.product_type,
                       product.product_size, round(product.selling_price, 2))

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
        else:
            pass

    def search_product(self, event=None, scan_code=None):
        product_code = f"{self.ety_search_product_code_1.get().strip()}" \
                       f"-{self.ety_search_product_code_2.get().strip()}" \
                       f"-{self.ety_search_product_code_3.get().strip()}" \
                       f"-{self.ety_search_product_code_4.get().strip()}"

        if len(scan_code) == 15:
            product_code = scan_code

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
                        row = (product.product_code, product.product_name, product.product_type,
                               product.product_size, round(product.selling_price, 2),
                               round(product.actual_price, 2))

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

    def search_old_product(self, event=None):
        product_code_old = self.ety_search_old_product_code.get().strip()

        if product_code_old != "":
            products = Product_Lookup.get_product_by_code(product_code_old=product_code_old)
            if products is None:
                messagebox.showerror("SS Fashion Tuty", f"Product_code_old: {product_code_old} not found!")
                print(f"Product_code_old: {product_code_old} not found!")
            else:
                if isinstance(products, Product_Lookup):
                    self.products_tree.selection_set(self.products_tree.tag_has(str(products.product_code_new)))
                    self.products_tree.focus_set()
                    self.products_tree.focus(self.selected_row)

    def generate_bill_header(self, bill_no):
        self.txt_receipt.delete("1.0", tk.END)

        self.txt_receipt.insert(tk.END, "\n")
        self.txt_receipt.insert(tk.END, f"{'SS Fashion Tuty':^41}\n")
        self.txt_receipt.insert(tk.END, f"{'Thalamuthu Nagar Main Road':^41}\n")
        self.txt_receipt.insert(tk.END, f"{'Koilpillaivilai, Tuticorin - 628002':^41}\n")
        self.txt_receipt.insert(tk.END, f"{'Contact: +91 9942380164':^41}\n")
        self.txt_receipt.insert(tk.END, "\n")

        form_bill_date = datetime.strftime(datetime.strptime(
            self.bill_date.get(), '%Y-%m-%d'), '%d-%b-%Y')
        bill_date = datetime.strftime(datetime.now(), '%d-%b-%Y')
        bill_time = datetime.strftime(datetime.now(), '%I:%M:%S %p')
        if form_bill_date != bill_date:
            bill_date = form_bill_date
            bill_time = "00:00:01 AM"

        self.txt_receipt.insert(tk.END, f"{' Cashier: ' + self.logged_user.upper():<21}")
        self.txt_receipt.insert(tk.END, f"{' Date: ' + bill_date + ' ':>20}\n")

        self.txt_receipt.insert(tk.END, f"{' Bill No: ' + str(bill_no):<21}")
        self.txt_receipt.insert(tk.END, f"{' Time: ' + bill_time+ ' ':>20}\n")

        self.txt_receipt.insert(tk.END, f"\n{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"{'#':^4}")
        self.txt_receipt.insert(tk.END, f"{'Item':^15}")
        self.txt_receipt.insert(tk.END, f"{'Qty':^4}")
        self.txt_receipt.insert(tk.END, f"{'Price':^8}")
        self.txt_receipt.insert(tk.END, f"{'Amount':^8}\n")

        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")

    def generate_bill_footer(self, quantity_sum, discount, bill_amount):
        sub_total = float(bill_amount) + float(discount)
        self.txt_receipt.insert(tk.END, "\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"    {'SubTotal':<15}{quantity_sum:^4}{sub_total:>17}\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"    {'Discount':<15}{discount:>21}\n")

        self.txt_receipt.insert(tk.END, "\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")
        self.txt_receipt.insert(tk.END, f"    {'Total':<15}{bill_amount:>21}\n")
        self.txt_receipt.insert(tk.END, f"{'-' * 41}\n")

        self.txt_receipt.insert(tk.END, "\n\n")
        self.txt_receipt.insert(tk.END, f"{'Thank You & Visit again':^41}")
        self.txt_receipt.insert(tk.END, "\n")

    def print_bill(self, event=None):
        bill = self.txt_receipt.get("1.0", tk.END)

        file = open(f"data/bills/{str(self.bill_no)}.txt", 'w')
        file.write(bill)
        file.close()

        self.clear_all()

    def clear_all(self, event=None):
        self.ety_search_product_code_1.delete(0, tk.END)
        self.ety_search_product_code_2.delete(0, tk.END)
        self.ety_search_product_code_3.delete(0, tk.END)
        self.ety_search_product_code_4.delete(0, tk.END)

        self.sales_counter = 0
        self.var_total_amount.set(format_currency(0, 'INR', locale='en_IN'))
        self.sales_tree.delete(*self.sales_tree.get_children())
        self.var_discount.set("0")
        self.var_bill_amount.set(format_currency(0, 'INR', locale='en_IN'))
        self.btn_save_bill.config(state="normal")

        self.reload_products()

    def save_bill(self, event=None):
        # to prevent submission via shortcut
        btn_state = str(self.btn_save_bill['state'])
        if btn_state == "disabled":
            return

        self.calculate_bill_amount()
        amount = self.var_total_amount.get()[1:].replace(',', '')
        discount = float(self.var_discount.get())
        bill_amount = self.var_total_amount.get()[1:].replace(',', '')

        if float(bill_amount) > 0:
            sales_date = datetime.now()
            if self.bill_date.get() != datetime.now().strftime('%Y-%m-%d'):
                sales_date = datetime.strptime(self.bill_date.get() + ' 00:00:01', '%Y-%m-%d 00:00:01')

            bill = (sales_date, amount, discount, bill_amount)
            bill_no = Billing.create_bill(bill)
            self.bill_no = bill_no
            self.generate_bill_header(bill_no=bill_no)
            sl_no = 0
            quantity_sum = 0
            for child in self.sales_tree.get_children():
                product_code = self.sales_tree.item(child)["values"][1]
                product_name = self.sales_tree.item(child)["values"][2]
                price = self.sales_tree.item(child)["values"][3]
                quantity = self.sales_tree.item(child)["values"][4]
                sub_amount = self.sales_tree.item(child)["values"][5]

                sales = (sales_date, bill_no, product_code, quantity, sub_amount)
                Sales.add_sales(sales)

                stock = (product_code, quantity)
                Stock.compute_stock(stock)

                change = '-' + str(quantity)
                StockTimeline.add_timeline(date.today(), product_code, "Sales", change)

                sl_no += 1
                quantity_sum = quantity_sum + quantity

                product_name, size, *_ = product_name.split("|") + [" "]
                product_name = product_name.strip()
                size = size.strip()

                if len(size) > 0:
                    product_name = f"{product_name} '{size}'"

                parts, chars = divmod(len(product_name.strip()), 15)
                self.txt_receipt.insert(tk.END, f"{sl_no:^4}")
                self.txt_receipt.insert(tk.END, f"{product_name[:15].strip():<15}")
                self.txt_receipt.insert(tk.END, f"{quantity:^4}")
                self.txt_receipt.insert(tk.END, f"{price:>7}")
                self.txt_receipt.insert(tk.END, f"{sub_amount:>10}\n")

                parts = parts - 1
                if parts < 0:
                    chars = 0

                start_index = 15
                while parts > 0 or chars > 1:
                    self.txt_receipt.insert(tk.END, f"{' ':^4}")
                    self.txt_receipt.insert(tk.END, f"{product_name[start_index:(start_index+15)].strip():<15}")
                    self.txt_receipt.insert(tk.END, f"{' ':^4}")
                    self.txt_receipt.insert(tk.END, f"{' ':>7}")
                    self.txt_receipt.insert(tk.END, f"{' ':>10}\n")

                    start_index += 15
                    parts = parts - 1
                    if parts < 0:
                        chars = 0

            self.generate_bill_footer(quantity_sum=quantity_sum, discount=discount, bill_amount=bill_amount)
            self.btn_save_bill.config(state="disabled")
            messagebox.showinfo("SS Fashion Tuty", f"Bill No: {bill_no} Saved!")

    def calculate_total_amount(self):
        total_amount = 0
        for child in self.sales_tree.get_children():
            total_amount += float(self.sales_tree.item(child)["values"][5])

        self.var_total_amount.set(format_currency(total_amount, 'INR', locale='en_IN'))

    def calculate_bill_amount(self, event=None):
        self.calculate_total_amount()

        total_amount = self.var_total_amount.get()[1:].replace(',', '')

        try:
            discount = float(self.var_discount.get())
        except TclError:
            discount = 0.0

        self.var_total_amount.set(format_currency(float(total_amount) - discount, 'INR', locale='en_IN'))
        self.var_bill_amount.set(format_currency(float(total_amount) - discount, 'INR', locale='en_IN'))

    def get_quantity(self, event):
        self.selected_row = event.widget.selection()
        product = self.products_tree.item(self.selected_row)['values']

        if isinstance(product, str):
            return

        product = Stock.get_stock(product_code=product[0])
        self.var_available_quantity.set(product.quantity)

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

        self.window.after(1, lambda: self.window.focus_force())

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

        self.window.after(1, lambda: self.window.focus_force())
        if add_quantity:
            self.var_quantity.set(quantity)
            self.add_to_sales_list(event)

    def add_sales_by_button(self):
        self.products_tree.event_generate('<Return>')

    def add_to_sales_list(self, event):
        quantity = self.var_quantity.get()

        self.selected_row = event.widget.selection()
        product = self.products_tree.item(self.selected_row)['values']

        for child in self.sales_tree.get_children():
            if self.sales_tree.item(child)["values"][1] == product[0]:
                prev_quantity = self.sales_tree.item(child)["values"][4]
                price = self.sales_tree.item(child)["values"][3]

                quantity += prev_quantity
                self.sales_tree.set(child, "#4", quantity)
                self.sales_tree.set(child, "#5", float(price) * quantity)

                break
        else:
            product_name = product[1]
            product_type = str(product[2]).strip("-")
            product_size = str(product[3]).strip("-")

            if len(product_type) > 0:
                product_type = f"- {product_type}"

            if len(product_size) > 0:
                product_size = f"| {product_size}"

            product_short = f"{product_name} {product_type} {product_size}"
            self.sales_counter = self.sales_counter + 1
            row = (self.sales_counter, product[0], product_short, round(float(product[4]), 2), quantity,
                   round(float(product[4]), 2) * quantity)

            self.sales_tree.insert("", tk.END, values=row)

        self.calculate_total_amount()

        if len(self.products_tree.selection()) > 0:
            self.products_tree.selection_remove(self.products_tree.selection()[0])

        self.ety_search_product_code_1.focus()
        self.ety_search_product_code_1.selection_range(0, tk.END)

        self.ety_scan_product_code.focus()
        self.ety_scan_product_code.selection_range(0, tk.END)

    def reload_products(self, event=None):
        self.filter_ety_product_name.delete(0, tk.END)
        self.filter_ety_product_type.delete(0, tk.END)
        self.filter_ety_product_size.delete(0, tk.END)
        self.filter_ety_product_sell_price.delete(0, tk.END)

        self.products_tree.delete(*self.products_tree.get_children())

        products = Product.get_active_products()
        row_num = 0
        for product in products:
            row_num += 1
            row = (product.product_code, product.product_name, product.product_type, product.product_size,
                   round(product.selling_price, 2))

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
