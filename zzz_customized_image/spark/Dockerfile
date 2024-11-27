FROM bitnami/spark:3.5.3

USER root

COPY requirements.txt /dolphin/requirements.txt

RUN pip install -r /dolphin/requirements.txt
RUN pip install psutil pynvml 
# Create user with UID 1001
RUN useradd -u 1001 -m -d /home/dolphinnG dolphinnG

# must change back to 1001 to run as non-root otherwise dfs_tmpdir will not work and you are fucked 
USER 1001

# # Set username for user 1001
# RUN usermod -l dolphinnG -d /home/dolphinnG -m 1001

# zip the user's modules and use --py-files to add them to the PYTHONPATH