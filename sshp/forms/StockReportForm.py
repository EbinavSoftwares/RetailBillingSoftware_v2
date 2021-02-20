import tkinter as tk
from datetime import date
from tkinter import filedialog
from tkinter import ttk

import xlsxwriter

from sshp.forms.MainForm import MainForm
from sshp.models.ProductCategory import ProductCategory
from sshp.models.Stock import Stock

from sshp.models.Product import Product


class StockReportForm(MainForm):
    def __init__(self):
        super().__init__()

        self.window.title("SS Fashion Tuty - Stock Report")

        # variables
        self.stock_dict = dict()
        self.category = dict()

        # widgets
        self.product_name_tree = None
        self.cbo_product_category = None
        self.product_tree = None
        self.product_type_tree = None
        self.product_size_tree = None
        self.selected_row = None

        self.load_stock_report_form()

    def load_stock_report_form(self):
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.show_menu(MainForm.is_admin_user)
        self.update_username()

        self.get_category()

        # ********** Sub Containers *********
        left_container = tk.Frame(self.content_container, bd=5, padx=5, pady=2, relief=tk.RIDGE, bg=self.clr_yellow)
        left_container.pack(fill='y', expand=True, side=tk.LEFT)

        center_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg=self.clr_yellow)
        center_container.pack(fill='both', expand=True, side=tk.LEFT)

        right_container = tk.Frame(self.content_container, bd=5, padx=5, pady=5, relief=tk.RIDGE, bg=self.clr_yellow)
        right_container.pack(fill='both', expand=True, side=tk.RIGHT)

        # left_container elements
        left_top_button_container = tk.Frame(left_container, relief=tk.RIDGE, bg=self.clr_yellow)
        left_top_button_container.pack(fill='both', expand=True, side=tk.TOP)

        product_name_tree_container = tk.Frame(left_container, pady=3, bg=self.clr_yellow, relief=tk.RIDGE)
        product_name_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        lbl_product_category = tk.Label(left_top_button_container, text="Category:", bg=self.clr_yellow)
        lbl_product_category.grid(row=0, column=0, sticky="nw", padx=1, pady=1)
        self.cbo_product_category = ttk.Combobox(left_top_button_container, width=7, values=list(self.category.keys()))
        self.cbo_product_category.grid(row=0, column=1, sticky="nw", padx=2, pady=1, ipady=6)
        self.cbo_product_category.current(0)

        btn_export = tk.Button(left_top_button_container, text="Export Data", bg=self.clr_limegreen,
                               command=self.export_to_excel)
        btn_export.grid(row=0, column=3, sticky="news", padx=2, pady=1)
        # btn_export.config(font=("Calibri bold", 22))

        btn_refresh = tk.Button(left_top_button_container, text="Refresh", bg=self.clr_fuchsia, fg='white',
                                command=lambda: self.load_product_name_tree()) #category=self.cbo_product_category.get()))
        btn_refresh.grid(row=0, column=2, sticky="news", padx=2, pady=1)

        # ********** tree_containers elements *********
        # self.stock_tree = ttk.Treeview(stock_tree_container, height=25)
        # vsb = ttk.Scrollbar(stock_tree_container, orient="vertical", command=self.stock_tree.yview)
        # hsb = ttk.Scrollbar(stock_tree_container, orient="horizontal", command=self.stock_tree.xview)
        #
        # style = ttk.Style()
        # style.configure("Treeview.Heading", font=('Calibri', 12))
        # style.configure("Treeview", font=('Courier', 12), rowheight=25)
        #
        # self.stock_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        # self.stock_tree.grid(column=0, row=0, sticky='nsew', in_=stock_tree_container)
        #
        # vsb.grid(column=1, row=0, sticky='ns', in_=stock_tree_container)
        # hsb.grid(column=0, row=1, sticky='ew', in_=stock_tree_container)
        #
        # stock_tree_container.grid_columnconfigure(0, weight=1)
        # stock_tree_container.grid_rowconfigure(0, weight=1)
        #
        # self.stock_tree.bind('<<TreeviewOpen>>', self.handle_open_event)
        # self.stock_tree.bind('<<TreeviewSelect>>', self.on_report_tree_select)
        # self.load_report_tree(category='All')

        # ********** stock_tree_container elements *********
        header = ('#', 'PRODUCT_NAME', 'QTY', '')
        self.product_name_tree = ttk.Treeview(product_name_tree_container, columns=header, show="headings", height=25,
                                              selectmode="browse")
        vsb = ttk.Scrollbar(product_name_tree_container, orient="vertical", command=self.product_name_tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.product_name_tree.xview)

        self.product_name_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.product_name_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.product_name_tree.grid(column=0, row=0, sticky='nsew', in_=product_name_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=product_name_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=product_name_tree_container)

        product_name_tree_container.grid_columnconfigure(0, weight=1)
        product_name_tree_container.grid_rowconfigure(0, weight=1)

        self.product_name_tree.heading("0", text="#")
        self.product_name_tree.heading("1", text="PRODUCT_NAME")
        self.product_name_tree.heading("2", text="QTY")

        self.product_name_tree.column(0, anchor='center', width="35")
        self.product_name_tree.column(1, anchor=tk.W, width="140")
        self.product_name_tree.column(2, anchor='center', width="60")
        self.product_name_tree.column(3, anchor='center', width="2")

        self.load_product_name_tree()

        numeric_cols = ['#', 'PRODUCT_NAME', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.product_name_tree.heading(col, text=col,
                                               command=lambda _col=col: self.sort_treeview(
                                                   self.product_name_tree, _col,
                                                   numeric_sort=True, reverse=False))
            else:
                self.product_name_tree.heading(col, text=col,
                                               command=lambda _col=col: self.sort_treeview(
                                                   self.product_name_tree, _col,
                                                   numeric_sort=False, reverse=False))

        self.product_name_tree.tag_configure("evenrow", background='#fbefcc')
        self.product_name_tree.tag_configure("oddrow", background='white', foreground='black')
        self.product_name_tree.bind('<<TreeviewSelect>>', self.on_product_name_tree_select)

        # ********** tree_containers elements *********
        products_tree_container = tk.Frame(center_container, pady=1, bg=self.clr_yellow)
        products_tree_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'PRODUCT_CODE', 'PRODUCT_NAME', 'PRODUCT_TYPE', 'SIZE', 'SELL_PRICE',
                  'QTY', '')
        self.product_tree = ttk.Treeview(products_tree_container, columns=header, show="headings", height=7,
                                         selectmode="browse")
        vsb = ttk.Scrollbar(products_tree_container, orient="vertical", command=self.product_tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.product_tree.xview)

        self.product_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.product_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.product_tree.grid(column=0, row=0, sticky='nsew', in_=products_tree_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=products_tree_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=products_tree_container)

        products_tree_container.grid_columnconfigure(0, weight=1)
        products_tree_container.grid_rowconfigure(0, weight=1)

        self.product_tree.heading("0", text="#")
        self.product_tree.heading("1", text="PRODUCT_CODE")
        self.product_tree.heading("2", text="PRODUCT_NAME")
        self.product_tree.heading("3", text="PRODUCT_TYPE")
        self.product_tree.heading("4", text="SIZE")
        self.product_tree.heading("5", text="SELL_PRICE")
        self.product_tree.heading("6", text="QTY")

        self.product_tree.column(0, anchor='center', width="35")
        self.product_tree.column(1, anchor='center', width="120")
        self.product_tree.column(2, anchor=tk.W, width="140")
        self.product_tree.column(3, anchor=tk.W, width="150")
        self.product_tree.column(4, anchor='center', width="100")
        self.product_tree.column(5, anchor=tk.E, width="90")
        self.product_tree.column(6, anchor='center', width="60")
        self.product_tree.column(7, anchor='center', width="2")

        self.load_product_tree()

        numeric_cols = ['#', 'SELL_PRICE', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.product_tree.heading(col, text=col,
                                          command=lambda _col=col: self.sort_treeview(
                                               self.product_tree, _col,
                                               numeric_sort=True, reverse=False))
            else:
                self.product_tree.heading(col, text=col,
                                          command=lambda _col=col: self.sort_treeview(
                                               self.product_tree, _col,
                                               numeric_sort=False, reverse=False))

        self.product_tree.tag_configure("evenrow", background='#fbefcc')
        self.product_tree.tag_configure("oddrow", background='white', foreground='black')

        # ********** products_type_container elements *********
        product_type_container = tk.Frame(right_container, pady=1, bg=self.clr_yellow)
        product_type_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'PRODUCT_TYPE', 'QTY', '')
        self.product_type_tree = ttk.Treeview(product_type_container, columns=header, show="headings", height=7,
                                              selectmode="browse")
        vsb = ttk.Scrollbar(product_type_container, orient="vertical", command=self.product_tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.product_tree.xview)

        self.product_type_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.product_type_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.product_type_tree.grid(column=0, row=0, sticky='nsew', in_=product_type_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=product_type_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=product_type_container)

        product_type_container.grid_columnconfigure(0, weight=1)
        product_type_container.grid_rowconfigure(0, weight=1)

        self.product_type_tree.heading("0", text="#")
        self.product_type_tree.heading("1", text="PRODUCT_TYPE")
        self.product_type_tree.heading("2", text="QTY")

        self.product_type_tree.column(0, anchor='center', width="35")
        self.product_type_tree.column(1, anchor=tk.W, width="150")
        self.product_type_tree.column(2, anchor='center', width="60")
        self.product_type_tree.column(3, anchor='center', width="2")

        self.load_product_type_summary_tree()

        numeric_cols = ['#', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.product_type_tree.heading(col, text=col,
                                               command=lambda _col=col: self.sort_treeview(
                                                   self.product_tree, _col,
                                                   numeric_sort=True, reverse=False))
            else:
                self.product_type_tree.heading(col, text=col,
                                               command=lambda _col=col: self.sort_treeview(
                                                    self.product_tree, _col,
                                                    numeric_sort=False, reverse=False))

        self.product_type_tree.tag_configure("evenrow", background='#fbefcc')
        self.product_type_tree.tag_configure("oddrow", background='white', foreground='black')

        # ********** product_size_container elements *********
        product_size_container = tk.Frame(right_container, pady=1, bg=self.clr_yellow)
        product_size_container.pack(fill='both', expand=True, side=tk.TOP)

        header = ('#', 'PRODUCT_SIZE', 'QTY', '')
        self.product_size_tree = ttk.Treeview(product_size_container, columns=header, show="headings", height=7,
                                              selectmode="browse")
        vsb = ttk.Scrollbar(product_size_container, orient="vertical", command=self.product_tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.product_tree.xview)

        self.product_size_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 12))
        style.configure("Treeview", font=('Calibri', 12), rowheight=25)

        self.product_size_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.product_size_tree.grid(column=0, row=0, sticky='nsew', in_=product_size_container)

        vsb.grid(column=1, row=0, sticky='ns', in_=product_size_container)
        hsb.grid(column=0, row=1, sticky='ew', in_=product_size_container)

        product_size_container.grid_columnconfigure(0, weight=1)
        product_size_container.grid_rowconfigure(0, weight=1)

        self.product_size_tree.heading("0", text="#")
        self.product_size_tree.heading("1", text="PRODUCT_SIZE")
        self.product_size_tree.heading("2", text="QTY")

        self.product_size_tree.column(0, anchor='center', width="35")
        self.product_size_tree.column(1, anchor=tk.W, width="150")
        self.product_size_tree.column(2, anchor='center', width="60")
        self.product_size_tree.column(3, anchor='center', width="2")

        self.load_product_size_summary_tree()

        numeric_cols = ['#', 'QTY']
        for col in header:
            if col in numeric_cols:
                self.product_size_tree.heading(col, text=col,
                                               command=lambda _col=col: self.sort_treeview(
                                                   self.product_tree, _col,
                                                   numeric_sort=True, reverse=False))
            else:
                self.product_size_tree.heading(col, text=col,
                                               command=lambda _col=col: self.sort_treeview(
                                                   self.product_tree, _col,
                                                   numeric_sort=False, reverse=False))

        self.product_size_tree.tag_configure("evenrow", background='#fbefcc')
        self.product_size_tree.tag_configure("oddrow", background='white', foreground='black')

    def load_product_type_summary_tree(self):
        self.product_type_tree.delete(*self.product_type_tree.get_children())

        rows = Stock.get_all_active_stocks()
        sl_no = 0
        for row in rows:
            product = row.Product
            stock = row.Stock

            sl_no = sl_no + 1
            quantity = "-"
            if stock:
                quantity = stock.quantity

            rw = (sl_no, product.product_type, quantity)

            if sl_no % 2 == 0:
                self.product_type_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_type))
            else:
                self.product_type_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_type))

    def load_product_size_summary_tree(self):
        self.product_size_tree.delete(*self.product_size_tree.get_children())

        rows = Stock.get_all_active_stocks()
        sl_no = 0
        for row in rows:
            product = row.Product
            stock = row.Stock

            sl_no = sl_no + 1
            quantity = "-"
            if stock:
                quantity = stock.quantity

            rw = (sl_no, product.product_size, quantity)

            if sl_no % 2 == 0:
                self.product_size_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_size))
            else:
                self.product_size_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_type))

    def load_product_tree(self):
        self.product_tree.delete(*self.product_tree.get_children())

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
                self.product_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
            else:
                self.product_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))

    def get_category(self):
        categories = ProductCategory.get_all_categories()

        self.category = {
            'All': ''
        }

        for category in categories:
            self.category[category.category] = category.start_num[:1]

    def load_product_name_tree(self):
        self.product_name_tree.delete(*self.product_name_tree.get_children())

        rows = Stock.get_active_product_name_summary()
        sl_no = 0
        for row in rows:
            product_name = row[0]
            quantity = row[1]

            sl_no = sl_no + 1
            rw = (sl_no, product_name, quantity)
            if sl_no % 2 == 0:
                self.product_name_tree.insert("", tk.END, values=rw, tags=('evenrow', product_name))
            else:
                self.product_name_tree.insert("", tk.END, values=rw, tags=('oddrow', product_name))

        # self.product_name_tree.delete(*self.product_name_tree.get_children())
        #
        # products = Product.get_product_name_list()
        #
        # sl_no = 0
        # for product in products:
        #     sl_no = sl_no + 1
        #
        #     rw = (sl_no, product.product_name)
        #     if sl_no % 2 == 0:
        #         self.product_name_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_name))
        #     else:
        #         self.product_name_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_name))

    # def load_report_tree(self, category):
    #     self.stock_dict = dict()
    #     self.stock_tree.delete(*self.stock_tree.get_children())
    #
    #     rows = Stock.get_all_active_stocks()
    #     for row in rows:
    #         product = row.Product
    #         stock = row.Stock
    #
    #         if product.product_code.startswith(self.category.get(category)):
    #             if product.product_name not in self.stock_dict:
    #                 self.stock_dict[product.product_name] = dict()
    #
    #             if product.product_type not in self.stock_dict[product.product_name]:
    #                 self.stock_dict[product.product_name][product.product_type] = dict()
    #
    #             if product.product_size not in self.stock_dict[product.product_name][product.product_type]:
    #                 self.stock_dict[product.product_name][product.product_type][product.product_size] = stock.quantity
    #
    #     # calculate total quantity
    #     for pname in list(self.stock_dict):
    #         pname_qty = 0
    #         for ptype in list(self.stock_dict[pname]):
    #             ptype_qty = 0
    #             for psize in list(self.stock_dict[pname][ptype]):
    #                 ptype_qty = ptype_qty + int(self.stock_dict[pname][ptype][psize])
    #                 pname_qty = pname_qty + int(self.stock_dict[pname][ptype][psize])
    #             self.stock_dict[pname][f"{ptype} ({ptype_qty})"] = self.stock_dict[pname].pop(ptype)
    #         self.stock_dict[f"{pname} ({pname_qty})"] = self.stock_dict.pop(pname)
    #
    #     pname_no = 0
    #     for pname in self.stock_dict:
    #         pname_no += 1
    #         self.stock_tree.insert('', pname_no, f"i{pname_no + 1}", text=f"{pname}")
    #
    #         ptype_no = 0
    #         for ptype in self.stock_dict[pname]:
    #             ptype_no += 1
    #             self.stock_tree.insert(f"i{pname_no + 1}", 'end', f"i{pname_no + 1}.{ptype_no}", text=ptype)
    #
    #             psize_no = 0
    #             for psize in self.stock_dict[pname][ptype]:
    #                 psize_no += 1
    #                 self.stock_tree.insert(f"i{pname_no + 1}.{ptype_no}", 'end',
    #                                        f"i{pname_no + 1}.{ptype_no}.{psize_no}",
    #                                        text=f'{psize: <15}{self.stock_dict[pname][ptype][psize]}')

    # def open_children(self, parent):
    #     self.stock_tree.item(parent, open=True)
    #     for child in self.stock_tree.get_children(parent):
    #         self.open_children(child)
    #
    # def handle_open_event(self, event):
    #     self.open_children(self.stock_tree.focus())

    def export_to_excel(self):
        file = filedialog.asksaveasfilename(title="Select file", initialfile=f"OpenStock_{date.today()}.xlsx",
                                            filetypes=[("Excel file", "*.xlsx")])
        if file:
            workbook = xlsxwriter.Workbook(file)
            worksheet = workbook.add_worksheet()

            # Create a format to use in the merged range.
            head_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': 'yellow'
            })

            worksheet.merge_range('A1:D1', 'Open Stock Report', head_format)

            worksheet.write(1, 0, "Date:", head_format)
            worksheet.write(1, 1, f"{date.today()}", head_format)
            worksheet.write(1, 2, "User:", head_format)
            worksheet.write(1, 3, f"{self.logged_user}", head_format)

            worksheet.write(3, 0, "Name", head_format)
            worksheet.write(3, 1, "Type", head_format)
            worksheet.write(3, 2, "Size", head_format)
            worksheet.write(3, 3, "Qty", head_format)

            row = 4
            large_pname_row = 0
            large_ptype_row = 0
            large_psize_row = 0
            for pname in self.stock_dict:
                worksheet.write(row, 0, f"{pname}")
                if len(pname) > large_pname_row:
                    large_pname_row = len(pname)
                for ptype in self.stock_dict[pname]:
                    row += 1
                    worksheet.write(row, 1, f"{ptype}")
                    if len(ptype) > large_ptype_row:
                        large_ptype_row = len(ptype)

                    for psize in self.stock_dict[pname][ptype]:
                        row += 1
                        if len(psize) > large_psize_row:
                            large_psize_row = len(psize)
                        worksheet.write(row, 2, f"{psize}")
                        worksheet.write(row, 3, f"{self.stock_dict[pname][ptype][psize]}")
                row += 1

            worksheet.set_column(0, 0, large_pname_row)
            worksheet.set_column(1, 1, large_ptype_row)
            worksheet.set_column(2, 2, large_psize_row)
            worksheet.set_column(3, 3, large_psize_row)

            workbook.close()

    def on_product_name_tree_select(self, event):
        self.selected_row = event.widget.selection()

        product_name = self.product_name_tree.item(self.selected_row)['values'][1]

        if product_name:
            self.refresh_product_tree(product_name)
            self.refresh_product_type_summary_tree(product_name)
            self.refresh_product_size_summary_tree(product_name)

        #
        # self.selected_row = event.widget.focus()
        # print(self.selected_row)
        # product_name = self.product_name_tree.item(self.selected_row)['text']
        # print(product_name)
        # product_name = product_name[:product_name.rfind("(", 0)-1].strip()  # to get rid of quantity in parenthesis
        #
        # if product_name:
        #     self.refresh_product_tree(product_name)
        #     self.refresh_product_type_summary_tree(product_name)
        #     self.refresh_product_size_summary_tree(product_name)

    def refresh_product_tree(self, product_name):
        self.product_tree.delete(*self.product_tree.get_children())

        rows = Stock.get_all_active_stocks()
        sl_no = 0
        for row in rows:
            product = row.Product
            stock = row.Stock

            if product.product_name == product_name:

                sl_no = sl_no + 1
                quantity = "-"
                if stock:
                    quantity = stock.quantity

                rw = (sl_no, product.product_code, product.product_name, product.product_type, product.product_size,
                      round(product.selling_price, 2), quantity)

                if sl_no % 2 == 0:
                    self.product_tree.insert("", tk.END, values=rw, tags=('evenrow', product.product_code))
                else:
                    self.product_tree.insert("", tk.END, values=rw, tags=('oddrow', product.product_code))

        # self.product_tree.delete(*self.product_tree.get_children())
        #
        # rows = Stock.get_active_product_name_summary()
        # sl_no = 0
        # for row in rows:
        #     product_name = row[0]
        #     quantity = row[1]
        #
        #     if product_name == product_name:
        #         sl_no = sl_no + 1
        #         rw = (sl_no, product_name, quantity)
        #         if sl_no % 2 == 0:
        #             self.product_tree.insert("", tk.END, values=rw, tags=('evenrow', product_name))
        #         else:
        #             self.product_tree.insert("", tk.END, values=rw, tags=('oddrow', product_name))

    def refresh_product_type_summary_tree(self, product_name):
        self.product_type_tree.delete(*self.product_type_tree.get_children())

        rows = Stock.get_active_product_type_summary(product_name=product_name)
        sl_no = 0
        for row in rows:
            product_type = row[0]
            quantity = row[1]

            sl_no = sl_no + 1
            rw = (sl_no, product_type, quantity)
            if sl_no % 2 == 0:
                self.product_type_tree.insert("", tk.END, values=rw, tags=('evenrow', product_type))
            else:
                self.product_type_tree.insert("", tk.END, values=rw, tags=('oddrow', product_type))

    def refresh_product_size_summary_tree(self, product_name):
        self.product_size_tree.delete(*self.product_size_tree.get_children())

        rows = Stock.get_active_stock_size_summary(product_name=product_name)
        sl_no = 0
        for row in rows:
            product_size = row[0]
            quantity = row[1]

            sl_no = sl_no + 1
            rw = (sl_no, product_size, quantity)
            if sl_no % 2 == 0:
                self.product_size_tree.insert("", tk.END, values=rw, tags=('evenrow', product_size))
            else:
                self.product_size_tree.insert("", tk.END, values=rw, tags=('oddrow', product_size))
