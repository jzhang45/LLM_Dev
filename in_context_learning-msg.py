import os
import json
import openai
import concurrent.futures

class DoctorCategoryAssistant:
    def __init__(self, categories):
        self.categories = categories
        system_message = """
        You are a medical AI assistant. Your role is to suggest the appropriate type of doctor for the patient to see based on their details and symptoms.
        When diagnosing, remember to think step by step, first gathering the patient's symptoms, considering potential causes, asking follow-up questions if necessary, and only then making your suggestion. 
        Also, use simple, non-medical language that a layperson can understand.
        """
        self.messages = [{
            "role": "system",
            "content": system_message
        }]

        self.logic = """

        - Please provide the following physical information to navigate to the appropriate doctor category:
          - Ask for patient's age.
          - Ask for patient's gender (Male/Female/Other).
          - Ask if the patient is a smoker (Yes/No).
          - Ask if the patient has any significant medical records (Yes/No).
        - If the patient is under 18:
          - Direct the patient to the Pediatrics department.
        - If the patient is a smoker:
          - Advise the patient to visit a General Practitioner for a check-up and advice on smoking cessation.
        - If the patient is not a smoker:
          - If the patient is female:
            - If the patient has significant medical records:
              - Direct the patient to a Gynecologist/Obstetrician.
            - If the patient does not have significant medical records:
              - Direct the patient to a General Practitioner.
          - If the patient is male:
            - If the patient has significant medical records:
              - Direct the patient to a Urologist.
            - If the patient does not have significant medical records:
              - Direct the patient to a General Practitioner.
          - If the patient is neither female nor male:
            - Ask if the patient has any skin-related symptoms.
              - If yes:
                - Direct the patient to a Dermatologist.
              - If no:
                - Ask if the patient has any heart-related symptoms.
                  - If yes:
                    - Direct the patient to a Cardiologist.
                  - If no:
                    - Ask if the patient has any neurological symptoms.
                      - If yes:
                        - Direct the patient to a Neurologist.
                      - If no:
                        - Ask if the patient has any bone or joint-related symptoms.
                          - If yes:
                            - Direct the patient to an Orthopedic Surgeon.
                          - If no:
                            - Ask if the patient has any gastrointestinal symptoms.
                              - If yes:
                                - Direct the patient to a Gastroenterologist.
                              - If no:
                                - Ask if the patient has any cancer-related symptoms.
                                  - If yes:
                                    - Direct the patient to an Oncologist.
                                  - If no:
                                    - Direct the patient to a General Practitioner.
        """
    def predict_category(self, user_input):
        predicted_category = self.categories[-1]  # Default category
        for category in self.categories:
            if category.lower() in user_input.lower():
                predicted_category = category
                break
        return predicted_category

categories = [
    "General Practitioner",
    "Cardiologist",
    "Dermatologist",
    "Pediatrics",
    "Neurologist",
    "Orthopedic Surgeon",
    "Radiologist",
    "Gastroenterologist",
    "Oncologist"
]

# Create an instance of the DoctorCategoryAssistant class
assistant = DoctorCategoryAssistant(categories)

script_dir = os.path.dirname(os.path.abspath(__name__))
# Load patient information from a JSON file
with open(f'{script_dir}/patient_1.json') as f:
    patient_info = json.load(f)

# Extract patient details
# patient_description = patient_info['description']
smoke = patient_info['smoke']
age = patient_info['age']
gender = patient_info['gender']
medical_records = patient_info['medical_records']

# System message
assistant.messages.append({"role": "system", "content": assistant.logic})
# assistant.messages.append({"role": "system", "content": f"Patient Description: {patient_info['description']}"})
assistant.messages.append({"role": "system", "content": f"smoke or not: {patient_info['smoke']}"})
assistant.messages.append({"role": "system", "content": f"Patient Age: {patient_info['age']}"})
assistant.messages.append({"role": "system", "content": f"Patient Gender: {patient_info['gender']}"})
assistant.messages.append({"role": "system", "content": f"Patient Medical Records: {patient_info['medical_records']}"})

print("Assistant: Hello, what brought you here today?")
patient_input = input("Patient: ")

# Add the patient's input to the conversation
assistant.messages.append({
    "role": "user",
    "content": patient_input
})


# Loop until a category is found
while True:
    # Generate a response from the model
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        # model="gpt-3.5-turbo-16k",
        messages=assistant.messages,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.6,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the assistant's reply
    assistant_reply = response.choices[0].message['content']

    # Print the assistant's reply
    print("Assistant:", assistant_reply)

    # Extract the predicted category from the assistant's final reply
    predicted_category = assistant.predict_category(assistant_reply)

    # Break the loop if a category has been found
    if predicted_category:
        break

    # Get additional patient input
    patient_input = input("Patient: ")

    # Add assistant and patient responses to the conversation
    assistant.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    assistant.messages.append({
        "role": "user",
        "content": patient_input
    })

# Print the predicted category
print("Predicted category:", predicted_category)
