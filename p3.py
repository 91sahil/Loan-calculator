from tkinter import *
from tkinter.messagebox import *
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.geometry("800x740+200+30")
root.title("Loan Calculator")
f = ("Times New Roman", 25,)


lab_header = Label(root, text="Compute Loan Payment", font = ("Times New Roman", 30, "bold"))
lab_header.pack(pady=20)

lab_amount = Label(root, text="Loan Amount = ", font = f)
lab_amount.place(x=40,y=80)
ent_amount = Entry(root, font = f)
ent_amount.place(x=350,y=80)

lab_tenure = Label(root, text="Tenure (Month) = ", font = f)
lab_tenure.place(x=40,y=160)
ent_tenure = Entry(root, font = f)
ent_tenure.place(x=350,y=160)

lab_interest = Label(root, text="Interest Rate (%) = ", font = f)
lab_interest.place(x=40,y=240)
ent_interest = Entry(root, font = f)
ent_interest.place(x=350,y=240)

special_char_pattern = r'[!@#$%^&*()+=/\|"\'\',?]'

def is_valid_loan_amount(loan_amount):
    try:
        loan_amount = float(loan_amount)
        if loan_amount <= 0:
            showerror("Input Error", "Loan Amount must be a positive number.")
            return False
        return True
    except ValueError:
        showerror("Input Error", "Loan Amount must be a valid number.")
        return False

def is_valid_loan_tenure(loan_tenure):
    try:
        loan_tenure = int(loan_tenure)
        if loan_tenure <= 0:
            showerror("Input Error", "Loan Tenure must be a positive integer.")
            return False
        return True
    except ValueError:
        showerror("Input Error", "Loan Tenure must be a valid integer.")
        return False

def is_valid_interest_rate(interest_rate):
    try:
        interest_rate = float(interest_rate)
        if interest_rate <= 0:
            showerror("Input Error", "Interest Rate must be a positive number.")
            return False
        if not (0 <= interest_rate <= 100):  # Example limits, adjust as needed
            showerror("Input Error", "Interest Rate must be between 0 and 100.")
            return False
        return True
    except ValueError:
        showerror("Input Error", "Interest Rate must be a valid number.")
        return False

def calculate():
    try:
        loan_amount = ent_amount.get()
        loan_tenure = ent_tenure.get()
        interest_rate = ent_interest.get()

        # Check if any input is empty
        if not loan_amount or not loan_tenure or not interest_rate:
            showerror("Input Error", "All fields must be filled.")
            return

        # Validate loan amount
        if not is_valid_loan_amount(loan_amount):
            return

        # Validate loan tenure
        if not is_valid_loan_tenure(loan_tenure):
            return

        # Validate interest rate
        if not is_valid_interest_rate(interest_rate):
            return

        # Calculate EMI, total interest payable, and total payment
        emi = calculate_emi(float(loan_amount), int(loan_tenure), float(interest_rate))
        total_interest = emi * int(loan_tenure) - float(loan_amount)
        total_payment = emi * int(loan_tenure)

        # Update the labels with the results
        ent_emi.configure(text=round(emi,2))
        ent_total_interest.configure(text=round(total_interest,2)) 
        ent_total_payment.configure(text=round(total_payment,2))
         
        categories = ["EMI", "Total Interest", "Total Payment"]
        values = [emi, total_interest, total_payment]
        fig, ax = plt.subplots()
        ax.bar(categories, values)
        ax.set_xlabel("Categories")
        ax.set_ylabel("Amount")
        ax.set_title("Loan Payment Summary")
        canvas = FigureCanvasTkAgg(fig, master=vw)
        canvas.get_tk_widget().place(x=60,y=100)
        canvas.draw()

    except Exception as e:
        showerror("Issue", str(e))

def calculate_emi(loan_amount, loan_tenure, interest_rate):
    rate = interest_rate/1200  # Convert annual interest rate to monthly
    emi = (loan_amount * rate * (1 + rate) ** loan_tenure) / ((1 + rate) ** loan_tenure - 1)
    return emi

but_calc = Button(root, text="Calculate", font = f, command=calculate)
but_calc.place(x=200,y=320)

def clear():
	ent_amount.delete(0,END)
	ent_tenure.delete(0,END)
	ent_interest.delete(0,END)
	ent_emi.configure(text="")
	ent_total_interest.configure(text="")
	ent_total_payment.configure(text="")

but_clear = Button(root, text="Clear All", font = f, command=clear)
but_clear.place(x=500,y=320)

lab_emi = Label(root, text="EMI Amount = ", font = f)
lab_emi.place(x=40,y=420)
ent_emi = Label(root, text="", font = f)
ent_emi.place(x=350,y=420)

lab_total_interest = Label(root, text="Total Intrest Payable = ", font = f)
lab_total_interest.place(x=40,y=500)
ent_total_interest = Label(root, text="", font = f)
ent_total_interest.place(x=350,y=500)

lab_total_payment = Label(root, text="Total Payment = ", font = f)
lab_total_payment.place(x=40,y=580)
ent_total_payment = Label(root, text="", font = f)
ent_total_payment.place(x=350,y=580)

def f2():
	root.withdraw()
	vw.deiconify()
	calculate()


rootw_but_view = Button(root, text="View Graph", font = f, command=f2)
rootw_but_view.place(x=600,y=660)

def f3():
	vw.withdraw()
	root.deiconify()

vw = Tk()
vw.geometry("800x740+200+30")
vw.title("Graph")
vw_but_back_main = Button(vw, text = "Back", font = f, command = f3)
vw_but_back_main.pack(pady=20)

def f1():
	if askokcancel("Quit", "Do you want to exit"):
		root.destroy()
		vw.destroy()
root.protocol("WM_DELETE_WINDOW", f1)
vw.protocol("WM_DELETE_WINDOW", f1)

but_exit = Button(root, text="Exit", font = f, command=f1)
but_exit.place(x=60,y=660)

root.mainloop()