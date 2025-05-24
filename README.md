# AI Interview Assistant

An intelligent interview assistant that uses AI to conduct technical interviews and provide detailed analysis of candidate performance.

## Features

- Real-time voice-to-text transcription
- Natural conversation with AI interviewer
- Detailed interview analysis
- Interactive UI for candidates
- MongoDB persistence for interview data
- WebSocket-based real-time communication

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- OpenAI API Key
- MongoDB (automatically set up via Docker)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Roll-Ready-main
```

2. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Start the MongoDB service using Docker:
```bash
docker-compose up -d
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the application:
- Main interface: http://localhost:8000
- API documentation: http://localhost:8000/docs

## Project Structure

```
Roll-Ready-main/
├── main.py              # FastAPI application
├── interview_analysis.py # Interview analysis logic
├── templates/           # HTML templates
│   ├── index.html      # Interview interface
│   ├── landing.html    # Landing page
│   └── report.html     # Interview report
├── static/             # Static assets
├── requirements.txt    # Python dependencies
└── docker-compose.yml  # Docker configuration
```

## API Endpoints

- `GET /` - Landing page
- `POST /interview` - Start a new interview
- `GET /report/{client_id}` - Get interview report
- `WS /ws/{client_id}` - WebSocket endpoint for real-time communication

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key
- `MONGODB_URI` - MongoDB connection string (set automatically by Docker)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- OpenAI for the GPT API
- FastAPI for the backend framework
- MongoDB for data persistence
- Bootstrap for UI components
