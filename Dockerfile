FROM pypy:3-onbuild

ADD ./ /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["./start_web.sh"]