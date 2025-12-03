# SmartCareer - AI-Powered Career Guidance Platform

An intelligent, production-ready web application that helps students and professionals discover ideal career paths through AI-powered assessments, personalized roadmaps, intelligent career counseling, and interactive 3D visualizations.

![SmartCareer](https://img.shields.io/badge/Version-2.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Flask](https://img.shields.io/badge/Flask-2.3.3-red) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Overview

SmartCareer is a comprehensive career guidance platform designed specifically for the Indian education and job market. It features:

- **AI-Powered Career Assessment** - 15-question intelligent quiz that analyzes interests, skills, and personality
- **AI Career Chatbot** - Interactive chatbot powered by OpenRouter API for personalized career guidance
- **Career Growth Roadmap** - Interactive 3D timeline showing career progression from entry-level to leadership
- **College Database** - 100+ Indian colleges including all IITs, NITs, IIITs, AIIMS, and top private universities
- **Career Insights** - Real salary data, market trends, and skill demand analysis for 15+ top skills
- **Resume Builder** - Professional resume creation tool with instant download
- **Learning Roadmaps** - Step-by-step guides for 10+ career paths
- **Scholarship Finder** - Government, private, and international scholarship listings
- **3D Effects & Animations** - Modern scroll-triggered animations and interactive 3D effects

## ✨ Key Features

### 🤖 AI Career Chatbot
- **OpenRouter API Integration** - Powered by GPT-4o-mini for intelligent responses
- **Conversation History** - Maintains context across multiple messages
- **Personalized Guidance** - Career paths, skills, education, resumes, and job search strategies
- **Quick Questions** - Pre-filled questions for common career queries
- **Responsive Design** - Fully optimized for mobile, tablet, and desktop

### 🗺️ Career Growth Roadmap
- **5 Career Stages** - Entry Level → Mid-Level → Senior → Lead → Manager
- **3D Interactive Cards** - Hover effects with tilt and depth
- **Scroll Animations** - Staggered reveal animations as you scroll
- **Progress Tracking** - Visual progress indicator and timeline
- **Detailed Information** - Skills, responsibilities, salary ranges for each stage
- **Connecting Timeline** - Animated gradient line showing progression

### 🎨 3D Effects & Animations
- **Scroll-Triggered Animations** - Fade-in, slide-in, and scale effects
- **3D Card Effects** - Perspective transforms with mouse movement tracking
- **Parallax Scrolling** - Background elements moving at different speeds
- **Magnetic Hover** - Elements subtly move toward cursor
- **Staggered Animations** - Sequential reveal with customizable delays
- **GPU-Accelerated** - Smooth 60fps performance using transform and opacity

### 📊 Career Assessment Quiz
- **15 Interactive Questions** covering work preferences, skills, environment, and interests
- **Intelligent Scoring** - 10 career path options with match percentages
- **Visual Results** - Chart.js visualizations with detailed career information
- **Top 3 Recommendations** - Personalized career suggestions with scores

### 🏫 Comprehensive College Database
- **100+ Colleges** including:
  - 23 IITs with placement data
  - 15 NITs with branch information
  - 5 IIITs (including IIIT Hyderabad with ₹32 LPA avg)
  - 12 AIIMS medical colleges
  - Top private universities (BITS, VIT, Manipal, etc.)
  - IIMs for business education
- **Search & Filter** - By type, rank, package, location
- **Real Placement Data** - Average and highest packages

## 🛠 Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework (CDN)
- **Vanilla JavaScript (ES6+)** - Modern JavaScript features
- **Chart.js** - Interactive data visualizations
- **Font Awesome** - 6000+ icons
- **AOS (Animate On Scroll)** - Scroll animations library

### Backend
- **Flask 2.3.3** - Python web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Werkzeug 2.3.7** - Password hashing and security
- **python-dotenv 1.0.0** - Environment variable management
- **requests 2.31.0** - HTTP library for API calls

### External APIs
- **OpenRouter API** - AI chatbot integration (GPT-4o-mini)

### Storage
- **In-Memory Storage** - No database required for basic functionality
- **Session Management** - Flask secure sessions

## 📁 Project Structure

```
smartcareer/
├── app.py                          # Main Flask application (900+ lines)
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore file
├── static/
│   ├── css/
│   │   └── style.css              # Custom styles, 3D effects, animations (1700+ lines)
│   ├── js/
│   │   ├── main.js                # Core utilities & helpers
│   │   ├── quiz.js                # Career assessment logic
│   │   ├── dashboard.js           # Dashboard interactions
│   │   └── animations.js          # 3D effects & scroll animations
│   └── images/
│       └── .gitkeep               # Placeholder for future assets
└── templates/
    ├── base.html                  # Base template with navigation, footer
    ├── index.html                 # Landing page with hero, features, testimonials
    ├── login.html                 # User authentication form
    ├── register.html              # User registration with validation
    ├── quiz.html                  # Interactive career assessment (15 questions)
    ├── results.html               # Quiz results with Chart.js visualizations
    ├── dashboard.html             # Personalized user dashboard with statistics
    ├── roadmap.html               # 3D Career Growth Roadmap with timeline
    ├── chatbot.html               # AI Career Guidance Chatbot interface
    ├── resume_builder.html        # Professional resume creation tool
    ├── college_finder.html        # Searchable database of 100+ colleges
    ├── scholarships.html          # Government & private scholarship listings
    ├── career_insights.html       # Market trends, salaries, top skills
    ├── career_services.html       # Career services and resources
    └── ai_ml_datascience.html    # Specialized AI/ML career track
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- OpenRouter API key (for chatbot feature)

### Step 1: Clone or Download the Project

```bash
cd "mini project"
```

### Step 2: Create Virtual Environment

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

### Step 4: Configure Environment Variables

1. Create a `.env` file in the project root:

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

2. Add the following to `.env`:

```env
FLASK_SECRET_KEY=your_secret_key_here_change_in_production
FLASK_DEBUG=True
FLASK_ENV=development
OPENROUTER_API_KEY=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
```

**Important**: Change `FLASK_SECRET_KEY` to a secure random string in production!

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

Open your browser and navigate to the URL to see the application.

## 📊 Core Features Implementation

### 1. AI Career Chatbot 🤖

**Features:**
- Real-time conversation with AI career counselor
- Maintains conversation history for context
- Personalized career guidance based on user queries
- Quick question buttons for common topics
- Clear chat functionality
- Responsive design for all devices

**API Integration:**
- Uses OpenRouter API with GPT-4o-mini model
- System prompt optimized for career guidance
- Error handling for network issues
- Timeout protection (30 seconds)

**Usage:**
1. Navigate to `/chatbot` or click "Chatbot" in navigation
2. Type your career-related question
3. Get instant, personalized advice
4. Continue conversation with follow-up questions

### 2. Career Growth Roadmap 🗺️

**5 Career Stages:**
1. **Junior/Entry Level** (0-2 years) - ₹5-12 LPA
2. **Mid-Level Developer** (2-4 years) - ₹12-25 LPA
3. **Senior Developer** (4-6 years) - ₹25-40 LPA
4. **Lead/Principal Engineer** (6-8 years) - ₹40-70 LPA
5. **Manager/Architect** (8+ years) - ₹70+ LPA

**Each Stage Includes:**
- Job title and duration
- 5 key skills with hover effects
- 5 key responsibilities
- Salary range information
- Icon representation
- Numbered badge indicator

**3D Effects:**
- Scroll-triggered reveal animations
- 3D card tilt on hover (mouse tracking)
- Connecting timeline with animated progress
- Floating icon animations
- Staggered appearance (150ms delay)

### 3. Career Assessment Quiz 📝

**15 Questions Covering:**
- Type of work preferences
- Skill development interests
- Work environment preferences
- Subject interests
- Personality traits

**Scoring Algorithm:**
- 10 career path options
- Multi-dimensional scoring
- Match percentage calculations
- Top 3 recommendations

**Results Display:**
- Chart.js pie chart visualization
- Detailed career descriptions
- Salary ranges
- Required skills
- Top hiring companies

### 4. Comprehensive College Database 🏫

**100+ Colleges:**
- **IITs** (23 institutes) - Rank 1-23 with placement data
- **NITs** (15 institutes) - Top engineering colleges
- **IIITs** (5 institutes) - Specialized IT institutes
- **AIIMS** (12 institutes) - Medical colleges
- **Private Universities** - BITS, VIT, Manipal, Thapar, SRM, Anna
- **IIMs** (5 institutes) - Business schools

**Features:**
- Searchable database
- Filter by type (IITs, NITs, etc.)
- Sort by rank, package, location
- Real placement data
- NIRF rankings
- Entrance exam requirements

### 5. Skills & Career Insights 📈

**15+ Top Skills:**
1. Python Programming - ₹5-30 LPA, 97% demand
2. AI & Machine Learning - ₹10-60 LPA, 92% demand
3. Cloud Computing (AWS/Azure) - ₹8-45 LPA, 90% demand
4. Data Science & Analytics - ₹8-50 LPA, 93% demand
5. JavaScript & React - ₹5-28 LPA, 90% demand
6. Cybersecurity - ₹7-40 LPA, 85% demand
7. DevOps & CI/CD - ₹9-45 LPA, 88% demand
8. Docker & Kubernetes - ₹10-50 LPA, 82% demand
9. Blockchain - ₹12-70 LPA, 72% demand
10. UI/UX Design - ₹4-25 LPA, 85% demand
... and 5 more

**Each Skill Includes:**
- Demand percentage
- Salary range (min-max)
- Job count estimates
- Growth rate
- Difficulty level
- Industry sectors

### 6. Resume Builder 📄

**Features:**
- Form-based creation
- Real-time HTML preview
- Professional styling
- Download as HTML
- Print-friendly format
- Sections: Personal info, Education, Experience, Skills, Projects

### 7. Learning Roadmaps 📚

**10+ Career Paths:**
1. Software Developer (4 phases)
2. Data Scientist (4 phases)
3. AI/ML Engineer (4 phases)
4. UX/UI Designer (4 phases)
5. Digital Marketing Specialist (4 phases)
6. Cybersecurity Expert (4 phases)
7. Product Manager (4 phases)
8. Cloud Architect (4 phases)
9. Business Analyst (4 phases)
10. Content Writer (4 phases)

**Each Roadmap Includes:**
- Phase-by-phase breakdown
- Timeline for each phase
- Key learning topics
- Required skills
- Technology stack
- Resource recommendations

### 8. Scholarship Database 💰

**Categories:**
- Government Scholarships (AICTE, Ministry of Education)
- Private Scholarships (Tata Trusts, HDFC Bank)
- Merit-based scholarships
- Need-based scholarships
- Category-specific scholarships

**Information:**
- Organization name
- Award amount
- Eligibility criteria
- Application deadline
- Days remaining
- Direct links

## 🎨 3D Effects & Animations

### Scroll-Triggered Animations
- **Fade-in** - Elements fade in as they enter viewport
- **Slide-in** - From left, right, or bottom
- **Scale-in** - Elements scale up on reveal
- **Staggered** - Sequential appearance with delays

### 3D Transform Effects
- **Card Tilt** - Mouse movement tracking for 3D rotation
- **3D Lift** - Cards elevate on hover with depth
- **Perspective** - 3D perspective transforms
- **Depth Layering** - Multiple Z-axis layers

### Parallax Effects
- **Background Parallax** - Slower scroll speed for backgrounds
- **Floating Elements** - Continuous floating animations
- **Depth Perception** - Foreground/background separation

### Interactive Hover Effects
- **Magnetic Hover** - Elements move toward cursor
- **3D Elevation** - Lift effect with shadows
- **Glowing Effects** - Subtle glow on hover
- **Icon Animations** - Rotate, scale, bounce

### Performance Optimizations
- **GPU Acceleration** - Uses transform and opacity
- **Intersection Observer** - Efficient scroll detection
- **Request Animation Frame** - Smooth 60fps animations
- **Throttled Events** - Optimized scroll handlers

## 🌐 API Endpoints

### Authentication
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /login` - Login page
- `POST /login` - User login
- `GET /logout` - User logout

### Core Pages
- `GET /` - Landing page
- `GET /quiz` - Career assessment quiz
- `GET /results` - Quiz results page
- `GET /dashboard` - User dashboard (protected)
- `GET /roadmap` - General career roadmap
- `GET /roadmap/<career>` - Career-specific roadmap
- `GET /chatbot` - AI Career Chatbot
- `GET /resume_builder` - Resume creation tool
- `GET /college_finder` - College database
- `GET /scholarships` - Scholarship listings
- `GET /career_insights` - Skills & market data
- `GET /career_services` - Career services
- `GET /ai_ml_datascience` - AI/ML specialization

### API Endpoints
- `POST /api/submit_quiz` - Submit quiz answers
- `POST /api/chat` - Chat with AI career counselor
- `POST /api/build_resume` - Generate resume HTML
- `GET /api/colleges?type=all|iits|nits|private` - College database
- `GET /api/skills` - Skills database
- `GET /api/careers` - Career paths information
- `GET /api/scholarships` - Scholarship listings
- `GET /api/user/stats` - User statistics (protected)

## 🎓 Career Paths Included

1. **Software Developer** - ₹5-35 LPA
2. **Data Scientist** - ₹8-55 LPA
3. **AI/ML Engineer** - ₹12-70 LPA
4. **UX/UI Designer** - ₹5-30 LPA
5. **Digital Marketing Specialist** - ₹5-25 LPA
6. **Cybersecurity Expert** - ₹8-50 LPA
7. **Product Manager** - ₹15-60 LPA
8. **Cloud Architect** - ₹15-70 LPA
9. **Business Analyst** - ₹6-30 LPA
10. **Content Writer** - ₹3-18 LPA

## 🔐 Security Features

- **Password Security**: Werkzeug `generate_password_hash` & `check_password_hash`
- **Session Management**: Flask secure sessions with configurable timeout
- **Environment Variables**: Sensitive data stored in `.env`
- **CORS Protection**: Flask-CORS for cross-origin requests
- **Input Validation**: Client and server-side validation
- **XSS Protection**: HTML escaping in chatbot messages
- **API Key Security**: OpenRouter API key stored securely

## 📊 Data Structure (In-Memory)

```python
users_storage = {
    'email': {
        'name': 'User Name',
        'password_hash': 'hashed_password',
        'created_at': 'ISO timestamp',
        'profile_data': {}
    }
}

quiz_results_storage = [
    {
        'user_email': 'user@example.com',
        'careers': ['Career 1', 'Career 2', 'Career 3'],
        'scores': {'Career 1': 85, ...},
        'timestamp': 'ISO timestamp'
    }
]

progress_storage = {
    'user_email': {
        'quizzes_taken': 2,
        'matches_found': 3,
        'roadmaps_viewed': 1
    }
}

chat_history = {
    'user_email_chat': [
        {'role': 'user', 'content': '...'},
        {'role': 'assistant', 'content': '...'}
    ]
}
```

## 🎨 Frontend Features

### Responsive Design
- **Mobile First** - Optimized for all screen sizes
- **Breakpoints** - 640px, 768px, 1024px, 1280px
- **Touch Optimized** - Minimum 44px touch targets
- **Mobile Navigation** - Collapsible menu

### Animations & Effects
- **AOS (Animate On Scroll)** - Scroll-triggered animations
- **Custom 3D Effects** - CSS transforms with perspective
- **Parallax Scrolling** - Multi-layer depth effects
- **Smooth Transitions** - Cubic-bezier easing functions
- **GPU Acceleration** - Hardware-accelerated animations

### UI Components
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Interactive data visualizations
- **Font Awesome** - 6000+ icons
- **Custom Components** - Cards, buttons, forms

## 🔧 Configuration

### Flask Settings

```python
# app.py
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.run(debug=True, host='127.0.0.1', port=5000)
```

### Environment Variables

```env
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
FLASK_ENV=development
OPENROUTER_API_KEY=your_api_key_here
```

## 📝 Usage Examples

### 1. User Registration & Login
```
1. Click "Register" on homepage
2. Enter name, email, password (min 6 characters)
3. Confirm registration
4. Login with credentials
5. Access protected features (quiz, dashboard)
```

### 2. Take Career Quiz
```
1. Click "Career Quiz" from navigation
2. Answer 15 questions honestly
3. Submit for instant results
4. View top 3 career matches with scores
5. Explore recommended career paths
```

### 3. Chat with AI Career Counselor
```
1. Navigate to "Chatbot" section
2. Type your career question
3. Get personalized guidance
4. Ask follow-up questions
5. Use quick question buttons for common topics
```

### 4. Explore Career Roadmap
```
1. Go to "Career Roadmap"
2. Scroll to see 5 career stages
3. Hover over cards for 3D effects
4. View skills and responsibilities for each stage
5. Track your progress with the indicator
```

### 5. Explore Colleges
```
1. Go to "College Finder"
2. Filter by type (IITs, NITs, etc.)
3. Sort by rank, package, or location
4. View detailed college information
5. Check placement data and rankings
```

### 6. Build Resume
```
1. Go to "Resume Builder"
2. Fill in your information
3. See real-time preview
4. Download as HTML
5. Print or share your resume
```

## 🚦 Performance Optimizations

- **Lazy Loading**: Components load on demand
- **Caching**: Session storage for quiz results and chat history
- **CDN Assets**: Tailwind, Chart.js, Font Awesome via CDN
- **Efficient Storage**: In-memory dictionaries (no database queries)
- **API Timeout**: 30-second limit on external API calls
- **GPU Acceleration**: Transform and opacity for smooth animations
- **Throttled Events**: Optimized scroll and resize handlers
- **Intersection Observer**: Efficient viewport detection

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py:
app.run(debug=True, host='127.0.0.1', port=5001)
```

### API Key Issues
- Ensure OpenRouter API key is set in `.env`
- Check API key format (starts with `sk-or-v1-`)
- Verify API key is active and has credits

### Database Issues
- All data is in-memory, resets on restart
- For persistence, integrate with MongoDB or PostgreSQL
- Chat history is session-based

### Animation Performance
- Reduce animations on mobile devices
- Check browser DevTools for performance
- Disable animations if `prefers-reduced-motion` is set

## 📱 Browser Compatibility

- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+
- **Mobile browsers** (iOS Safari, Chrome Mobile)

## 🔄 Data Persistence

Currently, the application uses in-memory storage. For production:

### 1. Add Database (MongoDB, PostgreSQL)
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
```

### 2. Add Caching (Redis)
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 3. Implement Sessions (Flask-Session)
```python
from flask_session import Session
Session(app)
```

## 📚 Learning Resources

- **Python**: [Python.org](https://python.org)
- **Flask**: [Flask Documentation](https://flask.palletsprojects.com)
- **Tailwind CSS**: [Tailwind CSS Docs](https://tailwindcss.com/docs)
- **JavaScript**: [MDN Web Docs](https://developer.mozilla.org)
- **OpenRouter API**: [OpenRouter Docs](https://openrouter.ai/docs)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Authors

- **SmartCareer Development Team**
- Built with ❤️ for Indian students and professionals

## 📞 Support

For issues, questions, or suggestions:
- Email: support@smartcareer.com
- GitHub Issues: [Report Here]
- Documentation: [Wiki]

## 🎉 Acknowledgments

- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Interactive data visualizations
- **Font Awesome** - Icon library
- **AOS** - Animate On Scroll library
- **OpenRouter** - AI API platform
- **Flask** - Python web framework

## 🚀 Recent Updates (v2.0.0)

### New Features
- ✅ AI Career Chatbot with OpenRouter integration
- ✅ 3D Career Growth Roadmap with interactive timeline
- ✅ Advanced 3D effects and scroll animations
- ✅ Parallax scrolling effects
- ✅ Magnetic hover interactions
- ✅ Scroll progress indicator
- ✅ Enhanced responsive design

### Improvements
- ✅ GPU-accelerated animations for smooth performance
- ✅ Intersection Observer for efficient scroll detection
- ✅ Mobile-optimized 3D effects
- ✅ Accessibility improvements (prefers-reduced-motion)
- ✅ Enhanced error handling

---

**Version**: 2.0.0  
**Last Updated**: December 2025  
**Status**: Production Ready ✅  
**Python Version**: 3.8+  
**Flask Version**: 2.3.3
