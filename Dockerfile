# start image
FROM python:3.7.5-slim

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files in Labyrinth directory
COPY ./Labyrinth ./

# create a virtual environment
RUN python -m venv ./env
# activate the virtual environment
ENV VIRTUAL_ENV /env
ENV PATH /usr/src/app/env/bin:$PATH

# update pip if needed
RUN pip install --upgrade pip

# install any needed packages specified in requirements.txt
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

##################################################################
# WARNING volumes to be mounted must be specified as absolute path
# in the form HOSTVOLUME:IMAGEVOLUME:ro/rw
##################################################################
# create mount points of input data and results
VOLUME /usr/src/app/indata
VOLUME /usr/src/app/Percorsi

# run main.py when the container launches
CMD ["python", "./main.py"]

