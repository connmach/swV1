FROM python:3.6 
COPY . /platform
WORKDIR /platform
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["platformApp.py"]
