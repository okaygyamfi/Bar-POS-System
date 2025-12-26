# Bar Inventory & POS System (Beyond Bite -- Akropong Branch)

Bar Inventory & POS System (Professional Management Tool)

Project Overview
A high-performance, terminal-based Point of Sale (POS) and Inventory Management System designed for the hospitality industry. This project solves a common retail problem: Dual-Track Inventory Management. It allows a business to sell products by the unit (e.g., bottled beer) and by volume (e.g., spirit shots measured in milliliters) simultaneously, ensuring 100% stock accuracy.

Technical Skills Demonstrated
Backend Development (Python): Developed a modular application logic using Python, handling complex transactions and inventory calculations.

Database Architecture (MySQL): Designed a relational database schema to manage products, sales history, and real-time inventory levels with transaction integrity (Rollbacks/Commits).

Security & Credential Management: Implemented an abstraction layer using configparser to store sensitive database credentials in external .ini files, preventing hardcoded passwords in source control.

File I/O & System Automation: Integrated a database backup engine that automatically generates timestamped .sql dumps upon system exit for data disaster recovery.

Software Distribution: Configured build scripts with PyInstaller to compile the Python environment into a standalone Windows Executable (.exe) for end-user deployment.

Core Functionality
Intelligent Stock Deduction: Automatically calculates "Shots-to-Bottle" conversions (e.g., deducting 30ml from a 750ml bottle) or unit-based deductions based on product category.

Audit Trail: Logs every sale with unique IDs, payment methods (Cash/MoMo), and detailed itemized receipts.

Reporting: Real-time generation of Daily Sales Summaries and Monthly Performance Reports.

Stock Alerts: Visual "LOW STOCK" triggers to notify staff when inventory falls below critical levels.

## Features
- **Dual Inventory Tracking:** Supports both unit-based (Beers/Softs) and volume-based (Shots/ML) inventory.
- **Secure Configuration:** Uses `config.ini` to keep database credentials out of the source code.
- **Auto-Backups:** Generates a `.sql` dump of the database every time the system is closed.
- **Management Tools:** Includes modules for restocking, price updates, and monthly performance reports.

## Installation & Setup
1. **Clone the repo:**
   `git clone https://github.com/okaygyamfi/Bar-POS-System.git`
2. **Install dependencies:**
   `pip install -r requirements.txt`
3. **Database Setup:**
   Import `database_setup.sql` into your local MySQL server.
4. **Configuration:**
   Rename `config.example.ini` to `config.ini` and enter your MySQL credentials.
5. **Run the app:**
   `python app.py`

## Building the Executable
To create a standalone `.exe`:
`pyinstaller --onefile --console app.py`
