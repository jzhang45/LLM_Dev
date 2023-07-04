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

# Initialize the predicted category
predicted_category = None
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
system_prompt = f"You are a medical AI assistant. Your role is to suggest the appropriate type of doctor for the patient to see based on their details and symptoms.\n"
system_prompt += f"Patient Details:\nDescription: {patient_description}\nAge: {age}\nGender: {gender}\n"

for medical_record in medical_records:
    system_prompt += f"Medical Record: {medical_record}\n"

# Define the few-shot examples for each category
few_shot_examples = {
    "General Practitioner": [
        {
            "role": "user",
            "content": "I have a cough and sore throat."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, you should consult a general practitioner."
        },
        {
            "role": "user",
            "content": "I also have a fever and body aches."
        },
        {
            "role": "assistant",
            "content": "In that case, it's best to see a general practitioner for a comprehensive evaluation."
        },
        {
            "role": "user",
            "content": "What about my persistent fatigue?"
        },
        {
            "role": "assistant",
            "content": "For persistent fatigue, a general practitioner can help assess and guide you further."
        }
    ],
    "Cardiologist": [
        {
            "role": "user",
            "content": "I experience chest pain and shortness of breath."
        },
        {
            "role": "assistant",
            "content": "Considering your symptoms, it's important to consult a cardiologist."
        },
        {
            "role": "user",
            "content": "I also have a family history of heart disease."
        },
        {
            "role": "assistant",
            "content": "With a family history of heart disease, it's recommended to see a cardiologist for proper evaluation and guidance."
        },
        {
            "role": "user",
            "content": "What about my elevated blood pressure?"
        },
        {
            "role": "assistant",
            "content": "A cardiologist can help manage your elevated blood pressure and provide appropriate treatment options."
        }
    ],
    "Dermatologist": [
        {
            "role": "user",
            "content": "I have a rash on my skin."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, it's best to consult a dermatologist."
        },
        {
            "role": "user",
            "content": "I also have itching and redness on the affected area."
        },
        {
            "role": "assistant",
            "content": "For itching and redness along with the rash, a dermatologist can provide a proper diagnosis and treatment."
        },
        {
            "role": "user",
            "content": "What about my dry and flaky skin?"
        },
        {
            "role": "assistant",
            "content": "Dry and flaky skin can be addressed by a dermatologist who can recommend suitable skincare routines and products."
        }
    ],
    "Pediatrics": [
        {
            "role": "user",
            "content": "My child has a persistent cough and runny nose."
        },
        {
            "role": "assistant",
            "content": "Based on the symptoms you described, it's advisable to see a pediatrician."
        },
        {
            "role": "user",
            "content": "My child also has a high fever and seems lethargic."
        },
        {
            "role": "assistant",
            "content": "With the combination of high fever and lethargy, it's important to consult a pediatrician for proper evaluation and care."
        },
        {
            "role": "user",
            "content": "What about my child's frequent ear infections?"
        },
        {
            "role": "assistant",
            "content": "Frequent ear infections in children can be addressed by a pediatrician who specializes in child healthcare."
        }
    ],
    "Neurologist": [
        {
            "role": "user",
            "content": "I've been experiencing frequent headaches and dizziness."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, it's advisable to see a neurologist."
        },
        {
            "role": "user",
            "content": "I also have numbness and tingling in my limbs."
        },
        {
            "role": "assistant",
            "content": "Numbness and tingling along with your other symptoms require evaluation by a neurologist."
        },
        {
            "role": "user",
            "content": "What about my difficulty in maintaining balance?"
        },
        {
            "role": "assistant",
            "content": "Difficulty in maintaining balance should be assessed by a neurologist who specializes in the nervous system and related disorders."
        }
    ],
    "Orthopedic Surgeon": [
        {
            "role": "user",
            "content": "I have persistent joint pain and stiffness."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, it's recommended to consult an orthopedic surgeon."
        },
        {
            "role": "user",
            "content": "I also have difficulty in performing daily activities due to joint problems."
        },
        {
            "role": "assistant",
            "content": "If your joint problems are impacting your daily activities, an orthopedic surgeon can provide specialized care and treatment options."
        },
        {
            "role": "user",
            "content": "What about my history of fractures and bone injuries?"
        },
        {
            "role": "assistant",
            "content": "With a history of fractures and bone injuries, it's advisable to consult an orthopedic surgeon who specializes in bone-related issues."
        }
    ],
    "Radiologist": [
        {
            "role": "user",
            "content": "I've been experiencing persistent abdominal pain."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, it's advisable to see a radiologist for further evaluation."
        },
        {
            "role": "user",
            "content": "I also have been asked to undergo imaging tests for a proper diagnosis."
        },
        {
            "role": "assistant",
            "content": "Imaging tests play a crucial role in diagnosis, and a radiologist can interpret and provide insights based on those tests."
        },
        {
            "role": "user",
            "content": "What about my follow-up imaging after a previous surgery?"
        },
        {
            "role": "assistant",
            "content": "For follow-up imaging after a surgery, a radiologist can assess the progress and provide necessary recommendations."
        }
    ],
    "Gastroenterologist": [
        {
            "role": "user",
            "content": "I have frequent abdominal bloating and discomfort."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, it's advisable to consult a gastroenterologist."
        },
        {
            "role": "user",
            "content": "I also experience acid reflux and heartburn regularly."
        },
        {
            "role": "assistant",
            "content": "Acid reflux and heartburn can be addressed by a gastroenterologist who specializes in digestive system disorders."
        },
        {
            "role": "user",
            "content": "What about my persistent diarrhea and changes in bowel movements?"
        },
        {
            "role": "assistant",
            "content": "Persistent diarrhea and changes in bowel movements require evaluation by a gastroenterologist to identify and manage any underlying conditions."
        }
    ],
    "Oncologist": [
        {
            "role": "user",
            "content": "I've found a lump in my breast and I've been having unexplained weight loss."
        },
        {
            "role": "assistant",
            "content": "Based on your symptoms, you should promptly consult with an Oncologist. They specialize in diagnosing and treating cancer, which includes breast cancer."
        },
        {
            "role": "user",
            "content": "What if I have prolonged fatigue and night sweats?"
        },
        {
            "role": "assistant",
            "content": "If you're experiencing prolonged fatigue and night sweats, it's important to see an Oncologist for further evaluation."
        },
        {
            "role": "user",
            "content": "Do I need to consider my family history of cancer?"
        },
        {
            "role": "assistant",
            "content": "With a family history of cancer, it's advisable to consult an Oncologist for appropriate screening and guidance."
        }
    ]
}

