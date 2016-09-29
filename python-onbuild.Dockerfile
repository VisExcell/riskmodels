FROM python:2-onbuild
EXPOSE 5000
#CMD [ "python", "./calculators.py" ]
CMD ["gunicorn", "--workers=4", "-b 0.0.0.0:5000","wsgi:app"]
