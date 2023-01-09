# importing gui library
import tkinter as tk
import GetLoginInfo

sign_up_error_code = "none"
invalid_login_made = False
errors_made = False

# defining main functions
def create_account():
    # removing old stuff
    new.grid_remove()
    returning.grid_remove()
    sign_up.grid_remove()
    login.grid_remove()

    # changing main color
    window.config(bg="#47ffc2")

    # defining local variable as global
    global new_username_label, new_username, new_password_label, new_password, confirm_password_label, confirm_password, create_account_button, sign_up_error_code

    # creating all the thingys for create account screen
    new_username_label = tk.Label(window, text="Enter Username:", font="Calibri 18", bg="#47ffc2")
    new_username = tk.Entry(window, font="Calibri 18")
    new_password_label = tk.Label(window, text="Create Password:", font="Calibri 18", bg="#47ffc2")
    new_password = tk.Entry(window, font="Calibri 18", show="*")
    confirm_password_label = tk.Label(window, text="Confirm Password:", font="Calibri 18", bg="#47ffc2")
    confirm_password = tk.Entry(window, font="Calibri 18", show="*")
    create_account_button = tk.Button(window, text="Create Account", font="Calibri 18", bg="#186985", fg="white", command=verify_new_account)

    if sign_up_error_code == "username":
        username_error.grid_remove()
    elif sign_up_error_code == "mismatch":
        mismatch_error.grid_remove()
    elif sign_up_error_code == "passtooshort":
        passtooshort_error.grid_remove()

    # griding them thingys
    new_username_label.grid(row=1, column=1, padx=5, pady=25)
    new_username.grid(row=1, column=2, padx=5, pady=25)
    new_password_label.grid(row=2, column=1, padx=5, pady=25)
    new_password.grid(row=2, column=2, padx=5, pady=25)
    confirm_password_label.grid(row=3, column=1, padx=5, pady=25)
    confirm_password.grid(row=3, column=2, padx=5, pady=25)
    create_account_button.grid(row=4, column=1, pady=10, columnspan=2)

def sign_in():
    # clearing window for other stuff
    new.grid_remove()
    returning.grid_remove()
    sign_up.grid_remove()
    login.grid_remove()

    # changing screen color
    window.config(bg="#ff387e")

    # declaring all variable as global
    global enter_username_label, enter_username, enter_password_label, enter_password, sign_in_button, invalid_login, invalid_login_made

    # making all the thingys
    enter_username_label = tk.Label(window, text="Enter Username:", font="Calibri 18", bg="#ff387e")
    enter_username = tk.Entry(window, font="Calibri 18")
    enter_password_label = tk.Label(window, text="Enter Password:", font="Calibri 18", bg="#ff387e")
    enter_password = tk.Entry(window, font="Calibri 18", show="*")
    sign_in_button = tk.Button(window, text="Sign In", font="Calibri 18", bg="#186985", fg="white", command=validate_login)

    if invalid_login_made:
        invalid_login.grid_remove()
    else:
        invalid_login = tk.Button(window, text="Invalid Username or Password", font="Calibri 18", bg="#186985", fg="white", command=sign_in)
        invalid_login_made = True

    # gridding them thingys
    enter_username_label.grid(row=1, column=1, padx=5, pady=25)
    enter_username.grid(row=1, column=2, padx=5, pady=25)
    enter_password_label.grid(row=2, column=1, padx=5, pady=25)
    enter_password.grid(row=2, column=2, padx=5, pady=25)
    sign_in_button.grid(row=3, column=1, pady=10, columnspan=2)

def getlogininfo():
    global logininfo
    logininfo = GetLoginInfo.getLoginInfo()

# process of creating new account if it has unique username
def verify_new_account():
    # clearing everything before going to mainscreen
    new_username_label.grid_remove()
    new_username.grid_remove()
    new_password_label.grid_remove()
    new_password.grid_remove()
    confirm_password_label.grid_remove()
    confirm_password.grid_remove()
    create_account_button.grid_remove()

    getlogininfo()

    global sign_up_error_code

    if new_username.get() in logininfo:
        sign_up_error_code = "username"
        sign_up_error()
        return
    elif len(new_password.get()) < 8:
        sign_up_error_code = "passtooshort"
        sign_up_error()
        return
    elif new_password.get() != confirm_password.get():
        sign_up_error_code = "mismatch"
        sign_up_error()
        return

    GetLoginInfo.send_acc_details(new_username.get() + ":" + new_password.get())
    main_screen()

# logs user in if username and password match
def validate_login():
    # clearing everything before going to mainscreen
    enter_username_label.grid_remove()
    enter_username.grid_remove()
    enter_password_label.grid_remove()
    enter_password.grid_remove()
    sign_in_button.grid_remove()

    getlogininfo()

    # checking for username and password combo in doc
    if enter_username.get() + ":" + enter_password.get() in logininfo:
        main_screen()
    else:
        login_error()

def sign_up_error():
    global username_error, mismatch_error, passtooshort_error, errors_made

    if not errors_made:
        username_error = tk.Button(window, text="Username is Taken", font="Calibri 18", bg="#186985", fg="white", command=create_account)
        mismatch_error = tk.Button(window, text="Passwords do not Match", font="Calibri 18", bg="#186985", fg="white", command=create_account)
        passtooshort_error = tk.Button(window, text="Password is too Short", font="Calibri 18", bg="#186985", fg="white", command=create_account)
        errors_made = True

    if sign_up_error_code == "username":
        username_error.grid(padx=10, pady=10)
    elif sign_up_error_code == "mismatch":
        mismatch_error.grid(padx=10, pady=10)
    elif sign_up_error_code == "passtooshort":
        passtooshort_error.grid(padx=10, pady=10)

def login_error():
    invalid_login.grid(padx=10, pady=10)


def main_screen():
    window.config(bg="#186985")

# main window for tk
window = tk.Tk()
window.config(bg="#186985")

# defining labels
new = tk.Label(window, text="New to Service?", font="Calibri 20", bg="#47ffc2", width=20, padx=10)
returning = tk.Label(window, text="Returning Member", font="Calibri 20", bg="#ff387e", width=20, padx=10)

# defining buttons
sign_up = tk.Button(window, text="Sign Up", bg="#47ffc2", font="Calibri 15", width=15, borderwidth=5, command=create_account)
login = tk.Button(window, text="Login", bg="#ff387e", font="Calibri 15", width=15, borderwidth=5, command=sign_in)

# placing everything in window
new.grid(row=1, column=1, padx=5, pady=5)
returning.grid(row=1, column=2, padx=5, pady=5)
sign_up.grid(row=2, column=1, padx=5, pady=5)
login.grid(row=2, column=2, padx=5, pady=5)
window.mainloop()