FROM python:3.7
LABEL maintainer="dicmandilan@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app/app.py"]