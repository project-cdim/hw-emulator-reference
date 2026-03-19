FROM python:3-slim

# For healthcheck
RUN apt-get update && apt-get install curl -y

# Install python requirements
COPY Redfish_Simulator/requirements.txt /tmp/
RUN echo "gunicorn[gevent]" >> /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy server files
COPY Redfish_Simulator /usr/src/app/.
COPY simulatorDeviceList.json /usr/src/.

# Create main.py
RUN printf "import emulator\nfrom g import app\n" > /usr/src/app/main.py

# Env settings
EXPOSE 5000
HEALTHCHECK CMD curl --fail http://127.0.0.1:5000/redfish/v1/ || exit 1
WORKDIR /usr/src/app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gevent", "--workers", "1", "main:app"]
