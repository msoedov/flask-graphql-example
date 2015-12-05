FROM pypy:3-onbuild

ADD ./ /app
WORKDIR /app
RUN make req
ENV DEBUG 1

EXPOSE 5000

CMD ./start_web.sh