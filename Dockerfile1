#configuration of the containner

FROM python:3.7
#set the python to be directly sent to the terminer rather than buffred
ENV PYTHONBUFFRED 1
# ENV PIPENV_VENV_IN_PROJECT 1
#set the workdirectory of the containerµ
WORKDIR /app
# RUN pipenv --rm
COPY . /app

RUN pip install pipenv

#Copy the project to the containner
RUN pipenv install

#start project inside containner
EXPOSE 8000

ENTRYPOINT ["pipenv","run","python","-u","manage.py","runserver"]

CMD ["0.0.0.0:8000"]
    
