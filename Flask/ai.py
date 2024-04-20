import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import flask
import json,yaml
async def generate(x):
  vertexai.init(project="algorithmallies", location="us-central1")
  model = GenerativeModel("gemini-1.5-pro-preview-0409")
  responses = model.generate_content(
      [x],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )
  output_data = ""
  for response in responses:
    # Assuming the response contains text and optional end reason
    output_data = output_data + response.text
    
  
  output_data = output_data[7:-5]
  with open ('test.json','w') as fw:
    fw.write(output_data)
  # Return the list of dictionaries as JSON
  #return output_data
  return output_data
  

  



generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}



