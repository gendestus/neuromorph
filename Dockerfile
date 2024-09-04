FROM debian:bookworm
RUN apt update
RUN apt install -y python3 python3-pip python3-venv
WORKDIR /app
RUN python3 -m venv venv
COPY requirements.txt .
RUN . venv/bin/activate && pip install -r requirements.txt
COPY source .
CMD ["venv/bin/fastapi", "run", "main.py"]