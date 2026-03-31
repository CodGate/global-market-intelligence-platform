# Global Market Intelligence Assistant

A demo-ready Streamlit project for showcasing a market intelligence chatbot to clients.

## Features
- Single asset analysis
- Multi-opportunity comparison
- Portfolio suggestion mode
- Aggressive / Balanced / Conservative investor modes
- AI scoring system
- GitHub + Streamlit Community Cloud friendly

## Files
- `app.py` → main Streamlit app
- `requirements.txt` → Python dependencies
- `.streamlit/config.toml` → Streamlit configuration
- `.gitignore` → safe Git settings

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a new GitHub repository.
2. Upload all project files.
3. Push the repo to GitHub.
4. Go to Streamlit Community Cloud.
5. Connect your GitHub account.
6. Click **Create app**.
7. Select your repo, branch, and `app.py`.
8. Deploy.

## Important note
This version is a **demo MVP** using built-in sample data. It does not use real-time APIs.

## Future upgrades
- Add crypto API data
- Add stock API data
- Add news sentiment
- Add charts and heatmaps
- Add LLM-based explanations
