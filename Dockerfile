FROM python:3.11-slim-buster AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY src/ /src

# install dependencies and project into the local packages directory
WORKDIR /src
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

# run stage
FROM python:3.11-slim-buster

# retrieve packages from build stage
ENV PYTHONPATH=/src/pkgs
COPY --from=builder /src/__pypackages__/3.11/lib /src/pkgs

# retrieve executables
COPY --from=builder /src/__pypackages__/3.11/bin/* /bin/

WORKDIR /src
