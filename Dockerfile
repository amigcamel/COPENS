FROM python:2.7.14
ENV APPDIR /COPENS
WORKDIR $APPDIR
ADD . $APPDIR
RUN mkdir $APPDIR/log
RUN pip install -r requirements.txt uwsgi
