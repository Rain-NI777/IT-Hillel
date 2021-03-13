#!bin/bash
chmod +x homework.sh

python -m venv projectx
source ./projectx/bin/activate
pip install flask
pip freeze > requirements.txt

echo "Hello! My name is Rain"
exit 0
echo "This is my first project on Bash"
exit 0
