rm -rf .fllenv_upgrade
python3 -m venv .fllenv_upgrade
source .fllenv_upgrade/bin/activate
pip install -r requirements.txt
pip freeze >requirements_frozen.txt
rm -rf .fllenv_upgrade
