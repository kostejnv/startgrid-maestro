FROM minizinc/minizinc:latest

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt requirements.txt

RUN pip3 install --break-system-packages -r requirements.txt

COPY . .