import openai

class DoctorCategoryAssistant:
    def __init__(self):
        self.context = "Welcome to the symptom checker!\n"
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

    def generate_response(self, user_input):
        self.context += f"User: {user_input}\n"
        prompt = self.context + self.logic
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            n=1,
            stop=None,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        self.context += f"Assistant: {response.choices[0].text.strip()}\n"
        return response.choices[0].text.strip()

# Create an instance of the DoctorCategoryAssistant class
assistant = DoctorCategoryAssistant()

# Start the multi-turn conversation
print("Assistant: Hello, what brought you here today?")
while True:
    user_input = input("User: ")
    response = assistant.generate_response(user_input)
    print(f"Assistant: {response}")
    if "Please provide the following physical information" in response:
        break