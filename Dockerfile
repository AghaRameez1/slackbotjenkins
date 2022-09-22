FROM python:3.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ARG github_token
ENV GITHUB_TOKEN = $github_token
ARG slack_token
ENV SLACK_TOKEN = $slack_token
ARG signing_secret
ENV SIGNING_SECRET = $signing_secret
CMD python app.py