# 🎓 Antigravity | GDG Certificate Generation System

![Cinematic Header](https://raw.githubusercontent.com/Antigravity-AI/assets/main/banner.png)

A premium, futuristic AI-powered certificate generation web application designed for **Google Developer Groups On Campus - Holy Angel University**. Built with a focus on cinematic UI/UX, efficiency, and professional branding.

## ✨ Features

- **🚀 Premium Hero Section**: Animated gradients and smooth entrance effects.
- **🎨 Cinematic UI**: Glassmorphism cards, neon accents, and Aurora background.
- **🖼️ Smart Generator**: Automatically fits names and roles into the official GDG template.
- **📦 Batch Processing**: Generate and ZIP multiple certificates based on department or role.
- **📊 Analytics Dashboard**: Real-time stats on community growth and department distribution.
- **🔍 Advanced Search**: Filter through the officer database with ease.
- **💡 Inspirational Quotes**: Rotating leadership and developer messages for every session.
- **📄 Export Options**: High-quality PNG downloads and Excel database exports.

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Styling**: Custom CSS (Futuristic Dark Theme)
- **Logic**: Pillow (PIL), Pandas, OpenPyXL
- **Data**: Static JSON-based Officer Records

## 📁 Folder Structure

```text
GDG-cert/
│
├── app.py                # Main application logic
├── requirements.txt      # Dependency list
├── officers_data.py      # Member database & quotes
├── Template.png          # Official certificate template
├── assets/
│   └── fonts/            # Premium typography
│       ├── Inter-Bold.ttf
│       └── Inter-Regular.ttf
│
├── .streamlit/
│   └── config.toml       # Theme configuration
│
└── README.md             # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PIP

### Installation

1. **Clone the repository** (or navigate to the project folder).
2. **Create a virtual environment**:
   - **Mac/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

## 🎨 Visual Identity

- **Theme**: Obsidian Dark
- **Primary Color**: #4285F4 (Google Blue)
- **Secondary Colors**: Purple, Cyan, Pink
- **Typography**: Inter (Modern Sans Serif)

---

Built with ❤️ by **Antigravity** for **Google Developer Groups On Campus - Holy Angel University**.
