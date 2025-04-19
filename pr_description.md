# Add AI Chatbot Feature with Terminal-Style Interface

## Features Added
- Terminal-style chatbot interface with responsive design
- OpenAI-powered responses with RAG (Retrieval Augmented Generation)
- Document-based knowledge system using FAISS
- Lead collection system
- Contact information handling
- Mobile, tablet, and desktop responsive layouts

## Technical Changes
- Added FastAPI backend with the following endpoints:
  - `/chat` - Main chatbot interaction endpoint
  - `/submit_lead` - Lead information collection
  - `/health` - Health check endpoint
- Added static files serving for the frontend
- Implemented CORS handling for security
- Added configuration management system
- Created comprehensive test suite

## New Files
- `chatbot_api.py` - Main FastAPI application
- `config.py` - Configuration management
- `static/index.html` - Terminal-style chatbot interface
- `docs/` - Knowledge base documents
- `requirements.txt` - Python dependencies
- Test files for quality assurance

## Testing Done
- Tested chatbot responses
- Verified mobile responsiveness
- Checked lead collection functionality
- Validated documentation retrieval
- Confirmed CORS handling

## How to Test
1. Create and activate conda environment:
```bash
conda create -n recogenie_chatbot python=3.9
conda activate recogenie_chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_key
CONTACT_EMAIL=hello@recogenie.com
```

4. Run the server:
```bash
uvicorn chatbot_api:app --reload --port 8000 --host 0.0.0.0
```

5. Access the chatbot at: `http://localhost:8000/static/index.html`

## Screenshots
(To be added after review)

## Next Steps
- Deploy to production
- Integrate with the main website
- Add analytics tracking
- Implement user feedback system

## Security Considerations
- OpenAI API key is managed through environment variables
- CORS is configured for security
- Input validation is implemented
- Rate limiting should be added in production

Please review and provide feedback on:
1. Code structure and organization
2. Security implementations
3. UI/UX design
4. Integration approach with main website 