# docker build -t sjnarmstrong/techmunch-sholto:20210717 .
# docker run  -p 8888 sjnarmstrong/techmunch-sholto:20210717
# see best practices here https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# alpine is small and small ~ secure. Distroless
FROM python:3.7-alpine3.14
# Copy first as it will never change
COPY requirements.txt /tmp/
RUN python -m pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 8888
ENTRYPOINT ["python"]
CMD ["app.py"]