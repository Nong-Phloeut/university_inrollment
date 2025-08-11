# STEP 1: Clone the project
git clone https://github.com/yourusername/pharmacy-pos.git
cd pharmacy-pos

# STEP 2: Create and activate virtual environment (Python 3.x)
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate

# STEP 3: Install dependencies
pip install -r requirements.txt

# STEP 4: Setup MySQL database
# Open MySQL and run:
# Replace 'yourpassword' with your actual password
mysql -u root -p

# Inside MySQL shell:
CREATE DATABASE pharmacy_pos;
EXIT;

# STEP 5: Update database config
# Edit app/db.py and set your credentials
# Example:
# engine = create_engine("mysql+mysqlconnector://root:yourpassword@localhost/pharmacy_pos")

# STEP 6: Initialize database tables
python main.py  # First run will auto-create tables

# STEP 7: Launch the application
python main.py
