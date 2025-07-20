# Common Commands for the Cards Project

## 1. Activate the Virtual Environment
```bash
source venv/bin/activate
```

## 2. Generate All Cards from a CSV File
Replace `sample_cards.csv` with your desired CSV file if needed.
```bash
python generate_cards_bulk.py sample_cards.csv
```

## 3. Generate a Single Test Card
This uses the default hardcoded card in the script.
```bash
python generate_cards_bulk.py
```

## 4. Install Project Dependencies
If you add new dependencies or set up on a new machine:
```bash
pip install -r requirements.txt
```

## 5. Add a New Dependency
For example, to add `jinja2`:
```bash
pip install jinja2
pip freeze > requirements.txt
```

## 6. Deactivate the Virtual Environment
```bash
deactivate
```

---

**Tip:** Always activate your virtual environment before running Python scripts for this project. 