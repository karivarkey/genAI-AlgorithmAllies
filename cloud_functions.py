import base64
import functions_framework
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

# (Import Vertex AI libraries as before)

@functions_framework.http
def classify_image(request):
  """Cloud Function to classify an image using Functions Framework

  Args:
      request (functions_framework.HttpRequest): The HTTP request object.
          It should contain a body with the base64 encoded image data.

  Returns:
      functions_framework.HttpResponse: The HTTP response object containing the classification text
          or an error message.
  """

  # Extract image data
  try:
    image_data = request.body.decode("utf-8")
    if not image_data:
      raise ValueError("Missing image data in request body")
    image_bytes = base64.b64decode(image_data)
  except (ValueError, base64.binascii.Error) as e:
    return functions_framework.HttpResponse(status_code=400, body=f"Error processing image: {str(e)}")

    text1 = """For the Given image Classify it as the follows: vegetable, packed food, other. If vegetable return it as \'veg_<vegetable_name>\', else if packed good return as \'pac_<guess_what_this_packed_good_is>\', else if it\'s something other return as \'other_<guess_what_this_packed_good_is>\' ."""

    image1 = Part.from_data(
        mime_type="image/jpeg",
        data= image_bytes
        )

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

    vertexai.init(project="algorithmallies", location="us-central1")
    model = GenerativeModel("gemini-1.0-pro-vision-001")
    responses = model.generate_content(
        [text1, image1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    # Process the response stream to extract the classification text
    classification_text = ""
    for response_part in responses:
        classification_text += response_part.text.strip()

    # Return the classification text in the response body
    return functions_framework.HttpResponse(body={"classification": classification_text})

    


