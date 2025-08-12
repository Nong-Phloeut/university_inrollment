# STEP 1: Create and activate virtual environment (Python 3.x)
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate

# STEP 2: Install dependencies
pip install -r requirements.txt

# STEP 3: Setup MySQL database
# Open MySQL and run:
# Replace 'yourpassword' with your actual password
mysql -u root -p

# Inside MySQL shell:
CREATE DATABASE school_mgmt;
EXIT;

# STEP 4: Update env 
add your username and password 

# STEP 6: Initialize database tables
python run.py  # First run will auto-create tables

# STEP 7: Seeder data
python run.py  # First run will auto-create tables

# STEP 8: Launch the application
uvicorn main:app --reload

