FROM python:3.12-slim
COPY ./ /app/
WORKDIR /app/

RUN grep -v '\-e file:.' requirements.lock > requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "src/eventpix/app.py"]
