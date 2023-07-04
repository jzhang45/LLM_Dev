import os
import json
import openai

api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

# script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(__name__))
# Load patient information from a JSON file
with open(f'{script_dir}/patient_1.json') as f:
    patient_info = json.load(f)


# Define the initial prompt
initial_prompt = "Please provide some information about your symptoms"

# Print the initial prompt
print("Assistant:", initial_prompt)
# Define the categories
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

# Extract patient details
patient_description = patient_info['description']
age = patient_info['age']
gender = patient_info['gender']
medical_records = patient_info['medical_records']

# Initialize conversation history
conversation = [{'role': 'patient', 'message': initial_prompt}]

# Main loop
while True:
    # Construct the conversation input
    conversation_input = ""
    for turn in conversation:
        if turn['role'] == 'patient':
            conversation_input += f"\nPatient: {turn['message']}"
        else:
            conversation_input += f"\nAssistant: {turn['message']}"

    # Generate a response from the model
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=conversation_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the assistant's reply
    assistant_reply = response.choices[0].text.strip()

    # Print and store the assistant's reply
    print("Assistant:", assistant_reply)
    conversation.append({'role': 'assistant', 'message': assistant_reply})

    # Check if the task is complete
    if "category" in assistant_reply:
        break

    # Prompt the patient for the next input
    patient_input = input("Patient: ")

    # Store the patient's reply
    conversation.append({'role': 'patient', 'message': patient_input})

# Extract the predicted category from the assistant's final reply
predicted_category = None
for cat in categories:
    if cat.lower() in assistant_reply.lower():
        predicted_category = cat
        break

# Print the predicted category
print("Predicted category:", predicted_category)













