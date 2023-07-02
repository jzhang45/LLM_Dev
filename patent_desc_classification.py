import os
import openai

api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

def classify_patient_description(patient_description):
    # Define the categories
    categories = ["General Practitioner", "Cardiologist", "Dermatologist", "Pediatrics", "Neurologist", "Orthopedic Surgeon", "Radiologist", "Gastroenterologist", "Oncologist"]

    # Generate prompt for zero-shot classification
    prompt = f"Patient Description: {patient_description}\nCategories: " + ", ".join(categories) + "\nCategory:"

    # Generate completions for zero-shot classification
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3,
        n=1,
        stop=None
    )

    # Extract the predicted category from the response
    predicted_category = response.choices[0].text.strip()
    
    return predicted_category

# Example usage
patient_description_1 = "The patient is a 45-year-old male experiencing chest pain and shortness of breath."
patient_description_4 = "A 65-year-old female is experiencing frequent headaches and dizziness."

predicted_category_1 = classify_patient_description(patient_description_1)
predicted_category_4 = classify_patient_description(patient_description_4)

print("Patient Description 1:", patient_description_1)
print("Predicted Category 1:", predicted_category_1)
print()
print("Patient Description 4:", patient_description_4)
print("Predicted Category 4:", predicted_category_4)



