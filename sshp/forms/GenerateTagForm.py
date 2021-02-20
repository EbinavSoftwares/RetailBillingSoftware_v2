import tkinter as tk
from datetime import datetime
from tkinter import TclError
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

import os

from babel.numbers import format_currency, format_decimal
from ttkwidgets.autocomplete import AutocompleteEntry

from sshp.forms.MainForm import MainForm
from sshp.models.LkpProductName import LkpProductName
from sshp.models.LkpProductSize import LkpProductSize
from sshp.models.LkpProductType import LkpProductType
from sshp.models.Product import Product
from sshp.models.Purchase import Purchase
from sshp.models.Stock import Stock
from sshp.models.StockTimeline import StockTimeline
from sshp.utilities.QR_Generator import QRGenerator


class GenerateTagForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - Generate Tag")

        # variables
        self.select_first_row_threshold = 10
        self.selected_row = list()
        self.product_name_list = list()
        self.product_type_list = list()
        self.product_size_list = list()
        self.product_sell_price_list = list()
        # self.product_actual_price_list = list()
        self.selected_products_counter = 0

        # widgets
        self.filter_ety_product_name = None
        self.filter_ety_product_type = None
        self.filter_ety_product_size = None
        self.filter_ety_product_sell_price = None
        # self.filter_ety_product_actual_price = None
        self.products_tree = None
        self.selected_products_tree = None
        # self.purchase_date = None
        # self.ety_garment_name = None
        self.qty_window = None
        self.image_label = None

        # widget variables
        self.var_product_code = tk.StringVar()
        self.var_product_name = tk.StringVar()
        self.var_product_type = tk.StringVar()
        self.var_product_size = tk.StringVar()
        self.var_selling_price = tk.DoubleVar()
        # self.var_actual_price = tk.DoubleVar()
        self.var_sheet_count = tk.IntVar()
        self.var_selected_quantity = tk.IntVar()
        self.var_available_quantity = tk.IntVar()
        self.var_quantity = tk.IntVar(value=1)

        self.load_generate_tag_purchase_form()

        # shortcuts
        self.window.bind("<F5>", lambda event: self.filter_product(event))
        self.window.bind("<F1>", lambda event: self.select_first_row(event))

    def load_generate_tag_purchase_form(self):
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

        right_bottom_container = tk.Frame(right_container, relief=tk.RIDGE, bg=self.clr_yellow)
        right_bottom_container.pack(fill='both', expand=True, side=tk.TOP)

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

        btn_filter = tk.Button(left_top_button_container, text="Apply Filter [F5]", bg=self.clr_fuchsia, fg='white',
                               command=self.filter_product)
        btn_filter.grid(row=1, column=4, sticky="news", padx=2, pady=1)

        btn_clear_filter = tk.Button(left_top_button_container, text="Clear", command=self.reload_products)
        btn_clear_filter.grid(row=1, column=5, sticky="news", padx=2, pady=1)

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
        lbl_selected_quantity = tk.Label(right_top_button_container, text="Quantity:", bg=self.clr_yellow)
        lbl_selected_quantity.grid(row=0, column=0, rowspan=2, sticky="se", padx=2, pady=1)
        lbl_selected_quantity.config(font=("calibri bold", 18))

        ety_selected_quantity = tk.Entry(right_top_button_container, width=5, textvariable=self.var_selected_quantity,
                                         disabledbackground=self.clr_limegreen, disabledforeground="white",
                                         justify=tk.CENTER, state='disabled')
        ety_selected_quantity.grid(row=0, column=1, rowspan=2, sticky="se", padx=2, pady=1)
        ety_selected_quantity.config(font=("calibri bold", 18))

        btn_generate_tag = tk.Button(right_top_button_container, text="Generate Tag", bg=self.clr_fuchsia, fg='white',
                                     command=self.generate_tag)
        btn_generate_tag.grid(row=0, column=2, rowspan=2, sticky="se", padx=2, pady=1)

        btn_clear = tk.Button(right_top_button_container, text="Clear", command=self.clear_all)
        btn_clear.grid(row=0, column=3, rowspan=2, sticky="se", padx=2, pady=1)

        purchase_tree_container = tk.Frame(right_tree_container, pady=1, relief=tk.RIDGE, bg=self.clr_yellow)
        purchase_tree_container.pack(fill='both', expand=True, side=tk.RIGHT)

        header = ('#', 'product_code', 'product_name', 'type', 'size', 'selling_price', 'quantity', 'dummy')
        self.selected_products_tree = ttk.Treeview(purchase_tree_container, columns=header, height=10, show="headings",
                                                   selectmode="browse")
        vsb = ttk.Scrollbar(purchase_tree_container, orient="vertical", command=self.selected_products_tree.yview)
        hsb = ttk.Scrollbar(purchase_tree_container, orient="horizontal", command=self.selected_products_tree.xview)

        self.selected_products_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.selected_products_tree.grid(column=0, row=0, sticky='nsew')

        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        purchase_tree_container.grid_columnconfigure(0, weight=1)
        purchase_tree_container.grid_rowconfigure(0, weight=1)

        self.selected_products_tree.heading("0", text="#")
        self.selected_products_tree.heading("1", text="Code")
        self.selected_products_tree.heading("2", text="Product")
        self.selected_products_tree.heading("3", text="Type")
        self.selected_products_tree.heading("4", text="Size")
        self.selected_products_tree.heading("5", text="Price")
        self.selected_products_tree.heading("6", text="Qty")
        self.selected_products_tree.heading("7", text="")

        self.selected_products_tree.column(0, anchor='center', minwidth=25, width=25)
        self.selected_products_tree.column(1, anchor=tk.W, minwidth=40, width=110)
        self.selected_products_tree.column(2, anchor=tk.W, minwidth=80, width=100)  # Product
        self.selected_products_tree.column(3, anchor=tk.W, minwidth=110, width=110)  # Type
        self.selected_products_tree.column(4, anchor='center', minwidth=50, width=50)    # Size
        self.selected_products_tree.column(5, anchor=tk.E, minwidth=50, width=50)  # Price
        self.selected_products_tree.column(6, anchor='center', minwidth=40, width=40)  # Qty
        self.selected_products_tree.column(7, anchor='center', width=1)
        self.selected_products_tree["displaycolumns"] = (0, 1, 2, 3, 4, 5, 6, 7)
        self.selected_products_tree.bind('<Double-1>', lambda event: self.remove_product(event))

        self.products_tree.tag_configure("evenrow_active", background='#fbefcc')
        self.products_tree.tag_configure("oddrow_active", background='white', foreground='black')
        self.products_tree.tag_configure("evenrow_inactive", background='#fbefcc', foreground='red')
        self.products_tree.tag_configure("oddrow_inactive", background='white', foreground='red')

        self.products_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.products_tree.bind('<Double-1>', lambda event: self.get_quantity(event))
        self.products_tree.bind('<Return>', lambda event: self.get_quantity(event))

        # ********** bottom_container elements *********
        image_container = tk.Frame(right_bottom_container, pady=1, bd=5, relief=tk.RIDGE, bg=self.clr_yellow)
        image_container.pack(fill='both', expand=True, side=tk.TOP)

        img = ImageTk.PhotoImage(Image.open(f"images/Sample.png").resize((250, 250), Image.ANTIALIAS))
        # img = ImageTk.PhotoImage(Image.open(f"images/Sample.png"))
        self.image_label = tk.Label(image_container, image=img, bg=self.clr_yellow)
        self.image_label.image = img
        self.image_label.pack(side="bottom", fill="both", expand="yes")

    def remove_product(self, event):
        selected_row = event.widget.selection()[0]
        self.selected_products_tree.delete(selected_row)

        self.selected_products_counter = 0
        for child in self.selected_products_tree.get_children():
            self.selected_products_counter = self.selected_products_counter + 1
            row = self.selected_products_tree.item(child)["values"]
            row[0] = self.selected_products_counter

            self.selected_products_tree.delete(child)
            self.selected_products_tree.insert("", tk.END, values=row)

        self.calculate_total_amount_and_sheet()

    def select_first_row(self, event=None):
        element_id = self.products_tree.get_children()[0]
        self.products_tree.focus_set()
        self.products_tree.focus(element_id)
        self.products_tree.selection_set(element_id)

    def generate_tag(self):
        if int(self.var_selected_quantity.get()) < 1 or int(self.var_selected_quantity.get()) > 15:
            messagebox.showerror("SS Fashion Tuty", f"Selected Quantity should be '1' to '15'!")
            print(f"Selected Quantity should be '1' to '15'!")
            return

        filename = f"images/price_tags/{datetime.strftime(datetime.now(), '%d_%b_%Y_%H%M%S')}.png"
        large_font = ImageFont.truetype('consolab.ttf', 16)
        normal_font = ImageFont.truetype('consolab.ttf', 14)
        image = Image.new(mode="RGB", size=(565, 500), color="white")
        draw = ImageDraw.Draw(image)

        start_x = 15
        start_y = 15
        rect_width = 165
        rect_height = 80
        qr_rect_width = 45
        gap_x = 18
        gap_y = 18
        pcode_x = 10
        pcode_y = rect_height - 18
        pname_y = 2

        col_num = 0
        row_num = 0
        for child in self.selected_products_tree.get_children():
            product_code = self.selected_products_tree.item(child)["values"][1]
            product_name = str(self.selected_products_tree.item(child)["values"][2])[:13]
            product_type = str(self.selected_products_tree.item(child)["values"][3])[:13]
            if product_type == "-":
                product_type = str(self.selected_products_tree.item(child)["values"][2])[13:26]

            product_size = str(self.selected_products_tree.item(child)["values"][4])[:8]
            sell_price = self.selected_products_tree.item(child)["values"][5]
            quantity = self.selected_products_tree.item(child)["values"][6]

            QRGenerator.generate_qr(product_code)

            while quantity > 0:
                # shape = [(start_x, start_y), (start_x + rect_width, start_y + rect_height)]
                # draw.rectangle(shape, fill="#ffffff", outline="#ABB2B9", width=2)

                qr_image = Image.open(f"images/qr_codes/{product_code}.png")
                image.paste(qr_image, (start_x+2, start_y+5))

                draw.text((start_x + qr_rect_width + 15, start_y + pname_y), product_name,
                          font=normal_font, fill=(0, 0, 0))
                draw.text((start_x + qr_rect_width + 15, start_y + pname_y + 15), product_type,
                          font=normal_font, fill=(0, 0, 0))
                draw.text((start_x + qr_rect_width + 15, start_y + pname_y + 30), f"SIZE:{product_size}",
                          font=normal_font, fill=(0, 0, 0))
                draw.text((start_x + qr_rect_width + 25, start_y + pname_y + 45), f"Rs.{sell_price}",
                          font=large_font, fill=(0, 0, 0))

                draw.text((start_x + pcode_x, start_y + pcode_y), product_code,
                          font=large_font, fill=(0, 0, 0))
                start_x = start_x + rect_width + gap_x
                quantity = quantity - 1

                col_num += 1
                if col_num == 3:
                    row_num += 1
                    start_y = start_y + rect_height + gap_y
                    start_x = 15

                    col_num = 0

            if row_num == 5:
                break

        image.save(filename)

        # img = ImageTk.PhotoImage(Image.open(f"images/Sample.png"))
        # self.image_label = tk.Label(image_container, image=img)
        # self.image_label.image = img
        # self.image_label.pack(side="bottom", fill="both", expand="yes")

        # img = ImageTk.PhotoImage(Image.open(filename))
        # self.image_label.image = img
        # img = ImageTk.PhotoImage(file=filename)
        img = ImageTk.PhotoImage(Image.open(filename).resize((260, 260), Image.ANTIALIAS))
        self.image_label['image'] = img
        img.image = img

        # self.image_label.pack(side="bottom", fill="both", expand="yes")

        # os.system(filename)
        # purchase_date = datetime.strptime(self.purchase_date.get(), "%Y-%m-%d")
        # garment_name = self.ety_garment_name.get().strip()
        #
        # if garment_name == "" or garment_name is None:
        #     messagebox.showerror("SS Fashion Tuty", f"Garment Name is missing!")
        #     print(f"Garment Name is missing!")
        #     return
        #
        # if self.selected_products_tree.get_children():
        #     for child in self.selected_products_tree.get_children():
        #         product_code = self.selected_products_tree.item(child)["values"][1]
        #         quantity = self.selected_products_tree.item(child)["values"][6]
        #
        #         purchase = (purchase_date, garment_name, product_code, quantity)
        #         Purchase.add_purchase(purchase)
        #
        #         stock = (product_code, quantity)
        #         Stock.upload_stock(stock)
        #
        #         if StockTimeline.get_timeline(product_code=product_code):
        #             activity = "Add Purchase"
        #         else:
        #             activity = "Opening Stock"
        #
        #         StockTimeline.add_timeline(entry_date=purchase_date, product_code=product_code, activity=activity,
        #                                    change=f"+{quantity}")
        #
        #     messagebox.showinfo("SS Fashion Tuty", f"Purchase added Successfully!")
        #     self.clear_all()

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
        # self.ety_garment_name.delete(0, tk.END)
        self.selected_products_counter = 0
        self.selected_products_tree.delete(*self.selected_products_tree.get_children())
        self.var_sheet_count.set(format_decimal(0, locale='en_US'))
        self.var_selected_quantity.set(format_decimal(0, locale='en_US'))

        self.reload_products()
        self.selected_row = list()

    def calculate_total_amount_and_sheet(self):
        total_sheet = 0
        total_quantity = 0
        for child in self.selected_products_tree.get_children():
            total_sheet += int(self.selected_products_tree.item(child)["values"][6])
            total_quantity += int(self.selected_products_tree.item(child)["values"][6])

        self.var_sheet_count.set(format_decimal(total_sheet, locale='en_US'))
        self.var_selected_quantity.set(format_decimal(total_quantity, locale='en_US'))

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
            self.add_to_selected_list(event)

    def add_to_selected_list(self, event):
        quantity = self.var_quantity.get()

        self.selected_row = event.widget.selection()
        product = self.products_tree.item(self.selected_row)['values']

        active_product = Product.get_product_status(product_code=product[0])
        if not active_product:
            msg_box = messagebox.askquestion(
                "SS Fashion Tuty", "In-Active product! - Do you want to add this Product to selected list?",
                icon='question'
            )
            if msg_box == 'no':
                return

        for child in self.selected_products_tree.get_children():
            if self.selected_products_tree.item(child)["values"][1] == product[0]:
                prev_quantity = self.selected_products_tree.item(child)["values"][6]

                quantity += prev_quantity
                self.selected_products_tree.set(child, "#7", quantity)

                break
        else:
            self.selected_products_counter = self.selected_products_counter + 1
            row = (self.selected_products_counter, product[0], product[1], product[2], product[3], product[4],
                   quantity)

            self.selected_products_tree.insert("", tk.END, values=row)

        self.calculate_total_amount_and_sheet()

        if len(self.products_tree.selection()) > 0:
            self.products_tree.selection_remove(self.products_tree.selection()[0])

    def reload_products(self):
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
