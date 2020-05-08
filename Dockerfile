FROM python:3.8.2
LABEL maintainer="Caleb Dunn"
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8080/tcp
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF8
ENTRYPOINT ["python"]
CMD ["run.py"]
