@echo off
python -m venv .venv

call .venv\Scripts\activate

pip install -r requirements.txt

echo.
echo Environment ready.
echo Activate with: .venv\Scripts\activate
pause

streamlit run app.py