from tkinter import *
from tkinter import messagebox,ttk
# Database functionality disabled - pymysql import removed
# import pymysql 

import time
import os 
import tempfile

# ========================================================================
# STANDALONE GROSS-UP PAYROLL CALCULATION MODULE
# ========================================================================
# Excel-Ready: This function can process salary data from Excel rows
# Usage: result = calculate_gross_up_salary({'Basic Pay': 50000, 'PF Percentage': 12, ...})
# ========================================================================

def calculate_gross_up_salary(data: dict) -> dict:
    """
    Calculate Gross-Up salary with Inclusion and Exclusion components.
    
    GROSS-UP FORMULA EXPLANATION:
    ------------------------------
    When net/take-home salary needs to be maintained, we use gross-up calculation:
    
    Gross Salary = Total Inclusions / (1 - Total Deduction Rate)
    
    Example:
    - If Basic=50000, HRA=10000, OT=5000, Other=2000
    - Total Inclusions = 67000
    - If PF% = 12% (rate = 0.12)
    - Gross = 67000 / (1 - 0.12) = 67000 / 0.88 = 76136.36
    - PF Amount = Basic × 12% = 50000 × 0.12 = 6000
    - Net Salary = Gross - PF - Other Deductions
    
    KEY PRINCIPLE:
    - PF is ALWAYS calculated on Basic Pay only, NOT on Gross
    - Gross-up ensures that inclusion components remain constant
    - As deduction % increases, gross automatically increases to compensate
    
    Args:
        data (dict): Input salary components with keys:
            - 'Basic Pay' (float): Required - Base salary for PF calculation
            - 'HRA' (float): Optional - House Rent Allowance
            - 'Over Time' (float): Optional - Overtime pay
            - 'Other Allowances' (float): Optional - Additional allowances
            - 'PF Percentage' (float): Optional - Default 12%
            - 'Other Deductions' (float): Optional - Additional deductions
    
    Returns:
        dict: Calculated salary breakdown with keys:
            - All input components (echoed back)
            - 'PF Amount' (float): Calculated PF = Basic × PF%
            - 'Total Inclusions' (float): Sum of all inclusion components
            - 'Total Deductions' (float): PF + Other Deductions
            - 'Gross Salary' (float): Grossed-up salary
            - 'Net Salary' (float): Take-home = Gross - Total Deductions
    
    Excel Integration Example:
    --------------------------
    # If Excel has columns: Basic, HRA, OT, Other_Allow, PF_Percent
    # Row data can be directly converted to dict:
    excel_row = {'Basic Pay': row['Basic'], 'HRA': row['HRA'], ...}
    result = calculate_gross_up_salary(excel_row)
    """
    
    # Extract input values with defaults
    basic_pay = float(data.get('Basic Pay', 0))
    hra = float(data.get('HRA', 0))
    over_time = float(data.get('Over Time', 0))
    other_allowances = float(data.get('Other Allowances', 0))
    pf_percentage = float(data.get('PF Percentage', 12))  # Default 12%
    other_deductions = float(data.get('Other Deductions', 0))
    
    # Validation
    if basic_pay <= 0:
        raise ValueError("Basic Pay must be greater than 0")
    if pf_percentage < 0 or pf_percentage > 100:
        raise ValueError("PF Percentage must be between 0 and 100")
    
    # Calculate Total Inclusions (components that add to salary)
    total_inclusions = basic_pay + hra + over_time + other_allowances
    
    # Calculate PF Amount (ALWAYS based on Basic Pay only)
    pf_rate = pf_percentage / 100
    pf_amount = basic_pay * pf_rate
    
    # GROSS-UP CALCULATION
    # Formula: Gross = Inclusions / (1 - PF_Rate)
    # This ensures that after PF deduction, employee gets the intended inclusions
    if pf_rate >= 1.0:
        raise ValueError("PF Percentage cannot be 100% or more (would result in infinite gross)")
    
    gross_salary = total_inclusions / (1 - pf_rate)
    
    # Calculate Total Deductions
    total_deductions = pf_amount + other_deductions
    
    # Calculate Net/Take-Home Salary
    net_salary = gross_salary - total_deductions
    
    # Return comprehensive breakdown
    result = {
        # Input components (for reference)
        'Basic Pay': basic_pay,
        'HRA': hra,
        'Over Time': over_time,
        'Other Allowances': other_allowances,
        'PF Percentage': pf_percentage,
        'Other Deductions': other_deductions,
        
        # Calculated values
        'Total Inclusions': total_inclusions,
        'PF Amount': pf_amount,
        'Total Deductions': total_deductions,
        'Gross Salary': gross_salary,
        'Net Salary': net_salary
    }
    
    return result

