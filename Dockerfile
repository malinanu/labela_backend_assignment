FROM python:3.11
LABEL author='Label A'

WORKDIR /app

# Environment - Install Postgres dependencies
RUN apt-get update
RUN apt-get install -y bash vim nano postgresql postgresql-contrib 
RUN pip install --upgrade pip

# Major pinned python dependencies
RUN pip install --no-cache-dir flake8==3.8.4 uWSGI psycopg2-binary # Added psycopg2-binary
RUN apt-get update && apt-get install -y dos2unix

# Regular Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy our codebase into the container
COPY . .

RUN dos2unix manage.py 

# Ops Parameters
ENV WORKERS=2
ENV PORT=80
ENV PYTHONUNBUFFERED=1


ENV POSTGRES_USER=myuser 
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydb

# Initialize an empty Postgres data volume 
VOLUME /var/lib/postgresql/data 

EXPOSE ${PORT} 5432 

# Start Postgres and run Django app at container startup  
CMD ["sh", "-c", "service postgresql start && uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --module autocompany.wsgi:application"] 
