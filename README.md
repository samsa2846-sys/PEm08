# MotionCraft AI Competition Analyzer

AI-powered competitor analysis tool for 3D animation and motion design studios.

## Features

- **Text Analysis**: Analyze competitor descriptions and USPs using DeepSeek AI
- **Image Analysis**: Visual content analysis using Yandex Vision OCR
- **Scoring System**: Rate competitors on design, animation, innovation, execution, and client focus
- **Desktop Application**: PyQt6 GUI with CompetitionMonitor.exe
- **Web Interface**: Clean, responsive web UI for browser access

## Tech Stack

- **Backend**: FastAPI (Python 3.6+)
- **AI Services**: 
  - DeepSeek API for text analysis
  - Yandex Vision for image recognition
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Python 3.6 compatible for shared hosting

## Project Structure

```
pem08/
├── backend/
│   ├── config.py              # Configuration and settings
│   ├── main.py                # FastAPI application
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   └── services/
│       └── analyzer_service.py # AI analysis logic
├── frontend/
│   ├── index.html             # Web interface
│   ├── app.js                 # JavaScript logic
│   └── styles.css             # Styles
├── desktop_app.py             # PyQt6 desktop application
├── build.py                   # PyInstaller build script
├── requirements.txt           # Python dependencies
├── requirements-python36.txt  # Python 3.6 specific deps
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── proxy.php                 # PHP proxy for shared hosting
└── .htaccess                 # Apache configuration

```

## Installation

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/samsa2846-sys/PEm08.git
cd PEm08
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
Create `.env` file:
```env
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

YANDEX_VISION_API_KEY=your_yandex_key
YANDEX_VISION_FOLDER_ID=your_folder_id
YANDEX_VISION_ENDPOINT=https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze

API_HOST=0.0.0.0
API_PORT=8000
```

5. **Run the application**:
```bash
cd backend
python -m uvicorn main:app --reload
```

Visit `http://localhost:8000`

## Desktop Application

### Build Desktop App

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Build executable**:
```bash
python build.py
```

This creates `dist/CompetitionMonitor.exe`

3. **Run the application**:
   - Copy `.env` file to the same directory as `CompetitionMonitor.exe`
   - Double-click `CompetitionMonitor.exe`

### Using Desktop App

The desktop application provides:
- **Text Analysis Tab**: Analyze competitor text descriptions
- **Image Analysis Tab**: Upload and analyze visual content
- **Settings Tab**: View API configuration status

Features:
- Standalone executable (no Python required)
- Native desktop GUI with PyQt6
- Async analysis with progress indicators
- Example text loading
- Results export capability

### Shared Hosting Deployment (Python 3.6)

For shared hosting with Python 3.6:

1. Upload files to server
2. Create virtual environment:
```bash
python3.6 -m venv venv
source venv/bin/activate
```

3. Install Python 3.6 compatible dependencies:
```bash
pip install -r requirements-python36.txt
```

4. Configure `.env` with your API keys

5. Start uvicorn:
```bash
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

6. Configure Apache (`.htaccess`) to proxy requests through `proxy.php`

## API Endpoints

- `GET /` - Serve frontend
- `GET /health` - Health check
- `POST /analyze_text` - Analyze competitor text
- `POST /analyze_image` - Analyze image
- `GET /history` - Get analysis history
- `DELETE /history` - Clear history

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek API key | Yes |
| `DEEPSEEK_API_URL` | DeepSeek API endpoint | Yes |
| `YANDEX_VISION_API_KEY` | Yandex Cloud API key | Yes |
| `YANDEX_VISION_FOLDER_ID` | Yandex Cloud folder ID | Yes |
| `YANDEX_VISION_ENDPOINT` | Yandex Vision endpoint | Yes |
| `API_HOST` | Server host | No (default: 0.0.0.0) |
| `API_PORT` | Server port | No (default: 8000) |

## Usage

1. **Text Analysis**:
   - Paste competitor's text (website copy, service description)
   - Optionally enter competitor name
   - Click "Analyze Text"
   - View scores and insights

2. **Image Analysis**:
   - Upload screenshot or design image
   - Click "Analyze Image"
   - Get visual style analysis and recommendations

3. **Load Example**:
   - Click "Load Example" to test with sample data

## API Keys Setup

### DeepSeek API
1. Sign up at [DeepSeek](https://platform.deepseek.com/)
2. Generate API key from dashboard
3. Add to `.env` file

### Yandex Vision
1. Create account at [Yandex Cloud](https://cloud.yandex.com/)
2. Enable Vision API
3. Generate API key and folder ID
4. Add to `.env` file

## Development

**File encoding**: All files use UTF-8 encoding. Russian text in JavaScript uses Unicode escape sequences for compatibility.

**Python compatibility**: Backend is compatible with Python 3.6+ for shared hosting deployment.

## License

MIT License

## Author

Created as part of MotionCraft project for competitor analysis in motion design industry.

## Support

For issues or questions, please open an issue on GitHub.
