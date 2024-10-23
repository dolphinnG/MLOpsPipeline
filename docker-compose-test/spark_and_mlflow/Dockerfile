FROM bitnami/spark:3.5.0
USER root
RUN install_packages curl

COPY requirements.txt /dolphin/requirements.txt

RUN pip install -r /dolphin/requirements.txt

# must change back to 1001 to run as non-root otherwise dfs_tmpdir will not work and you are fucked 
USER 1001