# Generate the context for each category
category_contexts = {}
for category in categories:
    category_examples = few_shot_examples.get(category, [])
    category_context = system_prompt + f"{category} Examples:\n"
    for example in category_examples:
        role = example["role"]
        content = example["content"]
        category_context += f"{role.capitalize()}: {content}\n"
    category_contexts[category] = category_context

# Get patient input
patient_input = input("Patient: ")

# Loop until a category is found or there are no more patient inputs
while not predicted_category and patient_input:
    # Initialize the best category and its score
    best_category = None
    best_score = -1

    # Loop through each category and determine the score based on the generated context
    for category in categories:
        category_prompt = category_contexts[category] + f"\nPatient Symptoms: {patient_input}\n"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=category_prompt,
            max_tokens=150,
            n=1,
            stop=["\n"],
            temperature=0.6,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        assistant_reply = response.choices[0].text.strip()

        # Check if the assistant's reply indicates the category
        if category.lower() in assistant_reply.lower():
            predicted_category = category
            break

        # Calculate the score based on the assistant's reply
        # score = response.choices[0].score
        score = assistant_reply.lower().count(category.lower())
        if score > best_score:
            best_score = score
            best_category = category

    # If no category is found, set the best category based on the score
    if not predicted_category:
        predicted_category = best_category

    # Get additional patient input if a category is not found
    if not predicted_category:
        patient_input = input("Patient: ")

# Print the predicted category
if predicted_category:
    print("Predicted category:", predicted_category)
else:
    print("Unable to determine the category.")
