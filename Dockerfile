FROM pypy:3-onbuild

ADD ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
ENV DEBUG 1

EXPOSE 5000

CMD ["./start_web.sh"]