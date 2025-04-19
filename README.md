# RecoGenie Chatbot

A terminal-style chatbot interface for RecoGenie's AI solutions, powered by OpenAI. The chatbot provides information about RecoGenie's services and can handle customer inquiries.

## Features

- Terminal-style interface
- Responsive design (Desktop, Tablet, Mobile)
- OpenAI-powered responses
- Document-based knowledge (RAG system)
- Lead collection system
- Contact information handling

## Tech Stack

- Backend: FastAPI + Python
- Frontend: HTML + CSS + JavaScript
- AI: OpenAI GPT-3.5 + Sentence Transformers
- Vector Database: FAISS

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/recogenie-chatbot.git
cd recogenie-chatbot
```

2. Create and activate a conda environment:
```bash
conda create -n recogenie_chatbot python=3.9
conda activate recogenie_chatbot
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
CONTACT_EMAIL=your_contact_email
ALLOWED_ORIGINS=https://your-website.com
```

5. Add your documentation:
- Place your PDF documentation in `docs/Recogenie.pdf`
- Update `docs/About.md` and `docs/FAQ.md` with your content

## Development

Run the development server:
```bash
uvicorn chatbot_api:app --reload --port 8000 --host 0.0.0.0
```

The chatbot interface will be available at:
- Local: http://localhost:8000/static/index.html
- API Documentation: http://localhost:8000/docs

## Deployment

1. Set up your production environment variables
2. Update CORS settings in `config.py`
3. Deploy using your preferred hosting service (e.g., Heroku, DigitalOcean, AWS)
4. Point your domain to the deployed service
5. Update the frontend API endpoint in `static/index.html` if needed

## License

MIT License

## Support

For support, email hello@recogenie.com