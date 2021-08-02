sed 's/from django.utils.six import BytesIO/from io import BytesIO/' /app/.heroku/python/lib/python3.8/site-packages/easy_pdf/rendering.py
web: gunicorn online-testing-app.wsgi --log-file -
