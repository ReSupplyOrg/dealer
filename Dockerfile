FROM python:3.11.2-alpine

RUN adduser -S -u 5000 dealer

WORKDIR /dealer
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod 777 run.sh

ENV PRODUCTION true
ENV SECRET_KEY dealer
ENV POSTGRES_DATABASE dealer
ENV POSTGRES_USERNAME dealer
ENV POSTGRES_PASSWORD dealer
ENV POSTGRES_HOST dealer-postgres
ENV POSTGRES_PORT 5432
ENV REDIS_LEADER redis://dealer-redis:6379

USER 5000:5000
EXPOSE 8000
CMD ["/bin/sh", "-c", "./run.sh"]