FROM python:3.9-slim

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

RUN mkdir -p /for_download

VOLUME [ "/for_download" ]

EXPOSE 3000

ENV PYTHONPATH=.

RUN python3 app/init_data.py
CMD ["uvicorn", "app.main:app", "--reload", "--port=3000", "--host=0.0.0.0" ]
