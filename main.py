from mcp.server.fastmcp import FastMCP
from typing import List, Optional
from datetime import datetime
import uuid

mcp = FastMCP("HRManagementSystem")

##########################################################
# Employee Database
##########################################################

employees = {
    "E001": {
        "name": "John Doe",
        "department": "Engineering",
        "designation": "Software Engineer",
        "email": "john@example.com",
        "phone": "9999999999",
        "joining_date": "2023-01-15",
        "status": "Active"
    },
    "E002": {
        "name": "Alice Smith",
        "department": "HR",
        "designation": "HR Manager",
        "email": "alice@example.com",
        "phone": "8888888888",
        "joining_date": "2022-05-20",
        "status": "Active"
    }
}

##########################################################
# Leave Database
##########################################################

employee_leaves = {
    "E001": {
        "balance": 18,
        "history": [],
        "pending": []
    },
    "E002": {
        "balance": 20,
        "history": [],
        "pending": []
    }
}

##########################################################
# Salary Database
##########################################################

employee_salary = {
    "E001": {
        "basic": 60000,
        "bonus": 5000,
        "deduction": 0
    },
    "E002": {
        "basic": 80000,
        "bonus": 10000,
        "deduction": 2000
    }
}

##########################################################
# Employee Management
##########################################################


@mcp.tool()
def add_employee(
    employee_id: str,
    name: str,
    department: str,
    designation: str,
    email: str,
    phone: str,
    joining_date: str,
    salary: float
):
    """Add a new employee"""

    if employee_id in employees:
        return "Employee already exists."

    employees[employee_id] = {
        "name": name,
        "department": department,
        "designation": designation,
        "email": email,
        "phone": phone,
        "joining_date": joining_date,
        "status": "Active"
    }

    employee_leaves[employee_id] = {
        "balance": 20,
        "history": [],
        "pending": []
    }

    employee_salary[employee_id] = {
        "basic": salary,
        "bonus": 0,
        "deduction": 0
    }

    return f"{name} added successfully."


@mcp.tool()
def update_employee(
    employee_id: str,
    field: str,
    value: str
):
    """Update any employee detail"""

    if employee_id not in employees:
        return "Employee not found."

    if field not in employees[employee_id]:
        return "Invalid field."

    employees[employee_id][field] = value

    return "Employee updated successfully."


@mcp.tool()
def delete_employee(employee_id: str):
    """Delete employee from HR database"""

    if employee_id not in employees:
        return "Employee not found."

    employees.pop(employee_id, None)
    employee_leaves.pop(employee_id, None)
    employee_salary.pop(employee_id, None)

    return "Employee deleted."


@mcp.tool()
def get_employee(employee_id: str):
    """Get employee information"""

    if employee_id not in employees:
        return "Employee not found."

    return employees[employee_id]


@mcp.tool()
def search_employee(name: str):
    """Search employee by name"""

    result = []

    for eid, info in employees.items():
        if name.lower() in info["name"].lower():
            result.append({
                "employee_id": eid,
                **info
            })

    return result


@mcp.tool()
def list_all_employees():
    """List every employee"""

    return employees


##########################################################
# Leave Management
##########################################################

@mcp.tool()
def get_leave_balance(employee_id: str):

    if employee_id not in employee_leaves:
        return "Employee not found."

    return employee_leaves[employee_id]["balance"]


@mcp.tool()
def apply_leave(
    employee_id: str,
    leave_dates: List[str]
):
    """Apply leave"""

    if employee_id not in employee_leaves:
        return "Employee not found."

    request = {
        "request_id": str(uuid.uuid4())[:8],
        "dates": leave_dates,
        "status": "Pending"
    }

    employee_leaves[employee_id]["pending"].append(request)

    return request


@mcp.tool()
def approve_leave(
    employee_id: str,
    request_id: str
):
    """Approve leave request"""

    if employee_id not in employee_leaves:
        return "Employee not found."

    pending = employee_leaves[employee_id]["pending"]

    for req in pending:

        if req["request_id"] == request_id:

            days = len(req["dates"])

            if employee_leaves[employee_id]["balance"] < days:
                return "Insufficient balance."

            employee_leaves[employee_id]["balance"] -= days

            req["status"] = "Approved"

            employee_leaves[employee_id]["history"].append(req)

            pending.remove(req)

            return "Leave Approved."

    return "Request not found."


@mcp.tool()
def reject_leave(
    employee_id: str,
    request_id: str
):
    """Reject leave"""

    pending = employee_leaves[employee_id]["pending"]

    for req in pending:

        if req["request_id"] == request_id:

            req["status"] = "Rejected"

            pending.remove(req)

            return "Leave Rejected."

    return "Request not found."


@mcp.tool()
def cancel_leave(employee_id: str, request_id: str):
    """Cancel pending leave"""

    pending = employee_leaves[employee_id]["pending"]

    for req in pending:

        if req["request_id"] == request_id:

            pending.remove(req)

            return "Leave cancelled."

    return "Not found."


@mcp.tool()
def add_leave_balance(employee_id: str, days: int):

    employee_leaves[employee_id]["balance"] += days

    return employee_leaves[employee_id]


@mcp.tool()
def deduct_leave_balance(employee_id: str, days: int):

    employee_leaves[employee_id]["balance"] -= days

    return employee_leaves[employee_id]


@mcp.tool()
def leave_history(employee_id: str):

    return employee_leaves[employee_id]


##########################################################
# Salary Management
##########################################################

@mcp.tool()
def get_salary(employee_id: str):
    """Get employee salary"""

    if employee_id not in employee_salary:
        return "Employee not found."

    salary = employee_salary[employee_id]

    total = (
        salary["basic"]
        + salary["bonus"]
        - salary["deduction"]
    )

    return {
        **salary,
        "net_salary": total
    }


@mcp.tool()
def give_bonus(
    employee_id: str,
    amount: float
):
    """Add bonus"""

    employee_salary[employee_id]["bonus"] += amount

    return employee_salary[employee_id]


@mcp.tool()
def deduct_salary(
    employee_id: str,
    amount: float
):
    """Salary deduction"""

    employee_salary[employee_id]["deduction"] += amount

    return employee_salary[employee_id]


@mcp.tool()
def increment_salary(
    employee_id: str,
    amount: float
):
    """Salary increment"""

    employee_salary[employee_id]["basic"] += amount

    return employee_salary[employee_id]


@mcp.tool()
def annual_salary(employee_id: str):

    salary = get_salary(employee_id)

    if isinstance(salary, str):
        return salary

    return salary["net_salary"] * 12


@mcp.tool()
def generate_payslip(employee_id: str):
    """Generate employee payslip"""

    if employee_id not in employees:
        return "Employee not found."

    emp = employees[employee_id]

    salary = get_salary(employee_id)

    return {
        "employee": emp,
        "salary": salary,
        "generated_on": str(datetime.now())
    }


##########################################################
# Combined HR Tool
##########################################################

@mcp.tool()
def employee_summary(employee_id: str):
    """Complete employee profile"""

    if employee_id not in employees:
        return "Employee not found."

    return {
        "Employee Details": employees[employee_id],
        "Leave Details": employee_leaves[employee_id],
        "Salary Details": get_salary(employee_id)
    }


##########################################################
# Resources
##########################################################

@mcp.resource("employee://{employee_id}")
def employee_resource(employee_id: str):
    return employee_summary(employee_id)


@mcp.resource("greeting://{name}")
def greeting(name: str):
    return f"Welcome {name} to the HR Management System."


if __name__ == "__main__":
    mcp.run()
