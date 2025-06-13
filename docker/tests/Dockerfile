FROM ubuntu:16.04
RUN apt-get update

RUN apt-get -y install libttspico-utils python3 git

RUN git clone https://github.com/mothsART/gSpeech

CMD python -m unittest speech/tests/tests.py
