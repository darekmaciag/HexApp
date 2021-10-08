###########
# BUILDER #
###########

# pull official base image
FROM python:3.8-slim-buster as builder

# set work directory 
WORKDIR /usr/src/hexapp

# set environment variables 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/hexapp/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8-slim-buster

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
COPY --from=builder /usr/src/hexapp/wheels /wheels
COPY --from=builder /usr/src/hexapp/requirements.txt .
RUN pip install --no-cache /wheels/*

# set work directory
WORKDIR /usr/src/hexapp

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/hexapp/entrypoint.sh

# copy our django project
COPY ./hexapp .

# run entrypoint.sh
RUN chmod +x /usr/src/hexapp/entrypoint.sh
ENTRYPOINT ["/usr/src/hexapp/entrypoint.sh"]