import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Add a custom style
st.markdown(
    """
    <style>
    body {
        background-color: #f2f2f2;
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1, h2, h3 {
        color: #2e7d32;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# Function to calculate totals
def calculate_totals(expenses, period):
    today = datetime.today()
    end_date = today
    if period == "Weekly":
        end_date += timedelta(days=7)
    elif period == "Monthly":
        end_date += timedelta(days=30)
    elif period == "Yearly":
        end_date += timedelta(days=365)

    total = 0
    for expense in expenses:
        due_date = datetime.strptime(expense["due_date"], "%Y-%m-%d")
        while due_date <= end_date:  # Account for recurring payments
            if due_date >= today:
                total += expense["amount"]
            if expense["frequency"] == "Weekly":
                due_date += timedelta(days=7)
            elif expense["frequency"] == "Monthly":
                due_date += timedelta(days=30)
            elif expense["frequency"] == "Yearly":
                due_date += timedelta(days=365)
    return total

# Page Title
st.title("💵 Personal Finance Tracker")
st.markdown("Keep your expenses organized and never miss a payment again!")

# Input Section
st.header("Add a New Expense")
expense_name = st.text_input("🛒 Expense Name")
amount = st.number_input("💲 Amount ($)", min_value=0.0, format="%.2f")
due_date = st.date_input("📅 Due Date", min_value=datetime.today())
frequency = st.selectbox("🔁 Frequency of Payment", ["Weekly", "Monthly", "Yearly"])

if st.button("Add Expense"):
    if expense_name and amount > 0 and due_date:
        st.session_state["expenses"].append(
            {
                "name": expense_name,
                "amount": amount,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "frequency": frequency,
            }
        )
        st.success(f"Expense '{expense_name}' added!")
    else:
        st.error("Please fill out all fields correctly.")

# Display Expenses
st.header("Your Expenses")
if st.session_state["expenses"]:
    df = pd.DataFrame(st.session_state["expenses"])
    df["Due Date"] = pd.to_datetime(df["due_date"]).dt.strftime("%b %d, %Y")
    df.rename(columns={"frequency": "Frequency"}, inplace=True)
    df.drop(columns=["due_date"], inplace=True)
    st.table(df)
else:
    st.info("No expenses added yet.")

# Total Calculations
st.header("📊 Calculate Total Expenses")
period = st.selectbox("Select Period", ["Weekly", "Monthly", "Yearly"])
if st.button("Calculate Total"):
    total = calculate_totals(st.session_state["expenses"], period)
    st.success(f"💸 Total expenses for the next {period.lower()}: **${total:.2f}**")

# Reminders Section
st.header("⏰ Upcoming Payments")
today = datetime.today()
upcoming = [
    expense
    for expense in st.session_state["expenses"]
    if datetime.strptime(expense["due_date"], "%Y-%m-%d") >= today
]
if upcoming:
    for expense in upcoming:
        st.write(
            f"💡 **{expense['name']}** - Due on {expense['due_date']} - Amount: **${expense['amount']:.2f}** - Frequency: {expense['frequency']}"
        )
else:
    st.info("No upcoming payments!")

# Footer
st.markdown(
    """
    ---
    <div style="text-align: center;">
        <p>Built with ❤️ and Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True,
)
