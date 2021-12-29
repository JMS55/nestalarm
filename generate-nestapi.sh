#!/bin/bash

python -m grpc_tools.protoc -I./nest-protobuf --python_out=. --grpc_python_out=. $(find nest-protobuf -name \*.proto | tr '\n' ' ')
