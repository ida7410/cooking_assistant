# 🍳 Cooking Assistant

> An AI-powered recipe recommendation system with cooking time prediction and step simplification.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [License](#license)

---

## 🎯 Overview

Cooking Assistant is a full-stack web application that helps users discover recipes based on available ingredients, get personalized recommendations, predict cooking times, and simplify instructions for different skill levels.

### **Key Features**

- 🔍 **Ingredient-Based Search** - Find recipes using what you have
- 🤖 **AI Recommendations** - Hybrid ML system combining content and collaborative filtering
- ⏱️ **Time Prediction** - Accurate cooking time estimates with skill adjustments
- 📝 **Step Simplification** - AI-powered recipe instructions for beginners
- 🌐 **Web Interface** - Responsive Next.js frontend
- ⚡ **Fast API** - High-performance backend with async endpoints

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: FastAPI 0.110+ (ASGI)
- **ML/Data**: scikit-learn, pandas, numpy
- **AI**: Anthropic Claude API
- **Validation**: Pydantic v2
- **Server**: Uvicorn

### **Frontend**
- **Framework**: Next.js 14+
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Build Tool**: Vite

### **Infrastructure**
- **Deployment**: Railway
- **Version Control**: Git
- **CI/CD**: GitHub Actions (planned)

---

## 📁 Project Structure

```
cooking_assistant/
├── backend/                      # FastAPI backend
│   ├── src/                      # Application code
│   │   ├── main.py              # FastAPI app
│   │   ├── dependencies.py      # Dependency injection
│   │   ├── logger.py            # Logging
│   │   └── routers/             # API routes
│   ├── models/                  # ML models
│   ├── schemas/                 # Pydantic schemas
│   ├── config.py                # Configuration
│   ├── requirements.txt         # Dependencies
│   └── README.md                # Backend docs
│
├── frontend/                     # Next.js frontend
│   ├── src/                      # Source code
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   └── utils/               # Utilities
│   ├── public/                  # Static assets
│   ├── package.json             # Dependencies
│   └── README.md                # Frontend docs
│
├── data/                        # Dataset files
│   ├── RAW_recipes.csv          # Recipe data
│   └── RAW_interactions.csv     # User ratings
│
├── .github/                     # GitHub Actions
│   └── workflows/               # CI/CD pipelines
│
├── README.md                    # This file
└── LICENSE                      # MIT License
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

For questions or feedback, please open an issue on GitHub.