# 🚚 Fleet Intelligence Pro

**AI-Powered Fleet Management & Decision Intelligence Platform**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Fleet Intelligence Pro is a comprehensive AI-powered dashboard for fleet management and optimization. It provides real-time insights, predictive analytics, and intelligent recommendations to help fleet managers make data-driven decisions about their truck fleet.

### Key Capabilities
- **AI Decision Engine**: Automated KEEP/SELL/INSPECT recommendations
- **Predictive Analytics**: 90-day cost forecasting and 6-month equity projections
- **Risk Assessment**: Comprehensive risk scoring and analysis
- **Financial Tracking**: Real-time equity monitoring and P&L analysis
- **Interactive Visualizations**: 15+ premium charts and dashboards

## ✨ Features

### 📊 Executive Dashboard
- Fleet-wide KPIs and metrics
- Decision distribution analysis
- Risk profiling
- Financial performance overview
- Real-time status monitoring

### 🚚 Active Fleet Management
- Operational truck monitoring
- Utilization tracking
- Revenue and cost per mile analysis
- Advanced filtering capabilities

### 💤 Inactive Asset Disposition
- Liquidation priority ranking
- Holding cost analysis
- Equity distribution tracking
- Financial impact assessment

### 📈 Predictive Analytics
- 90-day maintenance cost predictions
- 6-month equity forecasts
- Top movers identification
- Trend analysis

### 🔍 Truck Deep Dive
- Individual truck analysis
- Risk, financial health, and efficiency gauges
- Complete vehicle history

### ⚙️ Smart Settings
- Custom threshold configuration
- 3 preset strategies (Conservative/Balanced/Aggressive)
- Manual decision criteria adjustment
- Data export capabilities

## 🎥 Demo

**Live Demo**: [Your Deployment URL Here]

**Video Walkthrough**: [Your Video Link Here]

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/fleet-intelligence-pro.git
cd fleet-intelligence-pro
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Your Model File (Optional)
Place your `fleet_models.pkl` file in the project directory for live ML predictions.

## 💻 Usage

### Run the Dashboard
```bash
streamlit run fleet_dashboard_COMPLETE.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Upload Your Data
1. Click the **"Upload Fleet Data"** button in the sidebar
2. Select your CSV file containing fleet data
3. The dashboard will automatically analyze and display insights

### Required CSV Columns
Your fleet data CSV should include:
- `Truck_ID`: Unique identifier
- `make`, `model`: Truck details
- `status`: ACTIVE or INACTIVE
- `truck_age`, `months_owned`: Age metrics
- `equity_ratio`, `current_equity`: Financial data
- `risk_score`: Risk assessment
- `fair_market_value`: Current value
- Additional columns as needed

## 📁 Project Structure

```
fleet-intelligence-pro/
│
├── fleet_dashboard_COMPLETE.py    # Main dashboard application
├── fleet_models.pkl                # ML models (optional)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
│
├── docs/                           # Documentation
│   ├── QUICK_START.md
│   ├── MODEL_INTEGRATION_GUIDE.md
│   └── HOW_TO_CHANGE_COLORS.md
│
├── tests/                          # Test files
│   └── test_model_loading.py
│
└── assets/                         # Screenshots and media
    └── screenshots/
```

## 🛠️ Technologies Used

### Core Framework
- **Streamlit**: Interactive web dashboard
- **Python 3.8+**: Core programming language

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Visualization
- **Plotly**: Interactive charts and graphs
- **Plotly Express**: High-level plotting

### Machine Learning
- **Scikit-learn**: ML model training (included in models)
- **Pickle**: Model serialization

### Styling
- **Custom CSS**: Premium dark theme
- **Google Fonts (Inter)**: Typography

## 📸 Screenshots

### Executive Dashboard
![Executive Dashboard](assets/screenshots/executive-dashboard.png)

### Predictive Analytics
![Predictive Analytics](assets/screenshots/predictive-analytics.png)

### Settings & Configuration
![Settings](assets/screenshots/settings.png)

## 🎓 Capstone Project Details

### Project Background
This project was developed as a capstone project for [Your University/Program Name]. It demonstrates the application of:
- Machine Learning for classification and regression
- Data visualization and dashboard design
- Full-stack development with Python
- Real-world business problem solving

### Learning Outcomes
- Built end-to-end ML pipeline for fleet decision-making
- Designed intuitive user interfaces for non-technical users
- Implemented predictive models for cost and equity forecasting
- Created production-ready deployment

### Datasets
- Fleet operational data (2018-2024)
- 950+ trucks analyzed
- Features: financial, operational, maintenance, and risk metrics

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@YourUsername](https://github.com/YourUsername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Thanks to [Your University/Instructor Name] for guidance
- Anthropic Claude for development assistance
- Streamlit community for amazing framework
- All contributors and testers

## 📊 Project Stats

- **Lines of Code**: 1,868
- **Charts & Visualizations**: 15+
- **Pages**: 6
- **ML Models**: 3 (Decision, Cost, Equity)
- **Development Time**: [Your timeframe]

---

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ and Python
