FROM apache/airflow:2.9.2

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

USER root

RUN apt-get update && apt-get install -y \
    wget

COPY ./dags/materi/requirements.txt /dags_requirements/materi/requirements.txt
RUN python -m venv /dags_venv/materi/venv && \
    source /dags_venv/materi/venv/bin/activate && \
    pip install -r /dags_requirements/materi/requirements.txt && \
    deactivate

COPY start.sh /start.sh
RUN chmod +x /start.sh
USER airflow

ENTRYPOINT ["/bin/bash","/start.sh"]