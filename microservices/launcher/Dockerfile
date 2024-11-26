# Use the official Python image as the base image
FROM python:3.12-slim


# Set environment variables
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    && apt-get clean

# Install pyenv
RUN curl https://pyenv.run | bash

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda clean --all --yes && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> /root/.bashrc && \
    echo "conda activate base" >> /root/.bashrc

# Set environment variables for Conda
ENV PATH="/opt/conda/bin:$PATH"

# Install Apache Spark
RUN wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz -O spark-3.5.3-bin-hadoop3.tgz && \
    tar -xvzf spark-3.5.3-bin-hadoop3.tgz && \
    mv spark-3.5.3-bin-hadoop3 /opt/spark && \
    rm spark-3.5.3-bin-hadoop3.tgz

# Set environment variables for Spark
ENV SPARK_HOME="/opt/spark"
ENV PATH="$SPARK_HOME/bin:$PATH"

# Install Java
RUN apt-get update && apt-get install -y default-jdk && apt-get clean

# Set JAVA_HOME environment variable
RUN echo "export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))" >> /root/.bashrc

# Install procps for ps command
RUN apt-get update && apt-get install -y procps && apt-get clean


RUN pip install --no-cache-dir mlflow boto3 pyspark virtualenv torchx torchx[kubernetes] kubernetes

# # Create user with UID 1001
# # WE WANT TO HAVE A SHARED MOUNTED VOLUMES BETWEEN ALL THE SPARK WORKERS AND THE DRIVER
# # SO need to create user with the same uid and gid, username to the spark workers 
# # to run as non-root otherwise dfs_tmpdir will not work and you are fucked
# # RUN useradd -u 1001 -m -d /home/dolphinnG dolphinnG
RUN useradd -u 1001 -m -d /home/spark spark
USER 1001

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . . 

USER root
RUN rm -rf .venv .vscode __pycache__ 
# RUN apt-get update && apt-get install -y sudo && apt-get clean
# RUN echo "spark ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# RUN echo "cache bust"
# RUN rm dolphin.rootCA.crt dolphin.rootCA.key
# GOTTA MOUNT THE CERTS AND .ENV WHEN DEPLOYING

RUN pip install opentelemetry-distro opentelemetry-exporter-otlp

RUN opentelemetry-bootstrap -a install


EXPOSE 15003

# # Run app.py when the container launches
# CMD ["opentelemetry-instrument", "python", "app.py"]

# Copy the entrypoint script
COPY entrypoint.sh ./entrypoint.sh
COPY spark-conf-generation-script.sh ./spark-conf-generation-script.sh

RUN chmod 777 entrypoint.sh spark-conf-generation-script.sh dolphin-spark.conf dolphin.rootCA.crt dolphin.rootCA.key

USER 1001 

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

