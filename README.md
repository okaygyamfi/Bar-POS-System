# Bar Inventory & POS System (Akropong Branch)

A robust, terminal-based Point of Sale system built with Python and MySQL. Designed for precision tracking of bottle inventory and individual spirit shots (ML-based tracking).

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