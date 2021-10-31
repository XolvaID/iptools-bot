FROM python:3.10.0

RUN git clone https://github.com/xolvaid/iptools-bot /home/iptools-bot/ && pip install -r /home/iptools-bot/requirements.txt

WORKDIR /home/iptools-bot/

CMD python3 -m iptools
