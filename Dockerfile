FROM python:3.12-slim

# create a non-root to run the app
RUN groupadd -r -g 1001 appgroup && useradd -r -m -l -u 1001 -g appgroup appuser

# create a directory to store the source code
WORKDIR /app

# copy over the requirements.txt file
COPY requirements.txt .

# install the required packages with pip. No cache to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# copy over the source code
COPY --chown=appuser:appgroup app.py .

# switch to the non-root user
USER appuser

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]


