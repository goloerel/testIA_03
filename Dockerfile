FROM python:3.11
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install fastapi==0.100.0
RUN pip install uvicorn==0.22.0
RUN pip install pymongo==4.4.1
RUN pip install pydantic==2.0.0
RUN pip install pytest==7.4.0
RUN pip install pytest-cov==4.1.0

COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
