@echo off
echo --- UPDATING YOUR STORE ---

:: 1. Run your Python logic (Make sure the python file is named 'final_shop.py' or similar)
python restore_products.py

:: 2. Build the site
hugo

echo.
echo --- DONE! SITE IS READY IN 'public' FOLDER ---
pause