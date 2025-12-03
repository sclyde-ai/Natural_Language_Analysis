python3 -3.7 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip list
python3 -m ipykernel install --user --name=NaturalLanguageAnlysis
deactivate
