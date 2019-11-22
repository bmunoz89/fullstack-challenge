FROM node:lts-alpine
WORKDIR /code
COPY yarn.lock /code/
RUN yarn install
COPY . /code/

EXPOSE 8080
