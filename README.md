# Tech Buddy

### TEAM NAME: Support Squad – Your AI-powered family tech helper

## **Table of Contents**
- [Tech Buddy](#tech-buddy)
    - [TEAM NAME: Support Squad – Your AI-powered family tech helper](#team-name-support-squad--your-ai-powered-family-tech-helper)
  - [**Table of Contents**](#table-of-contents)
  - [**About the Project**](#about-the-project)
    - [**Overview**](#overview)
    - [**Deployment**](#deployment)
    - [**Goal**](#goal)
    - [**Problem Statement**](#problem-statement)
    - [**Objective(s)**](#objectives)
    - [**Target Audience**](#target-audience)
  - [**Wireframes**](#wireframes)
  - [**Features**](#features)
    - [**AI Integration**](#ai-integration)
    - [**User Authentication**](#user-authentication)
    - [**Chat Interface**](#chat-interface)
    - [**Profile Management**](#profile-management)
  - [**Project Structure**](#project-structure)
  - [**Tech Stack**](#tech-stack)
    - [**Languages \& Frameworks**](#languages--frameworks)
    - [**Database**](#database)
    - [**Authentication**](#authentication)
    - [**Styling \& Fonts**](#styling--fonts)
    - [**Real-time Features**](#real-time-features)
    - [**Deployment \& Services**](#deployment--services)
    - [**Development Tools**](#development-tools)
  - [**Getting Started**](#getting-started)
    - [**Prerequisites**](#prerequisites)
    - [**Installation**](#installation)
    - [**Environment Setup**](#environment-setup)
    - [**Running the Project**](#running-the-project)
  - [**Design**](#design)
    - [**UI/UX Principles**](#uiux-principles)
    - [**Color Palette**](#color-palette)
    - [**Typography**](#typography)
  - [**Future Development**](#future-development)
    - [**Enhanced Matching Algorithm**](#enhanced-matching-algorithm)
    - [**Advanced Communication Features**](#advanced-communication-features)
    - [**Profile Enhancements**](#profile-enhancements)
    - [**Safety \& Privacy**](#safety--privacy)
    - [**User Experience**](#user-experience)
    - [**Premium Features**](#premium-features)
    - [**Community Features**](#community-features)
  - [**Testing**](#testing)
  - [**Contributing**](#contributing)
  - [**Team**](#team)
  - [**License**](#license)

## **About the Project**

### **Overview** 
Tech Buddy is an AI-powered web application designed to make technology more accessible and less intimidating for elderly family members. It provides instant, easy-to-understand technical support through a friendly chat interface, eliminating the need for stressful phone calls or in-person visits.

### **Deployment**
- Live Demo: [Tech Buddy](https://support-squad-tech-buddy-9d4a4ad47301.herokuapp.com/)
- Project Management: [Kanban Board](https://github.com/users/apeskinian/projects/9/views/1)

### **Goal**
Tech Buddy aims to:
* Empower non-technical users with confidence in handling tech issues
* Reduce the burden on tech-savvy family members
* Provide friendly, jargon-free technical support
* Deliver AI-powered assistance that feels human and approachable

### **Problem Statement**
* Elderly users struggle with daily technology use
* Remote tech support is often confusing and lacks context
* Need for an accessible, 24/7 technical support solution
* Requirement for AI-powered, user-friendly responses

### **Objective(s)**
* Simplify technical support for elderly users
* Provide immediate, clear solutions to common problems
* Create a family-friendly support environment
* Reduce technology-related frustration

### **Target Audience**
* Primary: Elderly users
* Secondary: Family members providing remote support
* Tertiary: Anyone seeking quick tech assistance

## **Wireframes**

## **Features**

### **AI Integration**
Tech Buddy leverages OpenAI's technology to provide:
* Natural Language Understanding
* Context-aware responses
* Empathetic communication
* Personalized assistance

### **User Authentication**
* Secure login system using django-allauth
* Social authentication options
* Multi-factor authentication support
* Session management

### **Chat Interface**
* Real-time AI-powered responses
* User-friendly message history
* Clear, step-by-step guidance
* Context preservation

### **Profile Management**
* User profile customization
* Support history tracking
* Preference settings
* Family member connections

## **Project Structure**
```
tech_buddy/
├── tech_buddy/          # Main project configuration
├── userprofile/         # User profile management
├── openaichat/          # OpenAI integration
├── static/             # Static files
├── templates/          # HTML templates
├── staticfiles/        # Collected static files
└── venv/              # Virtual environment
```

## **Tech Stack**

### **Languages & Frameworks**
* Python 3.11
* Django 5.2.1
* JavaScript
* HTML5
* CSS3
* OpenAI API
* Bootstrap v5.3

### **Database**
* PostgreSQL (Production)
* SQLite (Development)

### **Authentication**
* django-allauth
* Social authentication
* Multi-factor authentication

### **Styling & Fonts**
* Bootstrap 5.3
* FontAwesome 6.6.0
* Custom CSS

### **Real-time Features**
* AI chat simulation
* Real-time response generation

### **Deployment & Services**
* Heroku
* WhiteNoise 6.9.0
* Gunicorn

### **Development Tools**
* Git & GitHub
* VS Code
* python-dotenv
* Django Debug Toolbar

## **Getting Started**

### **Prerequisites**
* Python 3.11 or higher
* PostgreSQL (for production)
* OpenAI API key

### **Installation**
1. Clone the repository
```bash
git clone https://github.com/yourusername/tech_buddy.git
cd tech_buddy
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  
On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### **Environment Setup**
Create a `.env` file with the following variables:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openai_api_key
```

### **Running the Project**
1. Apply migrations
```bash
python manage.py migrate
```

2. Run development server
```bash
python manage.py runserver
```

## **Design**

### **UI/UX Principles**
* Large, legible fonts
* High-contrast interface
* Simple, intuitive layouts
* Step-by-step guidance
* Dark/light mode support
* Icon + text combinations

### **Color Palette**

* Primary Blue: #2196F3 (Used for buttons and interactive elements)
* Light Blue: #d5e9f2 (Used for navigation background)
* White: #fff (Used for backgrounds)
* Light Gray: #ccc (Used for borders)
* Black: #000000 (Used for text and borders)

  
- ThE color scheme creates a modern, professional look that's  
   - Maintains good contrast for accessibility
   - Uses a consistent blue theme throughout
   - Keeps the interface clean and uncluttered  
   - Easy on the eyes

### **Typography**
Roboto, Arial, sans-serif

## **Future Development**

### **Enhanced Matching Algorithm**
* AI model fine-tuning
* Improved query understanding
* Emotional intelligence

### **Advanced Communication Features**
* Video support
* Screen sharing
* Voice messages

### **Profile Enhancements**
* Issue history
* Solution favorites
* Family connections

### **Safety & Privacy**
* Data protection
* Consent management
* Privacy controls

### **User Experience**
* Mobile app
* Dark mode
* Accessibility features
* Custom notifications

### **Premium Features**
* Voice customization
* Priority support
* Advanced features

### **Community Features**
* Tech support community
* Solution sharing
* User ratings

## **Testing**
Detailed testing information is available in [TESTING.md](TESTING.md)

## **Contributing**
[]

## **Team**
[]

## **License**
[]
