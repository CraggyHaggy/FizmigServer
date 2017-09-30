FROM python:3.5-alpine


WORKDIR /opt

ADD . /opt

RUN apk add --no-cache gcc g++ linux-headers postgresql-dev \
&& pip install -r requirements.txt 


CMD ["flask", "run", "--host=0.0.0.0"]
