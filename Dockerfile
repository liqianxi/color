# FROM python:3.7

# WORKDIR /duckietown_pondcleaner
# COPY requirements.txt .
# RUN python3 -m pip install -r requirements.txt

# COPY . .

# RUN find .

# ENV DISABLE_CONTRACTS=1

# RUN pipdeptree
# RUN python setup.py develop --no-deps
# # run it once to see everything OK
# RUN dt-pc-demo --help
# CMD ["dt-pc-demo"]

FROM duckietown/dt-duckiebot-interface:daffy-arm64v8

WORKDIR /color_detector
COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt
ENV "N_SPLITS" 10
ENV "BINS" 10
ENV "MAX" 5

#COPY src/color_detector/color_detector.py .

CMD python3 ./color_detector.py