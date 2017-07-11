from clarifai.rest import ClarifaiApp

# Defining a function that will return details from an image
def get_keywords_from_image(url_of_image):
    # Passing the api_key
    app = ClarifaiApp(api_key='ecd67c30d8bc40d49dc25499fcb56862')

    model = app.models.get('general-v1.3')
    # Response from Get
    response = model.predict_by_url(url=url_of_image)
    # Returning the response from predict_by_url GET call
    return response