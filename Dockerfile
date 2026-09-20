FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Nu mai copiem fișierele cu COPY, ci vom mapa folderul local ca volum
# pentru ca noul CSV să apară direct pe Windows.
CMD ["bash"] 
