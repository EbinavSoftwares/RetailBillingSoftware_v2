import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from sshp.forms.MainForm import MainForm
from sshp.models.User import User


# Login Class
class Login(MainForm):
    def __init__(self):
        super().__init__()

        # containers
        self.login_container = None

        # widgets
        self.ety_username = None
        self.btn_verify = None
        self.ety_secret_answer = None
        self.ety_new_password = None
        self.ety_confirm_password = None
        self.btn_submit = None

        # local tkinter variables
        self.var_username = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_new_password = tk.StringVar()
        self.var_confirm_password = tk.StringVar()
        self.var_secret_question = tk.StringVar()
        self.var_secret_answer = tk.StringVar()

        # local variables
        self.user_validated = None

        self.login_form()

    # launch login_form
    def login_form(self):
        """
        launch login form
        :return:
        """
        for widget in self.content_container.winfo_children():
            widget.destroy()
 
        for index in range(1, 9):
            self.menubar.entryconfig(index, state=tk.DISABLED)

        self.login_container = tk.Frame(self.content_container, bd=20, padx=10, pady=10, relief=tk.RIDGE,
                                        bg=self.clr_limegreen)
        self.login_container.pack(fill=None, expand=True, side=tk.TOP, anchor="center")

        # content_container elements
        self.var_username.set("")
        lbl_username = tk.Label(self.login_container, text="Username: ", bg=self.clr_limegreen)
        lbl_username.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        username = tk.Entry(self.login_container, textvariable=self.var_username)
        username.grid(row=0, column=1, columnspan=2, sticky="se", padx=5, pady=5)
        username.bind("<Return>", lambda x: self.validate_user())

        lbl_password = tk.Label(self.login_container, text="Password: ", bg=self.clr_limegreen)
        lbl_password.grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        password = tk.Entry(self.login_container, textvariable=self.var_password, show='*')
        password.grid(row=1, column=1, columnspan=2, sticky="se", padx=5, pady=5)
        password.bind("<Return>", lambda x: self.validate_user())

        btn_cancel = tk.Button(self.login_container, text="Cancel", command=self.window.destroy)
        btn_cancel.grid(row=2, column=1, rowspan=2, sticky="news", padx=5, pady=5)

        btn_login = tk.Button(self.login_container, text="Login", bg=self.clr_fuchsia, fg='White',
                              command=self.validate_user)
        btn_login.grid(row=2, column=2, rowspan=2, sticky="news", padx=5, pady=5)

        lbl_forgot_password = tk.Label(self.login_container, text="Forgot Password?", bg=self.clr_limegreen, fg="blue",
                                       cursor="hand2")
        lbl_forgot_password.grid(row=4, column=1, columnspan=2, sticky="nw", padx=5, pady=5)
        lbl_forgot_password.bind("<Button-1>", lambda x: self.forgot_password())

        self.window.title("SS Fashion Tuty - Login")

        # display window
        self.window.mainloop()

    def forgot_password_form(self):
        """
        launch forgot_password form
        :return: None
        """
        self.var_new_password.set("")
        self.var_confirm_password.set("")
        self.var_secret_question.set("")
        self.var_secret_answer.set("")

        fpassword_container = tk.Frame(self.content_container, bd=20, padx=10, pady=10, relief=tk.RIDGE, bg='#FFE845')
        fpassword_container.pack(expand=True, side=tk.TOP, anchor="center")

        # content_container elements
        lbl_username = tk.Label(fpassword_container, text="Username: ", bg='#FFE845')
        lbl_username.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.ety_username = tk.Entry(fpassword_container, textvariable=self.var_username)
        self.ety_username.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.btn_verify = tk.Button(fpassword_container, text="Verify", width=10, command=self.verify_username)
        self.btn_verify.grid(row=0, column=2, sticky="news", padx=5, pady=5)

        lbl_secret_question = tk.Label(fpassword_container, text="Secret Question: ", bg='#FFE845')
        lbl_secret_question.grid(row=1, column=0, sticky="news", padx=5, pady=5)
        ety_secret_question = tk.Entry(fpassword_container, textvariable=self.var_secret_question, state='disabled')
        ety_secret_question.grid(row=1, column=1, columnspan=2, sticky="news", padx=5, pady=5)

        lbl_secret_answer = tk.Label(fpassword_container, text="Answer: ", bg='#FFE845')
        lbl_secret_answer.grid(row=2, column=0, sticky="news", padx=5, pady=5)
        self.ety_secret_answer = tk.Entry(fpassword_container, show='*', textvariable=self.var_secret_answer,
                                          state='disabled')
        self.ety_secret_answer.grid(row=2, column=1, sticky="news", padx=5, pady=5)

        lbl_new_password = tk.Label(fpassword_container, text="New Passowrd: ", bg='#FFE845')
        lbl_new_password.grid(row=3, column=0, sticky="news", padx=5, pady=5)
        self.ety_new_password = tk.Entry(fpassword_container, width=10, textvariable=self.var_new_password,
                                         show='*', state='disabled')
        self.ety_new_password.grid(row=3, column=1, sticky="news", padx=5, pady=5)

        lbl_confirm_password = tk.Label(fpassword_container, text="Confirm New Passowrd: ", bg='#FFE845')
        lbl_confirm_password.grid(row=4, column=0, sticky="news", padx=5, pady=5)
        self.ety_confirm_password = tk.Entry(fpassword_container, width=10, textvariable=self.var_confirm_password,
                                             show='*', state='disabled')
        self.ety_confirm_password.grid(row=4, column=1, sticky="news", padx=5, pady=5)

        btn_cancel = tk.Button(fpassword_container, text="Cancel", width=10, command=self.login_form)
        btn_cancel.grid(row=5, column=1, rowspan=2, sticky="nw", padx=5, pady=5)

        self.btn_submit = tk.Button(fpassword_container, text="Submit", width=10, command=self.set_password,
                                    state='disabled')
        self.btn_submit.grid(row=5, column=1, rowspan=2, columnspan=2, sticky="ne", padx=5, pady=5)

        self.window.title("SS Fashion Tuty - Forgot Password")

    def forgot_password(self):
        """
        display forgot_password form
        :return:
        """
        for widget in self.content_container.winfo_children():
            widget.destroy()

        self.forgot_password_form()

    def verify_username(self):
        """
        validate user
        :return:
        """
        username = self.var_username.get().strip().lower()

        user = User.get_user(username)
        if user:
            self.ety_username.configure(state=tk.DISABLED)
            self.var_secret_question.set(user.secret_question)
            self.ety_secret_answer.configure(state=tk.NORMAL)
            self.ety_new_password.configure(state=tk.NORMAL)
            self.ety_confirm_password.configure(state=tk.NORMAL)
            self.btn_submit.configure(state=tk.NORMAL)
        else:
            messagebox.showerror("SS Fashion Tuty", f"username: '{username}' not found!")
            print(f"username: '{username}' not found!")

    def set_password(self):
        username = self.var_username.get().strip().lower()
        new_password = self.var_new_password.get()
        confirm_password = self.var_confirm_password.get()
        secret_answer = self.var_secret_answer.get().strip().lower()

        if len(new_password) <= 0:
            messagebox.showerror("SS Fashion Tuty", f"password must be 4 to 15 characters!")
            print(f"password must be 4 to 15 characters!")
            return

        if new_password != confirm_password:
            messagebox.showerror("SS Fashion Tuty", f"password and confirm_password are not same!")
            print(f"password and confirm_password are not same!")
            return

        if len(secret_answer) <= 0:
            messagebox.showerror("SS Fashion Tuty", f"secret_answer cannot be empty!")
            print(f"secret_answer cannot be empty!")
            return

        user = User.get_user(username)
        if user:
            if user.secret_answer == secret_answer:
                User.set_password(username, new_password)
                messagebox.showinfo("SS Fashion Tuty", f"user: {username} password changed!")
                print(f"user: {username} password changed!")

                self.login_form()
            else:
                messagebox.showerror("SS Fashion Tuty", f"secret_answer is incorrect!")
                print(f"secret_answer is incorrect!")
        else:
            messagebox.showerror("SS Fashion Tuty", f"username: '{username}' not found!")
            print(f"username: '{username}' not found!")

    def validate_user(self):
        username = self.var_username.get().strip().lower()
        password = self.var_password.get()

        user = User.get_user(username)
        if user:
            if user.password == password:
                self.user_validated = True
                MainForm.set(user.is_admin, username)
                self.update_username()

                print(f"username: '{username}' validated! and user_profile: {MainForm.is_admin_user}")

                for widget in self.content_container.winfo_children():
                    widget.destroy()

                self.show_menu(MainForm.is_admin_user)  # self.admin_user
            else:
                messagebox.showerror("SS Fashion Tuty", f"Invalid password!")
                print(f"Invalid password!")
        else:
            messagebox.showerror("SS Fashion Tuty", f"username: '{username}' is not registered!")
            print(f"username: '{username}' is not registered!")
