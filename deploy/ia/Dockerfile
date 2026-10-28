FROM python:3.12-slim
WORKDIR /app
COPY servidor/ia/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu && pip install --no-cache-dir -r /tmp/requirements.txt
COPY servidor /app/servidor
COPY frontend/dist /app/frontend/dist
ENV TP_SOS_MODEL=/models/sos HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
EXPOSE 4180
CMD ["uvicorn", "servidor.ia.app:app", "--host", "0.0.0.0", "--port", "4180"]