# ========================================================================
# EXAMPLE USAGE (for testing)
# ========================================================================
# sample_data = {
#     'Basic Pay': 50000,
#     'HRA': 10000,
#     'Over Time': 5000,
#     'Other Allowances': 2000,
#     'PF Percentage': 12,
#     'Other Deductions': 1000
# }
# result = calculate_gross_up_salary(sample_data)
# print(f"Gross Salary: {result['Gross Salary']:.2f}")
# print(f"Net Salary: {result['Net Salary']:.2f}")
# ========================================================================

class EmployeeSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll Management System")
        self.root.geometry("1350x700+0+0") 
        self.root.config(bg="white")
        Title = Label(self.root, text="Employee Payroll Management System", font=("times new roman", 30, "bold"), bg="#262626", fg="white",anchor="w",padx=10)
        Title.place(x=0, y=0, relwidth=1)
        btn_show_emp = Button(self.root,command=self.view_all ,text="View All Records", font=("times new roman",15), bg="white", fg="black", padx=10)
        btn_show_emp.place(x=1190, y=10,height=27,width=150)
        
        #Frame1
        #Variables
        self.var_emp_code=StringVar()
        self.var_emp_designation=StringVar()
        self.var_emp_name=StringVar()
        self.var_emp_age=StringVar()
        self.var_emp_gender=StringVar()
        self.var_emp_email=StringVar()
        self.var_emp_hl=StringVar()
        self.var_emp_dob=StringVar()
        self.var_emp_doj=StringVar()
        self.var_emp_exp=StringVar()
        self.var_emp_pid=StringVar()
        self.var_emp_contact=StringVar()
        self.var_emp_status=StringVar()
        
        Frame1=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        Frame1.place(x=10,y=70,width=750,height=650)
        Title1 =Label(Frame1, text="Employee Details", font=("times new roman", 20, "bold"), bg="lightgray", fg="black",anchor="w",padx=10)
        Title1.place(x=0, y=0, relwidth=1)

        lbl_code = Label(Frame1, text="Employee Code", font=("times new roman", 20, "bold"), bg="white", fg="black",anchor="w",padx=10)
        lbl_code.place(x=10, y=50)
        self.entry_code = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_code, bg="light yellow", fg="black", justify="left")
        self.entry_code.place(x=210, y=55,width=200)
        btn_search = Button(Frame1, command=self.search, text="Search", font=("times new roman",17), bg="white", fg="black", padx=10)
        btn_search.place(x=430, y=55,height=27)

        #ROW 1
        lbl_designation = Label(Frame1, text="Designation", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_designation.place(x=10, y=100)
        entry_designation = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_designation, bg="light yellow", fg="black", justify="left").place(x=170, y=105,width=200)

        lbl_DOB = Label(Frame1, text="D.O.B", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_DOB.place(x=380, y=100)
        entry_DOB= Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_dob, bg="light yellow", fg="black", justify="left").place(x=490, y=105)

        #ROW 2
        lbl_name= Label(Frame1, text="Name", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_name.place(x=10, y=150)
        entry_name = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_name, bg="light yellow", fg="black", justify="left").place(x=170, y=155,width=200)

        lbl_DOJ = Label(Frame1, text="D.O.J", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_DOJ.place(x=380, y=150)
        entry_DOJ= Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_doj, bg="light yellow", fg="black", justify="left").place(x=490, y=155)

        #ROW 3
        lbl_age= Label(Frame1, text="Age", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_age.place(x=10, y=200)
        entry_age = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_age, bg="light yellow", fg="black", justify="left").place(x=170, y=205,width=200)

        lbl_experince = Label(Frame1, text="Experince", font=("times new roman", 17), bg="white", fg="black", anchor="w", padx=10)
        lbl_experince.place(x=380, y=200)
        entry_experince= Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_exp, bg="light yellow", fg="black", justify="left").place(x=490, y=205)

        #ROW 4
        lbl_gender= Label(Frame1, text="Gender", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_gender.place(x=10, y=250)
        entry_gender = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_gender, bg="light yellow", fg="black", justify="left").place(x=170, y=255,width=200)

        lbl_proof = Label(Frame1, text="Proof ID", font=("times new roman", 17), bg="white", fg="black", anchor="w", padx=10)
        lbl_proof.place(x=380, y=250)
        entry_proof= Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_pid, bg="light yellow", fg="black", justify="left").place(x=490, y=255)

        #ROW 5
        lbl_email= Label(Frame1, text="Email", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_email.place(x=10, y=300)
        entry_email = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_email, bg="light yellow", fg="black", justify="left").place(x=170, y=305,width=200)

        lbl_contact = Label(Frame1, text="Contact", font=("times new roman", 17), bg="white", fg="black", anchor="w", padx=10)
        lbl_contact.place(x=380, y=300)
        entry_contact= Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_contact, bg="light yellow", fg="black", justify="left").place(x=490, y=305)

        #ROW 6
        lbl_hired= Label(Frame1, text="Hired Location", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_hired.place(x=10, y=350)
        entry_hired = Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_hl, bg="light yellow", fg="black", justify="left").place(x=170, y=355,width=200)

        lbl_status = Label(Frame1, text="Status", font=("times new roman", 17), bg="white", fg="black", anchor="w", padx=10)
        lbl_status.place(x=380, y=350)
        entry_status= Entry(Frame1, font=("times new roman", 15, "bold"),textvariable=self.var_emp_status, bg="light yellow", fg="black", justify="left").place(x=490, y=355)

        #ROW 7
        lbl_add= Label(Frame1, text="Address", font=("times new roman",17), bg="white", fg="black", anchor="w", padx=10)
        lbl_add.place(x=10, y=400)
        self.entry_add = Text(Frame1, font=("times new roman", 15, "bold"), bg="light yellow", fg="black")
        self.entry_add.place(x=170, y=405,width=525,height=150)

        #Frame2
        #Variables - Salary Components for Gross-Up Calculation
        self.var_slr_month=StringVar()
        self.var_slr_year=StringVar()
        self.var_slr_basic=StringVar()  # Basic Pay (inclusion)
        self.var_slr_hra=StringVar()  # HRA (inclusion)
        self.var_slr_ot=StringVar()  # Over Time (inclusion)
        self.var_slr_other_allow=StringVar()  # Other Allowances (inclusion)
        self.var_slr_pf_percent=StringVar()  # PF percentage (exclusion, default 12%)
        self.var_slr_pf_percent.set('12')  # Default PF percentage
        self.var_slr_other_deduct=StringVar()  # Other deductions (exclusion)
        self.var_slr_gross=StringVar()  # Calculated Gross Salary
        self.var_slr_pf_amount=StringVar()  # Calculated PF Amount
        self.var_slr_net=StringVar()  # Net/Take-Home Salary
        
        # Legacy variables (kept for backward compatibility)
        self.var_slr_salary=StringVar()  # Old salary field
        self.var_slr_tdays=StringVar()
        self.var_slr_abs=StringVar()
        self.var_slr_medical=StringVar()
        self.var_slr_pf=StringVar()  # Old PF amount field
        self.var_slr_conv=StringVar()
       
        Frame2=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        Frame2.place(x=770,y=70,width=600,height=325)
        Title2 =Label(Frame2, text="Employee Salary Details", font=("times new roman", 20, "bold"), bg="lightgray", fg="black",anchor="w",padx=10)
        Title2.place(x=0, y=0, relwidth=1)

        lbl_month = Label(Frame2, text="Month", font=("times new roman", 15), bg="white", fg="black",anchor="w",padx=10)
        lbl_month.place(x=10, y=60)
        entry_month = Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_month, bg="light yellow", fg="black", justify="left").place(x=80, y=62,width=100)
        
        lbl_year = Label(Frame2, text="Year", font=("times new roman", 15), bg="white", fg="black",anchor="w",padx=10)
        lbl_year.place(x=200, y=60)
        entry_year = Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_year, bg="light yellow", fg="black", justify="left").place(x=265, y=62,width=100)

        lbl_pf_percent = Label(Frame2, text="PF %", font=("times new roman", 15), bg="white", fg="black",anchor="w",padx=10)
        lbl_pf_percent.place(x=380, y=60)
        entry_pf_percent = Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_pf_percent, bg="light yellow", fg="black", justify="left").place(x=450, y=62,width=100)

        #ROW 1 - Inclusion Components
        lbl_basic = Label(Frame2, text="Basic Pay", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_basic.place(x=10, y=100)
        entry_basic = Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_basic, bg="light yellow", fg="black", justify="left").place(x=140, y=105,width=125)

        lbl_hra = Label(Frame2, text="HRA", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_hra.place(x=310, y=100)
        entry_hra= Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_hra, bg="light yellow", fg="black", justify="left").place(x=425, y=105,width=125)

        #ROW 2 - More Inclusions
        lbl_ot = Label(Frame2, text="Over Time", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_ot.place(x=10, y=155)
        entry_ot = Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_ot, bg="light yellow", fg="black", justify="left").place(x=140, y=155,width=125)

        lbl_other_allow = Label(Frame2, text="Other Allow", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_other_allow.place(x=310, y=155)
        entry_other_allow= Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_other_allow, bg="light yellow", fg="black", justify="left").place(x=425, y=155,width=125)

        #ROW 3 - Outputs and Deductions
        lbl_other_deduct = Label(Frame2, text="Other Deduct", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_other_deduct.place(x=10, y=205)
        entry_other_deduct = Entry(Frame2, font=("times new roman", 15, "bold"),textvariable=self.var_slr_other_deduct, bg="light yellow", fg="black", justify="left").place(x=140, y=205,width=125)

        lbl_gross = Label(Frame2, text="Gross Salary", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_gross.place(x=310, y=205)
        entry_gross= Entry(Frame2, state="readonly", font=("times new roman", 15, "bold"),textvariable=self.var_slr_gross, bg="lightyellow", fg="black", justify="left").place(x=425, y=205,width=125)
        
        #ROW 4 - PF Amount and Net Salary
        lbl_pf_amount = Label(Frame2, text="PF Amount", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_pf_amount.place(x=10, y=235)
        entry_pf_amount = Entry(Frame2, state="readonly", font=("times new roman", 15, "bold"),textvariable=self.var_slr_pf_amount, bg="lightyellow", fg="black", justify="left").place(x=140, y=235,width=125)
        
        lbl_net = Label(Frame2, text="Net Salary", font=("times new roman",15), bg="white", fg="black", anchor="w", padx=10)
        lbl_net.place(x=310, y=235)
        entry_net= Entry(Frame2, state="readonly", font=("times new roman", 15, "bold"),textvariable=self.var_slr_net, bg="lightyellow", fg="black", justify="left").place(x=425, y=235,width=125)

        #ROW 5 Buttons
        btn_calc = Button(Frame2, text="Calculate",command=self.calculate_gross_up, font=("times new roman",15), bg="yellow", fg="black", padx=10)
        btn_calc.place(x=10, y=280,height=27,width=100)
        self.btn_save = Button(Frame2, text="Save",command=self.save, font=("times new roman",15), bg="green", fg="white", padx=10)
        self.btn_save.place(x=120, y=280,height=27,width=100)
        btn_clear = Button(Frame2, text="Clear",command=self.clear, font=("times new roman",15), bg="orange", fg="black", padx=10)
        btn_clear.place(x=230, y=280,height=27,width=100)
        self.btn_update = Button(Frame2, text="Update",state=DISABLED,command=self.update, font=("times new roman",15), bg="cyan", fg="black", padx=10)
        self.btn_update.place(x=340, y=280,height=27,width=100)
        self.btn_delete = Button(Frame2, text="Delete",state=DISABLED,command=self.delete, font=("times new roman",15), bg="red", fg="black", padx=10)
        self.btn_delete.place(x=450, y=280,height=27,width=100)
        
        #Frame3
        Frame3=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        Frame3.place(x=770,y=400,width=600,height=320)

        #Calculator frame
        self.var_txt=StringVar()
        self.var_operator=''
        def btn_click(num):
            self.var_operator=self.var_operator+str(num)
            self.var_txt.set(self.var_operator)

        def result():
            res=str(eval(self.var_operator))
            self.var_txt.set(res)
            self.var_operator=''

        def clear_cal():
            self.var_txt.set('')
            self.var_operator=''

        cal_frame=Frame(Frame3,bg="white",bd=2,relief=RIDGE)
        cal_frame.place(x=2,y=2,width=245,height=305)

        txt_result=Entry(cal_frame,bg="light yellow",textvariable=self.var_txt,font=("times new roman",22,'bold'),justify='right')
        txt_result.place(x=0,y=0,relwidth=1,height=52)

        #=============ROW 1============================
        btn_7=Button(cal_frame,text='7',command=lambda:btn_click(7),font=("times new roman",15,"bold")).place(x=0,y=58,width=60,height=55)
        btn_8=Button(cal_frame,text='8',command=lambda:btn_click(8),font=("times new roman",15,"bold")).place(x=61,y=58,width=60,height=55)
        btn_9=Button(cal_frame,text='9',command=lambda:btn_click(9),font=("times new roman",15,"bold")).place(x=122,y=58,width=60,height=55)
        btn_div=Button(cal_frame,text='/',command=lambda:btn_click('/'),font=("times new roman",15,"bold")).place(x=183,y=58,width=60,height=55)

        #=============ROW 2============================
        btn_4=Button(cal_frame,text='4',command=lambda:btn_click(4),font=("times new roman",15,"bold")).place(x=0,y=118,width=60,height=55)
        btn_5=Button(cal_frame,text='5',command=lambda:btn_click(5),font=("times new roman",15,"bold")).place(x=61,y=118,width=60,height=55)
        btn_6=Button(cal_frame,text='6',command=lambda:btn_click(6),font=("times new roman",15,"bold")).place(x=122,y=118,width=60,height=55)
        btn_mul=Button(cal_frame,text='*',command=lambda:btn_click('*'),font=("times new roman",15,"bold")).place(x=183,y=118,width=60,height=55)

        #=============ROW 3============================
        btn_1=Button(cal_frame,text='1',command=lambda:btn_click(1),font=("times new roman",15,"bold")).place(x=0,y=178,width=60,height=55)
        btn_2=Button(cal_frame,text='2',command=lambda:btn_click(2),font=("times new roman",15,"bold")).place(x=61,y=178,width=60,height=55)
        btn_3=Button(cal_frame,text='3',command=lambda:btn_click(3),font=("times new roman",15,"bold")).place(x=122,y=178,width=60,height=55)
        btn_min=Button(cal_frame,text='-',command=lambda:btn_click('-'),font=("times new roman",15,"bold")).place(x=183,y=178,width=60,height=55)

        #=============ROW 4============================
        btn_0=Button(cal_frame,text='0',command=lambda:btn_click(0),font=("times new roman",15,"bold")).place(x=0,y=238,width=60,height=55)
        btn_dot=Button(cal_frame,text='C',command=clear_cal,font=("times new roman",15,"bold")).place(x=61,y=238,width=60,height=55)
        btn_eql=Button(cal_frame,text='+',command=lambda:btn_click('+'),font=("times new roman",15,"bold")).place(x=122,y=238,width=60,height=55)
        btn_eql=Button(cal_frame,text='=',command=result,font=("times new roman",15,"bold")).place(x=183,y=238,width=60,height=55)

        #=============Salary frame============================
        
        sal_frame=Frame(Frame3,bg="white",bd=2,relief=RIDGE)
        sal_frame.place(x=250,y=2,width=330,height=305)
        Title_sal =Label(sal_frame, text="Salary Reciept", font=("times new roman", 20, "bold"), bg="lightgray", fg="black",anchor="w",padx=10)
        Title_sal.place(x=0, y=0, relwidth=1)

        sal_frame2=Frame(sal_frame,bg='white',bd=2,relief=RIDGE)
        sal_frame2.place(x=0,y=39,relwidth=1,height=230)

        self.sample=f'''\tCompany Name, XYZ\n\tAddress: XYZ, Floor4
    ---------------------------------------------
     Employee Id\t\t:    1
     Salary of\t\t:    Mon-YYYY
     Generated On\t\t:    DD-MM-YYYY  
    ---------------------------------------------
     Total Days\t\t:    DD
     Total Present\t\t:    DD
     Total Absent\t\t:    DD
     Convenience\t\t:    Rs.----
     Medical\t\t:    Rs.----
     PF\t\t:    Rs.----
     Gross Payment\t\t:    Rs.------
     Net Salary\t\t:    Rs.------
    ---------------------------------------------
     This Is A Computer Generated Slip,
     It Does Not Require Any Signature.
    '''

        scroll_y=Scrollbar(sal_frame2,orient=VERTICAL)
        scroll_y.pack(fill=Y,side=RIGHT)

        self.txt_salary_recipt=Text(sal_frame2,font=("times new roman",13),bg="light yellow",yscrollcommand=scroll_y)
        self.txt_salary_recipt.pack(fill=BOTH,expand=True)
        scroll_y.config(command=self.txt_salary_recipt.yview)
        self.txt_salary_recipt.insert(END,self.sample)
        self.btn_print = Button(sal_frame,text="Print",command=self.print_reciept,state=DISABLED, font=("times new roman",15), bg="light blue", fg="black", padx=10)
        self.btn_print.place(x=225, y=271,height=27,width=100)

        self.check_connection()
    #============ all functions start hear============
    def search(self):
        # Database functionality disabled
        messagebox.showinfo("Database Disabled", "Search function is disabled (Database removed - Option A mode)\nDatabase functionality has been removed from this version.", parent=self.root)
    
    def clear(self):
        self.btn_save.config(state=NORMAL)
        self.btn_update.config(state=DISABLED)
        self.btn_delete.config(state=DISABLED)
        self.entry_code.config(state=NORMAL)
        self.btn_print.config(state=DISABLED)
        self.var_emp_code.set('')
        self.var_emp_designation.set('')
        self.var_emp_name.set('')
        self.var_emp_age.set('')
        self.var_emp_gender.set('')
        self.var_emp_email.set('')
        self.var_emp_hl.set('')
        self.var_emp_dob.set('')
        self.var_emp_doj.set('')
        self.var_emp_exp.set('')
        self.var_emp_pid.set('')
        self.var_emp_contact.set('')
        self.var_emp_status.set('')
        self.entry_add.delete('1.0',END)
  
        # Clear gross-up salary fields
        self.var_slr_month.set('')
        self.var_slr_year.set('')
        self.var_slr_basic.set('')
        self.var_slr_hra.set('')
        self.var_slr_ot.set('')
        self.var_slr_other_allow.set('')
        self.var_slr_pf_percent.set('12')  # Reset to default
        self.var_slr_other_deduct.set('')
        self.var_slr_gross.set('')
        self.var_slr_pf_amount.set('')
        self.var_slr_net.set('')
        
        # Clear legacy fields (if needed)
        self.var_slr_salary.set('')
        self.var_slr_tdays.set('')
        self.var_slr_abs.set('')
        self.var_slr_medical.set('')
        self.var_slr_pf.set('')
        self.var_slr_conv.set('')
        self.txt_salary_recipt.delete('1.0',END)
        self.txt_salary_recipt.insert(END,self.sample)

    def view_all(self):
        self.window = Toplevel(self.root) 
        self.window.title("Employee Payroll Management System")
        self.window.geometry("1000x500+120+80") 
        self.window.config(bg="white")
        Title = Label(self.window, text="All Employee Details", font=("times new roman", 30, "bold"), bg="#262626", fg="white",anchor="w",padx=10)
        Title.pack(side=TOP,fill=X)
        self.window.focus_force()

        Scrollx=Scrollbar(self.window,orient=HORIZONTAL)
        Scrolly=Scrollbar(self.window,orient=VERTICAL)
        Scrollx.pack(side=BOTTOM,fill=X)
        Scrolly.pack(side=RIGHT,fill=Y)

        self.dataframe=ttk.Treeview(self.window,columns=('code', 'designation', 'name', 'age', 'gender', 'email', 'hl', 'dob', 'doj', 'exp', 'pid', 'contact', 'status', 'add', 'month', 'year', 'salary', 'tdays', 'abs', 'medical', 'pf', 'conv', 'net', 'reciept'),yscrollcommand=Scrolly.set,xscrollcommand=Scrollx.set)
        self.dataframe.heading('code',text='Employee Code')
        self.dataframe.heading('designation',text='Designation')
        self.dataframe.heading('name',text='Name')
        self.dataframe.heading('age',text='Age')
        self.dataframe.heading('gender',text='Gender')
        self.dataframe.heading('email',text='Email')
        self.dataframe.heading('hl',text='Hired Location')
        self.dataframe.heading('dob',text='Date of Birth')
        self.dataframe.heading('doj',text='Date of Joining')
        self.dataframe.heading('exp',text='Experience')
        self.dataframe.heading('pid',text='Proof ID')
        self.dataframe.heading('contact',text='Contact')
        self.dataframe.heading('status',text='Status')
        self.dataframe.heading('add',text='Address')
        self.dataframe.heading('month',text='Month')
        self.dataframe.heading('year',text='Year')
        self.dataframe.heading('salary',text='Salary')
        self.dataframe.heading('tdays',text='Total Days')
        self.dataframe.heading('abs',text='Absents')
        self.dataframe.heading('medical',text='Medical')
        self.dataframe.heading('pf',text='Provisional Fund')
        self.dataframe.heading('conv',text='Convenience')
        self.dataframe.heading('net',text='Net Salary')
        self.dataframe.heading('reciept',text='Reciept')  
        self.dataframe['show']='headings'   

        self.dataframe.column('code',width=100)
        self.dataframe.column('designation',width=100)
        self.dataframe.column('name',width=100)
        self.dataframe.column('age',width=100)
        self.dataframe.column('gender',width=100)
        self.dataframe.column('email',width=100)
        self.dataframe.column('hl',width=100)
        self.dataframe.column('dob',width=100)
        self.dataframe.column('doj',width=100)
        self.dataframe.column('exp',width=100)
        self.dataframe.column('pid',width=100)
        self.dataframe.column('contact',width=100)
        self.dataframe.column('status',width=100)
        self.dataframe.column('add',width=100)
        self.dataframe.column('month',width=100)
        self.dataframe.column('year',width=100)
        self.dataframe.column('salary',width=100)
        self.dataframe.column('tdays',width=100)
        self.dataframe.column('abs',width=100)
        self.dataframe.column('medical',width=100)
        self.dataframe.column('pf',width=100)
        self.dataframe.column('conv',width=100)
        self.dataframe.column('net',width=100)
        self.dataframe.column('reciept',width=100)
        Scrollx.config(command=self.dataframe.xview)
        Scrolly.config(command=self.dataframe.yview) 
        self.dataframe.pack(fill=BOTH,expand=1)  
        self.show() 
        
        self.window.mainloop()

    def update(self):
        # Database functionality disabled
        messagebox.showinfo("Database Disabled", "Update function is disabled (Database removed - Option A mode)\nDatabase functionality has been removed from this version.", parent=self.root)
    
    def delete(self):
        # Database functionality disabled
        messagebox.showinfo("Database Disabled", "Delete function is disabled (Database removed - Option A mode)\nDatabase functionality has been removed from this version.", parent=self.root)

    def save(self):
        # Database functionality disabled
        messagebox.showinfo("Database Disabled", "Save function is disabled (Database removed - Option A mode)\nDatabase functionality has been removed from this version.", parent=self.root)

    def calculate_gross_up(self):
        """
        GUI wrapper for gross-up salary calculation.
        Calls the standalone calculate_gross_up_salary function.
        """
        # Validate required fields
        if self.var_slr_basic.get()=='' or self.var_slr_pf_percent.get()=='':
            messagebox.showerror('Error','Basic Pay and PF% are required fields')
            return
        
        try:
            # Prepare input data dictionary for the calculation function
            input_data = {
                'Basic Pay': float(self.var_slr_basic.get() or 0),
                'HRA': float(self.var_slr_hra.get() or 0),
                'Over Time': float(self.var_slr_ot.get() or 0),
                'Other Allowances': float(self.var_slr_other_allow.get() or 0),
                'PF Percentage': float(self.var_slr_pf_percent.get() or 12),
                'Other Deductions': float(self.var_slr_other_deduct.get() or 0)
            }
            
            # Call the standalone gross-up calculation function
            result = calculate_gross_up_salary(input_data)
            
            # Update GUI fields with calculated values
            self.var_slr_gross.set(str(round(result['Gross Salary'], 2)))
            self.var_slr_pf_amount.set(str(round(result['PF Amount'], 2)))
            self.var_slr_net.set(str(round(result['Net Salary'], 2)))
            
            # Update the salary receipt
            new_sample=f'''\tCompany Name, XYZ\n\tAddress: XYZ, Floor4
    ---------------------------------------------
     Employee Id\t\t:    {self.var_emp_code.get()}
     Salary of\t\t:    {self.var_slr_month.get()}-{self.var_slr_year.get()}
     Generated On\t\t:    {str(time.strftime("%d-%m-%Y"))}  
    ---------------------------------------------
     SALARY BREAKDOWN (Gross-Up Calculation)
    ---------------------------------------------
     Inclusion Components:
     Basic Pay\t\t:    Rs.{result['Basic Pay']:.2f}
     HRA\t\t:    Rs.{result['HRA']:.2f}
     Over Time\t\t:    Rs.{result['Over Time']:.2f}
     Other Allowances\t\t:    Rs.{result['Other Allowances']:.2f}
    ---------------------------------------------
     Gross Salary\t\t:    Rs.{result['Gross Salary']:.2f}
    ---------------------------------------------
     Deductions:
     PF ({result['PF Percentage']:.1f}%)\t\t:    Rs.{result['PF Amount']:.2f}
     Other Deductions\t\t:    Rs.{result['Other Deductions']:.2f}
     Total Deductions\t\t:    Rs.{result['Total Deductions']:.2f}
    ---------------------------------------------
     Net Salary (Take-Home)\t:    Rs.{result['Net Salary']:.2f}
    ---------------------------------------------
     This Is A Computer Generated Slip,
     It Does Not Require Any Signature.
    '''
            self.txt_salary_recipt.delete('1.0',END)
            self.txt_salary_recipt.insert(END,new_sample)
            
        except ValueError as e:
            messagebox.showerror('Error', f'Invalid input: Please enter valid numbers\n{str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'Calculation error: {str(e)}')
    
    def check_connection(self):
        # Database functionality disabled - no connection check needed
        pass

    def show(self):
        # Database functionality disabled - clear dataframe and show message
        self.dataframe.delete(*self.dataframe.get_children())
        messagebox.showinfo("Database Disabled", "View All Records function is disabled (Database removed - Option A mode)\nDatabase functionality has been removed from this version.", parent=self.window)
    
    def print_reciept(self):
        temp_file=tempfile.mktemp(".txt")
        open(temp_file,'w').write(self.txt_salary_recipt.get('1.0',END))
        os.startfile(temp_file,'print')       

root = Tk()
obj = EmployeeSystem(root)
root.mainloop()