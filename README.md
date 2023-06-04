# llm-model-engine
model engine described by coco-LoRA

This is a python API service that handles the LLM model engine. *yes the large language model model engine*

This is not intended to function beyond proving the concept of dynamic model loading, training, LoRA, and inference. This will plug in enough of other available tools to function. This is not intended to compete with the other epic efforts to provide LLM interfaces. There should be competition, but this is not it.

Start off by imitating the ChatGPT API endpoints. In a more perfect world, there's an API bridge that will translate from anything to anything. *why make an extension to emulate claude/chatgpt/koboldai if a separate bridge could do it?* I'm sure there's pro's and cons.

API endpoints https://platform.openai.com/docs/api-reference/introduction
* /v1/chat/completions - Use for generation, completions, inference
* /v1/models - List models
  * /v1/models/{model} - Get model info
* /v1/chat/completions - probably not going to imitate this in the foreseeable future
* /v1/edits - probably not going to imitate this in the foreseeable future
* /v1/images/generations - probably not going to imitate this in the foreseeable future
* /v1/embeddings - probably not going to imitate this in the foreseeable future, although they are good for the embedding manager, that can probably just use bert
* /v1/audio/transcriptions - probably not going to imitate this in the foreseeable future
* /v1/files - needed for fine tunes
* /v1/fine-tunes - POST/GET - 
* /v1/fine-tunes/{fine_tune_id} - get info on fine tune job
* /v1/fine-tunes/{fine_tune_id}/cancel - cancel fine tune job
* /v1/fine-tunes/{fine_tune_id}/events - status of fine tuning
* /v1/models/{model} - DELETE - Delete LoRA
* /v1/moderations - if there's anything that should be regulated it's chatgpt's 
* /v1/engines - deprecated


    conda create -n largelanguagemodelmodelengine python=3.10