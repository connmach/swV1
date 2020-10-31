FROM python:3.6 
COPY . /platform
WORKDIR /platform
RUN pip install -r requirements.txt
CMD ["python3","flask_app.py"]
