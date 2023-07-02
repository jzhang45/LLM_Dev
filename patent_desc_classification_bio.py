import os
import openai

api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key
https://github.com/AndrewWooo/LLM_AI_Mavericks.git

def classify_patient_description(patient_description, age, gender, medical_records):
    # Define the categories
    categories = ["General Practitioner", "Cardiologist", "Dermatologist", "Pediatrics", "Neurologist", "Orthopedic Surgeon", "Radiologist", "Gastroenterologist", "Oncologist"]

    # Generate prompt for zero-shot classification
    prompt = f"Patient Description: {patient_description}\nAge: {age}\nGender: {gender}\nMedical Records: {medical_records}\nCategories: " + ", ".join(categories) + "\nCategory:"

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
patient_description_1 = "The patient is experiencing chest pain and shortness of breath."
age_1 = 45
gender_1 = "male"
medical_records_1 = "The patient has a history of heart disease and high blood pressure."

patient_description_4 = "The patient is experiencing frequent headaches and dizziness."
age_4 = 65
gender_4 = "female"
medical_records_4 = "The patient has a history of migraines and vertigo."

predicted_category_1 = classify_patient_description(patient_description_1, age_1, gender_1, medical_records_1)
predicted_category_4 = classify_patient_description(patient_description_4, age_4, gender_4, medical_records_4)

print("Patient Description 1:", patient_description_1)
print("Age 1:", age_1)
print("Gender 1:", gender_1)
print("Medical Records 1:", medical_records_1)
print("Predicted Category 1:", predicted_category_1)
print()
print("Patient Description 4:", patient_description_4)
print("Age 4:", age_4)
print("Gender 4:", gender_4)
print("Medical Records 4:", medical_records_4)
print("Predicted Category 4:", predicted_category_4)
