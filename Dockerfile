FROM python:3.8
ADD savior.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "savior.py", "1215495184:AAHIRlEAouLU4SN6mqowrKlxRaPlDXrGZSQ", "--texts", "scripts.txt" ]
