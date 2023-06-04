# runs the api web server
# implements api calls that
#   loads a model
#   runs training
#   applies LoRA, disables LoRA
#   merges LoRA with other LoRA and with 
#
# it does this by wholly borrowing massive chunks of code from systems with similar functionality including repo's
#
# due to my lack of knowledge of writing api's in python, this will use the flask framework, because it is the most
# popular and has the most documentation (according to github copilot which autofilled this comment for me)

# import only the necessary functions because github copilot likes to go on an import spree
from flask import Flask, request, jsonify, Response
import os
import sys
import json
import time
import subprocess
import requests

app = Flask(__name__)
