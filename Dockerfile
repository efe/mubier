FROM python:3.7.1-stretch as base

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

WORKDIR /mubier

## Development
FROM base as application_development

# Non Development
FROM base as application
COPY . .
