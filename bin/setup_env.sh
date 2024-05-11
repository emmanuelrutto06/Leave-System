python3 -m venv env
activate(){
    . env/bin/activate
    echo "Install requirements packages to the virtual environment"
    pip install -r requirements.txt
}
activate