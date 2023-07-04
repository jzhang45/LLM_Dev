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

# System message
system_prompt = f"You are an AI medical assistant. Based on the patient's details and symptoms, suggest the appropriate type of doctor they should see.\n"
system_prompt += f"Patient Details:\nDescription: {patient_description}\nAge: {age}\nGender: {gender}\n"

for medical_record in medical_records:
    system_prompt += f"Medical Record: {medical_record}\n"

system_prompt += "\nConversation:"

# Main loop
while True:
    # User input
    patient_input = input("Patient: ")

    # Construct the conversation input
    conversation_input = system_prompt + f"\nPatient: {patient_input}"

    # Generate a response from the model
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=conversation_input,
        max_tokens=150,
        n=1,
        stop=["\n"],
        temperature=0.6,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the assistant's reply
    assistant_reply = response.choices[0].text.strip()

    # Print the assistant's reply
    print("Assistant:", assistant_reply)

    # Update system prompt
    system_prompt += f"\nPatient: {patient_input}\nAssistant: {assistant_reply}"

    # Check if the task is complete
    if any(cat.lower() in assistant_reply.lower() for cat in categories):
        break

# Extract the predicted category from the assistant's final reply
predicted_category = None
for cat in categories:
    if cat.lower() in assistant_reply.lower():
        predicted_category = cat
        break

# Print the predicted category
print("Predicted category:", predicted_category)










