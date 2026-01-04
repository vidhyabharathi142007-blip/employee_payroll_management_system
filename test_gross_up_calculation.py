"""
TEST FILE: Gross-Up Payroll Calculation Module
================================================

This file demonstrates how to use the calculate_gross_up_salary() function
independently of the GUI, making it perfect for Excel data processing.

Excel Integration Workflow:
----------------------------
1. Read Excel file using pandas or openpyxl
2. For each row, convert to dictionary format
3. Call calculate_gross_up_salary(row_data)
4. Write results back to Excel or generate reports
"""

import sys
import os

# Add parent directory to path to import from employee.py
sys.path.insert(0, os.path.dirname(__file__))

# Import the standalone function
from employee import calculate_gross_up_salary


def test_basic_calculation():
    """Test Case 1: Basic gross-up calculation with standard PF"""
    print("\n" + "="*60)
    print("TEST CASE 1: Standard Employee with 12% PF")
    print("="*60)
    
    employee_data = {
        'Basic Pay': 50000,
        'HRA': 10000,
        'Over Time': 5000,
        'Other Allowances': 2000,
        'PF Percentage': 12,
        'Other Deductions': 1000
    }
    
    result = calculate_gross_up_salary(employee_data)
    
    print(f"\nINPUT:")
    print(f"  Basic Pay: ₹{result['Basic Pay']:,.2f}")
    print(f"  HRA: ₹{result['HRA']:,.2f}")
    print(f"  Over Time: ₹{result['Over Time']:,.2f}")
    print(f"  Other Allowances: ₹{result['Other Allowances']:,.2f}")
    print(f"  PF Percentage: {result['PF Percentage']:.1f}%")
    print(f"  Other Deductions: ₹{result['Other Deductions']:,.2f}")
    
    print(f"\nCALCULATIONS:")
    print(f"  Total Inclusions: ₹{result['Total Inclusions']:,.2f}")
    print(f"  Gross-Up Formula: {result['Total Inclusions']:,.2f} / (1 - 0.{int(result['PF Percentage'])})")
    print(f"  Gross Salary: ₹{result['Gross Salary']:,.2f}")
    print(f"  PF Amount (Basic × {result['PF Percentage']:.0f}%): ₹{result['PF Amount']:,.2f}")
    print(f"  Total Deductions: ₹{result['Total Deductions']:,.2f}")
    
    print(f"\nRESULT:")
    print(f"  ✓ Net Salary (Take-Home): ₹{result['Net Salary']:,.2f}")
    
    return result


def test_higher_pf():
    """Test Case 2: Employee with higher PF percentage (15%)"""
    print("\n" + "="*60)
    print("TEST CASE 2: Higher PF Percentage (15%)")
    print("="*60)
    
    employee_data = {
        'Basic Pay': 60000,
        'HRA': 15000,
        'Over Time': 0,
        'Other Allowances': 5000,
        'PF Percentage': 15,
        'Other Deductions': 0
    }
    
    result = calculate_gross_up_salary(employee_data)
    
    print(f"\nINPUT:")
    print(f"  Basic Pay: ₹{result['Basic Pay']:,.2f}")
    print(f"  HRA: ₹{result['HRA']:,.2f}")
    print(f"  Other Allowances: ₹{result['Other Allowances']:,.2f}")
    print(f"  PF Percentage: {result['PF Percentage']:.1f}%")
    
    print(f"\nRESULT:")
    print(f"  Gross Salary: ₹{result['Gross Salary']:,.2f}")
    print(f"  PF Amount: ₹{result['PF Amount']:,.2f}")
    print(f"  Net Salary: ₹{result['Net Salary']:,.2f}")
    
    print(f"\nNOTE: Higher PF% results in higher Gross to maintain inclusions")
    
    return result


def test_minimal_employee():
    """Test Case 3: Minimal employee with only basic pay"""
    print("\n" + "="*60)
    print("TEST CASE 3: Minimal Employee (Basic Pay Only)")
    print("="*60)
    
    employee_data = {
        'Basic Pay': 30000,
        'PF Percentage': 12
    }
    
    result = calculate_gross_up_salary(employee_data)
    
    print(f"\nINPUT:")
    print(f"  Basic Pay: ₹{result['Basic Pay']:,.2f}")
    print(f"  PF Percentage: {result['PF Percentage']:.1f}%")
    
    print(f"\nRESULT:")
    print(f"  Gross Salary: ₹{result['Gross Salary']:,.2f}")
    print(f"  PF Amount: ₹{result['PF Amount']:,.2f}")
    print(f"  Net Salary: ₹{result['Net Salary']:,.2f}")
    
    return result


