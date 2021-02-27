FROM     python:3.8-slim-buster

LABEL    version="0.1"
LABEL    description="Receives data from RuuviTags and exposes it via HTTP port 5150."

# install dependencies
RUN      apt-get update --quiet
RUN      apt-get install --quiet --yes libcap2-bin

# add user who runs app
RUN      useradd --create-home --shell /bin/bash ruuviserver

# use user's home directory to run app.
WORKDIR  /home/ruuviserver
COPY     requirements.txt ruuvi_server.py run_ruuvi.sh ./
RUN      chown ruuviserver:ruuviserver ./*
RUN      chmod a+x ./run_ruuvi.sh

# set up virtual env as user, before elevating Python's capabilities
USER     ruuviserver
SHELL    ["/bin/bash", "-c"]
RUN      python3.8 -m venv .       && \
         source ./bin/activate     && \
         pip install -U --no-cache-dir pip wheel  && \
         pip install --no-cache-dir -r requirements.txt

# python needs capabilities to run bleson as user.
USER     root
RUN      setcap 'cap_net_raw,cap_net_admin+eip' $(readlink -f $(which python3.8))

# back to user context for running app using bleson library
USER     ruuviserver
ENV      RUUVI_BLE_ADAPTER="Bleson"
ENTRYPOINT      ["./run_ruuvi.sh"]
