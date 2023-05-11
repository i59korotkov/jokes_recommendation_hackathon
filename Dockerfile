FROM python:3.10
ADD ./jokes_recommendation/ /jokes_recommendation/
RUN pip install --upgrade pip
RUN pip3 install -r jokes_recommendation/setting/requirements.txt
CMD ["python", "jokes_recommendation/start.py"]