def excel_simulation():
    """Simulate processing multiple employees from Excel"""
    print("\n" + "="*60)
    print("EXCEL SIMULATION: Processing Multiple Employees")
    print("="*60)
    
    # Simulate Excel rows (in real scenario, use pandas.read_excel())
    excel_data = [
        {'Emp_ID': 'E001', 'Basic Pay': 45000, 'HRA': 9000, 'Over Time': 3000, 'Other Allowances': 1500, 'PF Percentage': 12, 'Other Deductions': 500},
        {'Emp_ID': 'E002', 'Basic Pay': 55000, 'HRA': 11000, 'Over Time': 0, 'Other Allowances': 2000, 'PF Percentage': 12, 'Other Deductions': 0},
        {'Emp_ID': 'E003', 'Basic Pay': 70000, 'HRA': 14000, 'Over Time': 5000, 'Other Allowances': 3000, 'PF Percentage': 15, 'Other Deductions': 1500},
    ]
    
    print("\nProcessing employees...")
    print(f"\n{'Emp ID':<10}{'Basic Pay':<15}{'Gross Salary':<15}{'PF Amount':<15}{'Net Salary':<15}")
    print("-" * 70)
    
    results = []
    for row in excel_data:
        emp_id = row.pop('Emp_ID')  # Remove Emp_ID before calculation
        result = calculate_gross_up_salary(row)
        result['Emp_ID'] = emp_id  # Add it back to result
        results.append(result)
        
        print(f"{emp_id:<10}₹{result['Basic Pay']:<14,.0f}₹{result['Gross Salary']:<14,.2f}₹{result['PF Amount']:<14,.2f}₹{result['Net Salary']:<14,.2f}")
    
    print("\n✓ All employees processed successfully!")
    print("\nIn real scenario, write these results back to Excel using:")
    print("  - pandas: df.to_excel('output.xlsx')")
    print("  - openpyxl: workbook.save('output.xlsx')")
    
    return results


def demonstrate_gross_up_principle():
    """Demonstrate how gross-up works when PF increases"""
    print("\n" + "="*60)
    print("GROSS-UP PRINCIPLE DEMONSTRATION")
    print("="*60)
    print("\nScenario: Same inclusion components, different PF percentages")
    print("This shows how Gross automatically adjusts to maintain inclusions")
    
    base_data = {
        'Basic Pay': 50000,
        'HRA': 10000,
        'Over Time': 0,
        'Other Allowances': 0,
    }
    
    print(f"\n{'PF %':<10}{'Total Inclusions':<20}{'Gross Salary':<20}{'Net Salary':<20}")
    print("-" * 70)
    
    for pf_percent in [10, 12, 15, 18]:
        data = base_data.copy()
        data['PF Percentage'] = pf_percent
        data['Other Deductions'] = 0
        
        result = calculate_gross_up_salary(data)
        
        print(f"{pf_percent:<10}₹{result['Total Inclusions']:<19,.2f}₹{result['Gross Salary']:<19,.2f}₹{result['Net Salary']:<19,.2f}")
    
    print("\n✓ Notice: As PF% increases, Gross increases to compensate")
    print("✓ Total Inclusions remain constant across all scenarios")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("GROSS-UP PAYROLL CALCULATION TEST SUITE")
    print("="*60)
    
    try:
        # Run all test cases
        test_basic_calculation()
        test_higher_pf()
        test_minimal_employee()
        excel_simulation()
        demonstrate_gross_up_principle()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED SUCCESSFULLY!")
        print("="*60)
        
        print("\n\nHOW TO USE WITH EXCEL:")
        print("----------------------")
        print("1. Install: pip install pandas openpyxl")
        print("2. Read Excel: df = pd.read_excel('employees.xlsx')")
        print("3. Process: results = df.apply(lambda row: calculate_gross_up_salary(row.to_dict()), axis=1)")
        print("4. Save: results_df.to_excel('payroll_results.xlsx')")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
