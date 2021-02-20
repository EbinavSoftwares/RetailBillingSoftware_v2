import tkinter as tk
from datetime import datetime

from PIL import Image, ImageTk
from dynaconf import settings

from sshp.utilities.Clock import Clock
from sshp.utilities.windows import set_dpi_awareness


# Main class
class MainForm:
    # class variables
    is_admin_user = None
    logged_user = None
    user_profile = None

    def __init__(self):
        # set dpi to make clear objects
        set_dpi_awareness()

        # colour codes
        self.clr_yellow = "#FFE845"
        self.clr_blueiris = "#2C46C4"
        self.clr_fuchsia = "#D234B0"
        self.clr_limegreen = "#03D930"

        self.stock_alert_value = settings.STOCK_ALERT_VALUE
        self.low_stock_quantity = settings.LOW_STOCK_QUANTITY

        self.plus_activity = settings.PLUS_ACTIVITY
        self.minus_activity = settings.MINUS_ACTIVITY

        # creating main window
        self.window = tk.Tk()
        self.window.option_add("*Font", "Calibri 12 bold")
        self.window['background'] = self.clr_yellow
        self.window.columnconfigure(0, weight=1)
        self.window.title("SS Fashion Tuty - Home")

        self.window.geometry("%dx%d" % (1366, 768))
        self.window.columnconfigure(0, weight=1)
        self.window.state("zoomed")

        # containers
        self.header_container = None
        self.content_container = None
        self.footer_container = None
        self.info_container_left = None
        self.banner_container = None
        self.info_container_right = None

        # form widgets
        self.menubar = None
        self.user_menu = None

        # form variables
        self.var_username = tk.StringVar()
        self.var_user_profile = tk.StringVar()

        # launch form
        self.main_form()

    # set username and user_profile
    def update_username(self):
        """
        set username and user_profile
        :return: None
        """
        self.var_username.set(MainForm.logged_user)
        self.var_user_profile.set(MainForm.user_profile)

    # set class variables
    @classmethod
    def set(cls, is_admin_user, logged_user):
        """
        Set class variables
        :param is_admin_user:
        :param logged_user:
        :return: None
        """
        cls.is_admin_user = is_admin_user
        cls.logged_user = logged_user

        if is_admin_user:
            cls.user_profile = "Admin"
        else:
            cls.user_profile = "Cashier"

    # main form
    def main_form(self):
        """
        Launch the main form
        :return: None
        """
        # menubar
        self.menubar = tk.Menu(self.window)

        # Sales and Billing
        sales_menu = tk.Menu(self.menubar, tearoff=0)
        sales_menu.add_command(label="Add Sales", command=lambda: self.load_content('Add Sales'))
        sales_menu.add_separator()
        sales_menu.add_command(label="View Sales", command=lambda: self.load_content('View Sales'))
        self.menubar.add_cascade(label="Sales", menu=sales_menu)

        # Stock
        stock_menu = tk.Menu(self.menubar, tearoff=0)
        stock_menu.add_command(label="Products", command=lambda: self.load_content('Products'))
        stock_menu.add_separator()
        stock_menu.add_command(label="Stocks", command=lambda: self.load_content('Stocks'))
        self.menubar.add_cascade(label="Products & Stocks", menu=stock_menu)

        # Purchase
        purchase_menu = tk.Menu(self.menubar, tearoff=0)
        purchase_menu.add_command(label="Add Purchase", command=lambda: self.load_content('Add Purchase'))
        purchase_menu.add_separator()
        purchase_menu.add_command(label="View Purchase", command=lambda: self.load_content('View Purchase'))
        self.menubar.add_cascade(label="Purchase", menu=purchase_menu)

        # Report
        report_menu = tk.Menu(self.menubar, tearoff=0)
        report_menu.add_command(label="Sales Report", command=lambda: self.load_content('Sales Report'))
        report_menu.add_separator()
        report_menu.add_command(label="Stock Report", command=lambda: self.load_content('Stock Report'))
        report_menu.add_separator()
        report_menu.add_command(label="Purchase Report", command=lambda: self.load_content('Purchase Report'))
        self.menubar.add_cascade(label="Report", menu=report_menu)

        # User
        self.user_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="User Management", menu=self.user_menu)

        # Cash
        cash_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Cash Management", menu=cash_menu)

        # Admin
        admin_menu = tk.Menu(self.menubar, tearoff=0)
        admin_menu.add_command(label="Generate Tag", command=lambda: self.load_content('Generate Tag'))
        self.menubar.add_cascade(label="Admin", menu=admin_menu)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)

        # Main Containers
        self.header_container = tk.Frame(self.window, relief=tk.RIDGE, bg=self.clr_blueiris)
        self.header_container.pack(fill='x', expand=False, side=tk.TOP, anchor="nw")

        self.content_container = tk.Frame(self.window, relief=tk.RIDGE, bg=self.clr_yellow)
        self.content_container.pack(fill='both', expand=True, side=tk.TOP, anchor="n")

        self.footer_container = tk.Frame(self.window, bd=5, pady=3, relief=tk.RIDGE, bg=self.clr_yellow)
        self.footer_container.pack(fill='x', expand=True, side=tk.TOP, anchor="s")

        # header_container elements
        self.info_container_left = tk.Frame(self.header_container, padx=5, relief=tk.RIDGE, bg=self.clr_blueiris)
        self.info_container_left.pack(fill='both', expand=True, side=tk.LEFT, anchor="ne")

        self.banner_container = tk.Frame(self.header_container, padx=5, relief=tk.RIDGE, bg=self.clr_blueiris)
        self.banner_container.pack(fill='both', expand=False, side=tk.LEFT, anchor="nw")

        self.info_container_right = tk.Frame(self.header_container, padx=5, relief=tk.RIDGE, bg=self.clr_blueiris)
        self.info_container_right.pack(fill='both', expand=True, side=tk.RIGHT, anchor="ne")

        # info_container_left elements
        lbl_user = tk.Label(self.info_container_left, font=('Calibri', 14), text='User: ', bg=self.clr_blueiris,
                            fg='white')
        lbl_user.grid(row=0, column=0, sticky='nw', padx=2)
        lbl_username = tk.Label(self.info_container_left, font=('Calibri bold', 14), text=self.logged_user,
                                textvariable=self.var_username, bg=self.clr_blueiris, fg='white')
        lbl_username.grid(row=0, column=1, sticky='nw', padx=2)

        lbl_profile = tk.Label(self.info_container_left, font=('Calibri', 14), text='Profile: ', bg=self.clr_blueiris,
                               fg='white')
        lbl_profile.grid(row=1, column=0, sticky='nw', padx=2)
        lbl_user_profile = tk.Label(self.info_container_left, font=('Calibri bold', 14), text=self.user_profile,
                                    textvariable=self.var_user_profile, bg=self.clr_blueiris, fg='white')
        lbl_user_profile.grid(row=1, column=1, sticky='nw', padx=2)

        # info_container_right elements
        lbl_title = tk.Label(self.info_container_right, font=('Calibri', 14), text='Date: ', bg=self.clr_blueiris,
                             fg='white')
        lbl_title.grid(row=0, column=0, sticky='nw', padx=2)
        lbl_time = Clock(self.info_container_right, seconds=False)
        lbl_time.configure(bg=self.clr_blueiris, fg='white')
        lbl_time.grid(row=0, column=1, sticky="nw", padx=2)

        lbl_title = tk.Label(self.info_container_right, font=('Calibri', 14), text='Day: ', bg=self.clr_blueiris,
                             fg='white')
        lbl_title.grid(row=1, column=0, sticky='nw', padx=2, pady=2)
        lbl_title = tk.Label(self.info_container_right, font=('Calibri bold', 14),
                             text=datetime.strftime(datetime.today(), '%A'), bg=self.clr_blueiris, fg='white')
        lbl_title.grid(row=1, column=1, sticky='nw', padx=2)

        # banner
        self.banner_container.columnconfigure(0, weight=1)
        self.banner_container.rowconfigure(0, weight=1)
        self.banner_container.original = Image.open('images/Header.png')
        resized = self.banner_container.original.resize((750, 50), Image.ANTIALIAS)
        self.banner_container.image = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        self.banner_container.display = tk.Label(self.banner_container, image=self.banner_container.image)
        self.banner_container.display.grid(row=0)

        # display menu
        self.window.config(menu=self.menubar)

    # show menu based on user_profile
    def show_menu(self, admin_user):
        """
        show menu based on user_profile
        :param admin_user:
        :return: None
        """
        if admin_user:
            for index in range(1, 9):
                self.menubar.entryconfig(index, state=tk.NORMAL)
        else:
            self.menubar.entryconfig('Sales', state=tk.NORMAL)
            self.menubar.entryconfig('User Management', state=tk.NORMAL)
            self.user_menu.entryconfig('Add New User', state=tk.DISABLED)
            self.user_menu.entryconfig('View Users', state=tk.DISABLED)
            self.menubar.entryconfig('Help', state=tk.NORMAL)

    # load appropriate form based on menu selection
    def load_content(self, form_name):
        """
        load appropriate form based on menu selection
        :param form_name: form name to be launched
        :return:
        """
        self.window.destroy()

        if form_name == 'Add Sales':
            from sshp.forms.AddSalesForm import AddSalesForm
            AddSalesForm()
        elif form_name == 'View Sales':
            from sshp.forms.ViewSalesForm import ViewSalesForm
            ViewSalesForm()
        elif form_name == 'Products':
            from sshp.forms.ProductForm import ProductForm
            ProductForm()
        elif form_name == 'Stocks':
            from sshp.forms.StockForm import StockForm
            StockForm()
        elif form_name == 'Add Purchase':
            from sshp.forms.AddPurchaseForm import AddPurchaseForm
            AddPurchaseForm()
        elif form_name == 'View Purchase':
            from sshp.forms.ViewPurchaseForm import ViewPurchaseForm
            ViewPurchaseForm()
        elif form_name == 'Sales Report':
            from sshp.forms.SalesReportForm import SalesReportForm
            SalesReportForm()
        elif form_name == 'Stock Report':
            from sshp.forms.StockReportForm import StockReportForm
            StockReportForm()
        elif form_name == 'Purchase Report':
            from sshp.forms.PurchaseReportForm import PurchaseReportForm
            PurchaseReportForm()
        elif form_name == 'Generate Tag':
            from sshp.forms.GenerateTagForm import GenerateTagForm
            GenerateTagForm()
        else:
            pass

    def sort_treeview(self, tv, col, numeric_sort, reverse):
        if numeric_sort:
            l = [(float(tv.set(k, col)), k) for k in tv.get_children('')]
        else:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]

        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda _col=col: self.sort_treeview(tv, _col, numeric_sort, not reverse))
