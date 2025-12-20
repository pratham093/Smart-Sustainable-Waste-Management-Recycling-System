# Smart Waste Management System  
**IE 6700 – Data Management for Analytics (Northeastern University)**

## 📘 Course Context
This project was developed as part of **IE 6700: Data Management for Analytics** at **Northeastern University**.  
The objective of the course project was to design a **relational database–driven system** and build a **Python application** that executes analytical SQL queries and visualizes results for real-world decision-making.

---

## 📌 Project Overview
The **Smart Waste Management System** is a **data-driven municipal analytics application** built on top of a **MySQL relational database**.

It models and analyzes core waste management operations such as:
- Waste collection across city zones and routes
- Household-level recycling behavior
- Vehicle utilization and capacity usage
- Staff participation and performance
- Violations, fines, and payments
- Route efficiency and collection compliance

The project demonstrates how **structured data + SQL analytics + Python visualization** can support **smart city decision-making**.

---

## 🏗️ System Architecture

### 1️⃣ Relational Database (MySQL)
The database is designed in **Third Normal Form (3NF)** to ensure:
- Data integrity
- Minimal redundancy
- Clear entity relationships

Key entities include:
- Zone, Route, Household
- WasteBin, WasteType
- Vehicle, Staff
- CollectionSchedule, CollectionLog
- Violation, Payment, RecyclingCenter

The schema models real municipal waste operations and supports complex analytical queries.

---

### 2️⃣ Analytical SQL Queries
The system includes **12 analytical SQL queries** that generate actionable insights such as:
- Total waste collected by zone
- Recycling rate by household
- Vehicle capacity utilization
- Staff performance metrics
- Outstanding violations and fines
- Route efficiency (scheduled vs actual collections)
- Recycling center capacity usage
- Monthly violation trends

These queries go beyond basic CRUD operations and reflect real operational analytics.

---

### 3️⃣ Python Application (GUI + Analytics)
A **Python desktop application** was developed to interact with the MySQL database.

**Technologies used:**
- `Tkinter` – Graphical User Interface
- `mysql-connector-python` – Database connectivity
- `pandas` – Data processing
- `matplotlib` – Data visualization

**Application capabilities:**
- Executes SQL queries dynamically
- Displays query results in tabular format
- Generates visual analytics including:
  - Bar charts
  - Pie charts
  - Grouped and stacked bar charts
  - Line charts

This layer makes database insights accessible to **non-technical users**.

---

## 📂 Repository Structure

```text
.
├── SCHEMA.sql        # Database schema (DDL)
├── VALUES.sql        # Sample data insertion (DML)
├── index.py          # Python GUI application with SQL queries & visualizations
├── requirement.txt   # Python dependencies
└── README.md
