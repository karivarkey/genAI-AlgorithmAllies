#import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import flask
'''
print("enter path to image: ")
image_url = input()

with open(image_url, 'rb') as f:
    image_data = f.read()
    #base64_image = base64.b64encode(image_data)
    #print(base64_image)
'''
    
async def classify_object(image_data):
  text1 = """For the Given image Classify it as the follows: vegetable, packed food, other. If vegetable return it as \'veg_<vegetable_name>\', else if packed good return as \'pac_<guess_what_this_packed_good_is>\', else if it\'s something other return as \'other_<guess_what_this_packed_good_is>\'. only return in the specified format and failing to do so will break the code."""
  print("inside classify_object")
  image1 = Part.from_data(
    mime_type="image/jpeg",
    #data=base64.b64decode(image_data))
    data= image_data
    )

  vertexai.init(project="algorithmallies", location="us-central1")
  model = GenerativeModel("gemini-1.0-pro-vision-001")
  responses = model.generate_content(
      [text1, image1],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
)
  #return responses

  for response in responses:
    print(response.text, end="")


generation_config = {
    "max_output_tokens": 2048,
    "temperature": 0.4,
    "top_p": 0.4,
    "top_k": 32,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

#classify_object()