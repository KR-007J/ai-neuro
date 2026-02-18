# 🚀 Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Git** (for version control)
- **VS Code** (recommended IDE) or any code editor

Optional:
- **Docker** (for containerized deployment)
- **Postman** or similar API testing tool

---

## Step-by-Step Setup

### 1. Clone or Download the Repository

If using Git:
```bash
git clone <your-repository-url>
cd ai-neuro-adaptive-learning
```

If downloaded as ZIP:
- Extract the ZIP file
- Navigate to the extracted directory

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including FastAPI, NumPy, Pandas, and scikit-learn.

### 4. Set Up Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your preferred text editor
# For Windows: notepad .env
# For Linux/Mac: nano .env
```

Keep the default values for local development.

### 5. Generate Synthetic Data (Optional)

```bash
python data/synthetic_data_generator.py
```

This creates sample datasets in `data/processed/` for testing.

### 6. Train ML Models (Optional)

```bash
python training/train_learning_style.py
```

This trains and saves the learning style classifier model.

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### 8. Access the API

Open your browser and navigate to:

- **API Documentation (Swagger):** http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc):** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/health

---

## Running the Frontend (Optional)

If you want to use the Streamlit dashboard:

```bash
streamlit run frontend/streamlit_app.py
```

The dashboard will open automatically in your browser at http://localhost:8501

---

## Testing the API

### Using Swagger UI

1. Go to http://127.0.0.1:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

### Using curl (Command Line)

**Health Check:**
```bash
curl http://127.0.0.1:8000/health
```

**Register User:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "age": 25,
    "education_level": "Bachelors",
    "password": "securepass123"
  }'
```

**Get Recommendations:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/adaptation/recommend-content" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "user_profile": {
      "user_id": "test_user",
      "learning_style": "visual",
      "cognitive_load_capacity": 6.5
    },
    "performance_history": [0.7, 0.75, 0.8],
    "completed_content": []
  }'
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py -v

# Run with verbose output
pytest -v
```

---

## Common Issues and Solutions

### Issue: "Module not found" error

**Solution:** Make sure you've activated the virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Port already in use"

**Solution:** Either:
1. Kill the process using the port
2. Use a different port:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

### Issue: Import errors

**Solution:** Make sure you're running commands from the project root directory.

---

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Build the image
docker build -t neuro-adaptive-learning .

# Run the container
docker run -p 8000:8000 neuro-adaptive-learning
```

Access at http://localhost:8000

---

## VS Code Configuration

Recommended VS Code extensions:
- Python
- Pylance
- Python Test Explorer
- Docker (if using Docker)
- REST Client (for API testing)

---

## Next Steps

1. ✅ Explore the API documentation at http://127.0.0.1:8000/docs
2. ✅ Try the example requests
3. ✅ Run the Streamlit dashboard
4. ✅ Train your own models with custom data
5. ✅ Customize the cognitive profiling algorithms
6. ✅ Deploy to Render or another cloud platform

---

## Getting Help

If you encounter issues:

1. Check the [README.md](README.md) for more information
2. Review the API documentation
3. Look at example code in `tests/`
4. Check logs for error messages

---

**Happy Learning! 🧠🚀**
