FILENAME=/app/.heroku/python/lib/python3.8/site-packages/easy_pdf/rendering.py

sed -i '15d' $FILENAME
sed -i '15 a from io import BytesIO' $FILENAME

web: gunicorn online-testing-app.wsgi --log-file -
