# Doctor AI Appointment

## Project Overview

The Doctor AI Appointment is a Flask-based application that integrates with the Twilio API for voice-enabled operations and the OpenAI API for natural language processing. It allows patients to schedule an appointment with a healthcare provider using voice commands. The system also sends SMS confirmations to the patients.

## Features

- Voice-activated appointment scheduling
- SMS confirmation for appointments
- Dynamic provider and time offering
- Logging of session data
- Customizable voice responses using Eleven Labs API

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.x
- Pip
- FFmpeg (for audio processing)

You'll also need:

- A Twilio account and a Twilio phone number
- An OpenAI API key
- Eleven Labs API key
- Ngrok for local development (optional)

## Installation

1. Clone the repository.

   ```
   git clone https://github.com/swapp1990/doctor-ai-appointment.git
   ```

2. Navigate to the project directory.

   ```
   cd doctors-ai-assistant
   ```

3. Install the dependencies.

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in your root directory and add your credentials like so:

   ```
   ACCOUNT_SID="your_twilio_account_sid"
   AUTH_TOKEN="your_twilio_auth_token"
   OPENAI_API_KEY="your_openai_api_key"
   NGROK_URL="your_ngrok_url"
   TWILIO_PHONE_NUMBER="your_twilio_phone_number"
   ELEVEN_LABS="your_eleven_labs_api_key"
   ```

5. Run the Flask application.

   ```
   flask run
   ```

## Usage

1. Start the Ngrok service to expose your local server to the internet.

   ```
   ngrok http 5000
   ```

2. Update the Twilio webhook with the generated Ngrok URL to point to `/start_call`.

3. Call the Twilio number linked to the service. The AI assistant will guide you through the process of booking an appointment.

## Logs

The session data will be saved in a `sessions.json` file after the appointment is confirmed through SMS.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Twilio API for voice and SMS functionalities
- OpenAI API for natural language processing
- Eleven Labs API for dynamic voice generation

For further details, please refer to the code documentation.
