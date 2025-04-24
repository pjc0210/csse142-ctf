FROM ubuntu:24.04

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip python3-dev python3-venv

WORKDIR /ctf

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt /ctf
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and assets
COPY server.py /ctf
COPY init_db.py /ctf
COPY users.db /ctf

# Copy static files
RUN mkdir -p /ctf/static
COPY static/main.js /ctf/static

# Permissions and user config
RUN chmod 555 /ctf
USER 1000:1000

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "server.py"]