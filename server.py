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
import argparse
import os
import json
import requests

# parse the arguments
#parser = argparse.ArgumentParser(description='Run the LoRA API server')
#parser.add_argument('--models_path', type=str, default='~/models', help='path to the models directory')
#parser.add_argument('--port', type=int, default=5000, help='port to run the server on')
#args = parser.parse_args().
global models_path
models_path = '/home/username/models'
global active_model
active_model = 'llama7b'
global LoRA_path
LoRA_path = '/home/username/LoRA'


# create the flask app
app = Flask(__name__)

# define the api endpoints

def run_inference(prompt):
    # run inference on the prompt
    # return the completion
    # eventually replace with lots of cool code that does inference
    return 'climbed up the water spout'

@app.route("/v1/models")
def list_models():
    global models_path
    global active_model
    models = {}
    models['data'] = []
    for model in os.listdir(models_path):
        if os.path.isdir(os.path.join(models_path, model)) or model.endswith('.bin'):
            model_info = {}
            model_info['id'] = model
            model_info['object'] = 'model'
            model_info['owned_by'] = 'you'
            model_info['permission'] = ['read', 'write']
            models['data'].append(model_info)
    # this is supposed to also return a list of fine-tunes as models, but we're not there yet
    models['object'] = 'list'
    return jsonify(models)

@app.route("/v1/models/<model_name>")
def get_model(model_name):
    model = {}
    model['id'] = model_name
    model['object'] = 'model'
    model['owned_by'] = 'you'
    model['permission'] = ['read', 'write']
    return jsonify(model)

@app.route("/v1/completions", methods=['POST'])
def post_completion():
    # this should potentially either load a model or use the active model
    global models_path
    global active_model
    data = request.get_json()
    requested_model = data['model'] if 'model' in data else active_model
    if requested_model != active_model and requested_model in os.listdir(models_path):
        # load the model
        print('loading model ' + requested_model)
        # lots of fancy model loading stuff here
        active_model = requested_model

    prompt = data['prompt']
    # if max_tokens is not specified, default to 64
    max_tokens = data['max_tokens'] if 'max_tokens' in data else 64
    temperature = data['temperature'] if 'temperature' in data else 0
    top_p = data['top_p'] if 'top_p' in data else 1
    n = data['n'] if 'n' in data else 1
    stream = data['stream'] if 'stream' in data else False
    logprobs = data['logprobs'] if 'logprobs' in data else None
    stop = data['stop'] if 'stop' in data else '\n'

    completion_response  = run_inference(prompt)

    # create a dummy completion
    completion = {}
    completion['id'] = 'cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7'
    completion['object'] = 'text_completion'
    completion['created'] = 1589478378
    completion['model'] = active_model
    completion['choices'] = []
    choice = {}
    choice['text'] = completion_response
    choice['index'] = 0
    choice['logprobs'] = None
    choice['finish_reason'] = 'length'
    completion['choices'].append(choice)
    completion['usage'] = {}
    completion['usage']['prompt_tokens'] = 5
    completion['usage']['completion_tokens'] = 7
    completion['usage']['total_tokens'] = 12
    return jsonify(completion)

@app.route("/v1/completions", methods=['GET'])
def get_completion():
    global models_path
    global active_model
    # sends a POST to /v1/completions as a tester
    data = {}
    data['model'] = active_model
    data['prompt'] = 'What did itsy bitsy spider do?'
    data['max_tokens'] = 7
    data['temperature'] = 0
    data['top_p'] = 1
    data['n'] = 1
    data['stream'] = False
    data['logprobs'] = None
    data['stop'] = '\n'
    # send the POST to /v1/completions
    response = requests.post('http://localhost:5000/v1/completions', json=data)
    return response.json()

@app.route("/v1/fine-tunes", methods=['GET'])     # aka list LoRA
def get_fine_tunes():
    global LoRA_path
    fine_tunes = {}
    LoRAs = os.listdir(LoRA_path)
    fine_tunes['object'] = 'list'
    fine_tunes['data'] = []
    for LoRA in LoRAs:
        fine_tune = {}
        fine_tune['id'] = LoRA
        fine_tune['object'] = 'fine-tune'
        fine_tune['model'] = 'curie'
        fine_tune['created_at'] = 1614807352
        fine_tune['fine_tuned_model'] = None
        fine_tune['hyperparams'] = {}
        fine_tune['organization_id'] = 'org-...'
        fine_tune['result_files'] = []
        fine_tune['status'] = 'pending'
        fine_tune['validation_files'] = []
        fine_tune['training_files'] = []
        fine_tune['updated_at'] = 1614807352
        fine_tunes['data'].append(fine_tune)
    return jsonify(fine_tunes)

@app.route("/v1/fine-tunes", methods=['POST'])   # aka train LoRA
def post_fine_tune():
    print("fine-tune creation not implemented, returning placeholder data")
    placeholder = {
        "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
        "object": "fine-tune",
        "model": "curie",
        "created_at": 1614807352,
        "events": [
          {
            "object": "fine-tune-event",
            "created_at": 1614807352,
            "level": "info",
            "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
          }
        ],
        "fine_tuned_model": None,
        "hyperparams": {
          "batch_size": 4,
          "learning_rate_multiplier": 0.1,
          "n_epochs": 4,
          "prompt_loss_weight": 0.1,
        },
        "organization_id": "org-...",
        "result_files": [],
        "status": "pending",
        "validation_files": [],
        "training_files": [
          {
            "id": "file-XGinujblHPwGLSztz8cPS8XY",
            "object": "file",
            "bytes": 1547276,
            "created_at": 1610062281,
            "filename": "my-data-train.jsonl",
            "purpose": "fine-tune-train"
          }
        ],
        "updated_at": 1614807352,
      }
    return jsonify(placeholder)

@app.route("/v1/files", methods=['POST'])        # aka upload file for fine-tune
def post_file():
    # expecting post data to contain
    #   purpose: the purpose of the file
    #   file: the name of the file
    #   data: the data of the file

    print("file upload not implemented, returning placeholder data")
    placeholder = {
        "id": "file-XGinujblHPwGLSztz8cPS8XY",
        "object": "file",
        "bytes": 1547276,
        "created_at": 1610062281,
        "filename": "my-data-train.jsonl",
        "purpose": "fine-tune-train"
      }
    return jsonify(placeholder)

@app.route("/v1/files", methods=['GET'])         # aka list files
def get_files():
    # not implemented, returning placeholder data
    print("file listing not implemented, returning placeholder data")
    placeholder = {
        "data": [
            {
                "id": "file-ccdDZrC3iZVNiQVeEA6Z66wf",
                "object": "file",
                "bytes": 175,
                "created_at": 1613677385,
                "filename": "train.jsonl",
                "purpose": "search"
            },
            {
                "id": "file-XjGxS3KTG0uNmNOK362iJua3",
                "object": "file",
                "bytes": 140,
                "created_at": 1613779121,
                "filename": "puppy.jsonl",
                "purpose": "fine-tune"
            }
        ],
        "object": "list"
    }
    return jsonify(placeholder)
