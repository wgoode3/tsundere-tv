if [ -d venv ]; then
    source venv/bin/activate
fi

if [ ! -d venv ]; then
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

cd server
gunicorn --bind 0.0.0.0:8000 config.wsgi:application