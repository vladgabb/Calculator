from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import calendar
import datetime

def getMonthList(num_months):
    current_month = datetime.datetime.now().month
    months = []
    for i in range(num_months):
        month_name = calendar.month_name[(current_month + i - 1) % 12 + 1]
        months.append(month_name)
    return months


def getDaysInMonth(month_name):
    month_num = list(calendar.month_name).index(month_name)
    year = datetime.datetime.now().year
    days_in_month = calendar.monthrange(year, month_num)[1]
    return days_in_month

class Application:
    def __init__(self) -> None:
        self.__root = Tk()
        self.__root.title("Кредитный калькулятор")
        self.__root.geometry('850x520+400+150')
        self.__root.resizable(False, False)

        self.__menu = Menu(self.__root)
        self.__root.config(menu=self.__menu)

        self.__creditState = StringVar(value="annuity")

        self.__creditFrame = Frame(self.__root, width=850, height=520)
        self.__depositFrame = Frame(self.__root, width=850, height=520)

        self.__creditFrame.pack()

    def run(self):
        monthsDict = {
                "January": "Январь",
                "February": "Февраль",
                "March": "Март",
                "April": "Апрель",
                "May": "Май",
                "June": "Июнь",
                "July": "Июль",
                "August": "Август",
                "September": "Сентябрь",
                "October": "Октябрь",
                "November": "Ноябрь",
                "December": "Декабрь"
            }
        def creditCalculator():
            self.__depositFrame.pack_forget()
            self.__creditFrame.pack()
            self.__root.title("Кредитный калькулятор")

        def depositCalculator():
            self.__creditFrame.pack_forget()
            self.__depositFrame.pack()
            self.__root.title("Депозитный калькулятор")

        def calculateCredit():
            if not creditSumEntry.get():
                messagebox.showerror(message="Введите сумму кредита")
                return

            if not creditInterestRateEntry.get():
                messagebox.showerror(message="Введите процентую ставку")
                return

            if not creditTermEntry.get():
                messagebox.showerror(message="Введите срок кредитования")
                return
            
            if not creditSumEntry.get().replace('.', '1', 1).isdigit():
                messagebox.showerror(message="Сумма кредита должна быть числом")
                return

            if not creditInterestRateEntry.get().replace('.', '1', 1).isdigit():
                messagebox.showerror(message="Процентная ставка должна быть числом")
                return

            if not creditTermEntry.get().isdigit():
                messagebox.showerror(message="Срок кредитования должен быть целым числом")
                return

            creditResultTree.delete(*creditResultTree.get_children())

            match self.__creditState.get():
                case "annuity":

                    creditInterest = float(creditInterestRateEntry.get())

                    monthPercent = creditInterest/12/100
                    creditTerm = int(creditTermEntry.get())
                    creditSum = float(creditSumEntry.get())

                    annuityPayment = round(creditSum * ((monthPercent * (1 + monthPercent)**creditTerm)/((1 + monthPercent)**creditTerm - 1)), 2)
                    
                    months = getMonthList(creditTerm)

                    remainder = creditSum

                    count = 0

                    year = datetime.date.today().year

                    for month in months:

                        percent = round(remainder * (creditInterest/100) * getDaysInMonth(month)/365, 2)
                        creditBody = round(annuityPayment - percent, 2)

                        remainder = round(remainder - creditBody, 2) if remainder - creditBody > 0 else 0

                        if month == "January":
                            year += 1

                        creditResultTree.insert(parent='', index='end', iid=count, text='', values=(monthsDict.get(month) + ' ' + str(year), annuityPayment, percent, creditBody, remainder))

                        count += 1

                    overpayment.set(f"Перплата:\n{round(annuityPayment*creditTerm-creditSum, 2)}")

                case "diff":
                    creditInterest = float(creditInterestRateEntry.get())
                    creditTerm = int(creditTermEntry.get())
                    creditSum = float(creditSumEntry.get())

                    diffPayment = round(creditSum / creditTerm, 2)

                    months = getMonthList(creditTerm)

                    count = 0

                    year = datetime.date.today().year

                    remainder = creditSum

                    paymentSum = 0

                    for month in months:
                        percent = round(remainder * (creditInterest / 100) * getDaysInMonth(month) / 365, 2)

                        payment = round(diffPayment + percent, 2)

                        paymentSum += payment

                        remainder = round(remainder - diffPayment, 2) if remainder - diffPayment > 0 else 0

                        if month == "January":
                            year += 1

                        creditResultTree.insert(parent='', index='end', iid=count, text='', values=(monthsDict.get(month) + ' ' + str(year), payment, percent, diffPayment, remainder))

                        count += 1

                    overpayment.set(f"Перплата:\n{round(paymentSum-creditSum, 2)}")


        def calculateDeposit():
            if not depositSumEntry.get():
                messagebox.showerror(message="Введите сумму вклада")
                return

            if not depositInterestRateEntry.get():
                messagebox.showerror(message="Введите процентую ставку")
                return

            if not depositTermEntry.get():
                messagebox.showerror(message="Введите срок")
                return
            
            if not depositSumEntry.get().replace('.', '1', 1).isdigit():
                messagebox.showerror(message="Сумма вклада должна быть числом")
                return

            if not depositInterestRateEntry.get().replace('.', '1', 1).isdigit():
                messagebox.showerror(message="Процентная ставка должна быть числом")
                return

            if not depositTermEntry.get().isdigit():
                messagebox.showerror(message="Срок должен быть целым числом")
                return
            
            depositResultTree.delete(*depositResultTree.get_children())
            
            depositSum = float(depositSumEntry.get())

            depositTerm = int(depositTermEntry.get())

            depositInterestRate = float(depositInterestRateEntry.get())

            months = getMonthList(depositTerm)

            count = 0

            year = datetime.date.today().year

            remainder = depositSum

            percentSum = 0

            for month in months:
                percent = round(remainder * (depositInterestRate/100) / 365 * getDaysInMonth(month), 2)

                percentSum += percent

                remainder = round(remainder + percent, 2)

                if month == "January":
                    year += 1

                depositResultTree.insert(parent='', index='end', iid=count, text='', values=(monthsDict.get(month) + ' ' + str(year), percent, remainder))

                count += 1

            income.set(f"Выплата по процентам:\n{round(percentSum, 2)}")
        

        chooseCalculatorMenu = Menu(self.__menu)
        self.__menu.add_cascade(label="Выбрать калькулятор", menu=chooseCalculatorMenu)
        chooseCalculatorMenu.add_command(label="Кредитный калькулятор", command=creditCalculator)
        chooseCalculatorMenu.add_command(label="Депозитный калькулятор", command=depositCalculator)


        # КРЕДИТНЫЙ КАЛЬКУЛЯТОР

        overpayment = StringVar(value="")

        income = StringVar(value="")

        Radiobutton(self.__creditFrame, text="Аннуитетный платеж", variable=self.__creditState, value="annuity").place(x=10, y=10)
        Radiobutton(self.__creditFrame, text="Дифференцированный платеж", variable=self.__creditState, value="diff").place(x=180, y=10)

        ttk.Label(self.__creditFrame, text="Сумма кредита").place(x=10, y=50)
        creditSumEntry = ttk.Entry(self.__creditFrame)
        creditSumEntry.place(x=10, y=70)

        ttk.Label(self.__creditFrame, text="Процентная ставка").place(x=10, y=110)
        creditInterestRateEntry = ttk.Entry(self.__creditFrame)
        creditInterestRateEntry.place(x=10, y=130)

        ttk.Label(self.__creditFrame, text="Срок кредитования в месяцах").place(x=10, y=170)
        creditTermEntry = ttk.Entry(self.__creditFrame)
        creditTermEntry.place(x=10, y=190)

        ttk.Button(self.__creditFrame, text="Рассчитать", command=calculateCredit, width=17).place(x=10, y=230)

        ttk.Label(self.__creditFrame, textvariable=overpayment).place(x=10, y=270)

        creditScrollbarY = Scrollbar(self.__creditFrame)
        creditScrollbarY.place(x=810,y=41, height=440)

        creditResultTree = ttk.Treeview(self.__creditFrame, columns=("month", "payment", "percent", "creditBody", "remainder"), height=23, yscrollcommand=creditScrollbarY.set)
        creditResultTree.place(x=220, y=40)

        creditScrollbarY.config(command=creditResultTree.yview)

        creditResultTree.column("#0", width=0, stretch=NO)
        creditResultTree.column("month", width=110)
        creditResultTree.column("payment", width=110)
        creditResultTree.column("percent", width=110)
        creditResultTree.column("creditBody", width=150)
        creditResultTree.column("remainder", width=110)

        creditResultTree.heading("month", text="Месяц/Год")
        creditResultTree.heading("payment", text="Платеж")
        creditResultTree.heading("percent", text="Процент")
        creditResultTree.heading("creditBody", text="Тело кредита")
        creditResultTree.heading("remainder", text="Остаток")

        # ДЕПОЗИТЫНЙ КАЛЬКУЛЯТОР

        ttk.Label(self.__depositFrame, text="Сумма вклада").place(x=10, y=10)
        depositSumEntry = ttk.Entry(self.__depositFrame)
        depositSumEntry.place(x=10, y=30)

        ttk.Label(self.__depositFrame, text="Процентная ставка").place(x=10, y=70)
        depositInterestRateEntry = ttk.Entry(self.__depositFrame)
        depositInterestRateEntry.place(x=10, y=90)

        ttk.Label(self.__depositFrame, text="Срок вклада").place(x=10, y=130)
        depositTermEntry = ttk.Entry(self.__depositFrame)
        depositTermEntry.place(x=10, y=150)

        ttk.Button(self.__depositFrame, text="Рассчитать", command=calculateDeposit, width=17).place(x=10, y=190)

        ttk.Label(self.__depositFrame, textvariable=income).place(x=10, y=270)

        depositResultTree = ttk.Treeview(self.__depositFrame, columns=("month", "payout", "remainder"), height=23)
        depositResultTree.place(x=220, y=10)

        depositResultTree.column("#0", width=0, stretch=NO)
        depositResultTree.column("month", width=110)
        depositResultTree.column("payout", width=230)
        depositResultTree.column("remainder", width=230)

        depositResultTree.heading("month", text="Месяц")
        depositResultTree.heading("payout", text="Выплата")
        depositResultTree.heading("remainder", text="Остаток вклада")

        self.__root.mainloop()


def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()