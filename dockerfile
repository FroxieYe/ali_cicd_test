FROM python:3.7-alpine

EXPOSE 8889

# From this point, all the actions will happen under WORKDIR
WORKDIR /home/build

COPY . /home/build
COPY requirements.txt /home/build

RUN cd /home/build

# Install python dependencies
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt 

# "-u" so that it is unbuffered log, and we can check using `docker logs`
CMD ["python", "-u", "app.py"]
