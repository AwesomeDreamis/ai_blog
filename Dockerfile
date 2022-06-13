FROM python:3.8.10

RUN mkdir /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip
#RUN pip install --upgrade pip wheel
#RUN pip install tzdata
RUN #pip install backports.zoneinfo
RUN python -m pip install -r /app/requirements.txt

COPY . ./app/

WORKDIR /app/news/

#ENTRYPOINT ["python", "manage.py", "runserver", "localhost:8000"]
