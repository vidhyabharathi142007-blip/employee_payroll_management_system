#!/usr/bin/env python3
"""Quick test of gross-up calculation"""

from employee import calculate_gross_up_salary

# Test case
test_data = {
    'Basic Pay': 50000,
    'HRA': 10000,
    'Over Time': 5000,
    'Other Allowances': 2000,
    'PF Percentage': 12,
    'Other Deductions': 1000
}

result = calculate_gross_up_salary(test_data)

print("GROSS-UP CALCULATION TEST")
print("="*50)
print(f"Basic Pay: Rs.{result['Basic Pay']:,.2f}")
print(f"HRA: Rs.{result['HRA']:,.2f}")
print(f"Over Time: Rs.{result['Over Time']:,.2f}")
print(f"Other Allowances: Rs.{result['Other Allowances']:,.2f}")
print(f"Total Inclusions: Rs.{result['Total Inclusions']:,.2f}")
print(f"\nPF Percentage: {result['PF Percentage']:.1f}%")
print(f"PF Amount: Rs.{result['PF Amount']:,.2f}")
print(f"Other Deductions: Rs.{result['Other Deductions']:,.2f}")
print(f"Total Deductions: Rs.{result['Total Deductions']:,.2f}")
print(f"\nGROSS SALARY: Rs.{result['Gross Salary']:,.2f}")
print(f"NET SALARY: Rs.{result['Net Salary']:,.2f}")
print(f"\nSuccessful!")
