FROM python:3.10

WORKDIR /api_dir

COPY . .

RUN pip install -r requirements.txt

WORKDIR /api_dir/src

CMD ["fastapi", "run", "api.py"]