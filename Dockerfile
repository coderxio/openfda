FROM python:3
LABEL maintainer="Caleb Dunn"
COPY . /app
WORKDIR /app
RUN pip install requests sqlalchemy pymysql cryptography cherrypy
EXPOSE 8080/tcp
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF8
ENTRYPOINT ["python3"]
CMD ["run.py"]