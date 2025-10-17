# 🏋️ Agent Sportacus - Your Personal AI Fitness Trainer

A comprehensive fitness trainer application powered by Amazon Bedrock with intelligent workout planning, nutrition advice, and progress tracking.

## 🌟 Features Overview

### 🤖 **AI-Powered Personal Training**
- **Personalized Workout Plans**: Custom workouts based on your fitness level, goals, and available equipment
- **Smart Nutrition Advice**: Tailored meal recommendations considering dietary restrictions and health conditions
- **Interactive Chat**: Natural conversation with your AI trainer for real-time fitness guidance
- **Intelligent Workout Parsing**: AI can automatically save workouts to your journal from chat conversations

### 👤 **User Management & Profiles**
- **Secure Authentication**: JWT-based login system with user registration
- **Comprehensive Onboarding**: Detailed fitness assessment covering goals, experience, schedule, and health data
- **Profile Management**: Edit and update your fitness information anytime
- **Imperial Measurements**: All data in pounds, inches, and feet for US users

### 📝 **Workout Journal & Progress Tracking**
- **Digital Gym Notebook**: Log workouts manually or let AI parse and save them automatically
- **Exercise Tracking**: Track sets, reps, weight, duration, and personal notes
- **Progress Monitoring**: Check off completed exercises and track workout consistency
- **Edit Functionality**: Modify past workout entries as needed
- **Date Organization**: View workout history chronologically

### 🎯 **Smart Features**
- **Collapsible Dashboard**: Clean interface with expandable profile stats
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Updates**: Instant saving and syncing of workout progress
- **Context-Aware AI**: Agent remembers your profile for personalized responses

## 🏗️ Architecture

- **Backend**: FastAPI with SQLite database and Amazon Bedrock integration
- **Frontend**: Pure HTML/CSS/JavaScript (no framework dependencies)
- **AI Engine**: Amazon Bedrock Strands Agent for intelligent fitness coaching
- **Database**: SQLite with automatic schema migration
- **Authentication**: JWT tokens with secure session management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Amazon Bedrock access (for AI features)
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone and Setup Backend**:
```bash
cd fitness-trainer-app/backend

pip install fastapi uvicorn sqlite3 jwt pydantic
pip install strands-agents strands-agents-tools
```

2. **Start the Server**:
```bash
python simple_ai_server.py
```

3. **Open the App**:
   - Navigate to `frontend/auth.html` in your web browser
   - Or serve via local server: `python -m http.server 8080` in frontend directory

## 📱 How to Use Agent Sportacus

### 🔐 **Getting Started**

1. **Registration/Login**:
   - Open `auth.html` in your browser
   - Create new account or login with existing credentials
   - Secure JWT authentication keeps you logged in

2. **Complete Onboarding**:
   - Fill out comprehensive fitness assessment
   - Include: age, weight, height, fitness level, goals
   - Set workout preferences, schedule, and equipment
   - Add health conditions and dietary restrictions

### 🏠 **Dashboard Features**

#### **Profile Management**
- **View Stats**: Click "Your Profile ▼" to expand/collapse detailed information
- **Edit Profile**: Update any information as your fitness journey progresses
- **Comprehensive Data**: See all your fitness metrics in organized cards

#### **AI Workout Generation**
- **Get Personalized Workout**: AI creates custom workout based on your profile
- **Get Nutrition Advice**: Receive meal and nutrition recommendations
- **Formatted Output**: Easy-to-read workout plans with proper structure

#### **Interactive Chat**
- **Natural Conversation**: Ask questions like "What exercises are good for back pain?"
- **Context Awareness**: AI knows your profile and provides personalized answers
- **Workout Saving**: Say "Save this workout to my journal" and AI will parse and store it
- **Real-time Responses**: Instant AI-powered fitness coaching

### 📝 **Workout Journal**

#### **Manual Entry Creation**
1. Click "📝 Workout Journal" from dashboard
2. Click "+ New Workout Entry"
3. Fill in workout details:
   - **Date**: When you did/plan to do the workout
   - **Title**: Name your workout (e.g., "Push Day", "Leg Day")
   - **Notes**: How you felt, observations, modifications
4. **Add Exercises**:
   - Exercise name (e.g., "Bench Press", "Squats")
   - Sets and reps (e.g., 3 sets of 10 reps)
   - Weight used (in pounds)
   - Duration (for cardio exercises)
   - Exercise-specific notes
5. Click "Save Workout"

#### **AI-Assisted Entry**
1. In the chat, describe your workout or ask for a plan
2. When you want to save it, say: "Add this workout to my journal"
3. AI automatically parses the workout and creates a structured entry
4. Review and edit in your journal if needed

#### **Tracking Progress**
- **Check Off Exercises**: Mark exercises as completed during your workout
- **Edit Past Workouts**: Click "Edit" on any entry to modify details
- **View History**: See all workouts organized by date
- **Progress Visualization**: Completed exercises show with strikethrough

### 🎯 **Advanced Features**

#### **Smart Workout Parsing**
The AI can understand natural language workouts:
- "I did 3 sets of 10 push-ups, then 20 minutes of cardio"
- "Today's leg day: squats 3x12 at 135lbs, lunges 3x10 each leg"
- "Upper body circuit: bench press, rows, shoulder press"

#### **Personalized Recommendations**
AI considers your complete profile:
- **Fitness Level**: Beginner, intermediate, or advanced exercises
- **Goals**: Weight loss, muscle gain, strength, endurance
- **Equipment**: Home, gym, or no-equipment workouts
- **Schedule**: Workout frequency and duration preferences
- **Health**: Medical conditions and injury considerations
- **Preferences**: Favorite exercise types and workout styles

#### **Progress Insights**
- **Consistency Tracking**: See workout frequency patterns
- **Exercise Completion**: Track which exercises you complete most
- **Personal Records**: Note improvements in weights and reps
- **Goal Progress**: Monitor advancement toward fitness objectives

## 🔧 Technical Details

### **Database Schema**
- **Users**: Secure authentication with hashed passwords
- **Profiles**: Comprehensive fitness data with automatic migration
- **Workout Entries**: Date-organized workout sessions
- **Exercises**: Detailed exercise tracking with completion status

### **API Endpoints**
```
Authentication:
POST /auth/register - Create new user account
POST /auth/login - User login with JWT token

Profile Management:
POST /profile/save - Save/update user profile
GET /profile/get - Retrieve user profile data

AI Agent:
POST /agent/chat - Chat with AI trainer

Workout Journal:
POST /journal/save - Create new workout entry
GET /journal/entries - Get user's workout history
GET /journal/entry/{id} - Get specific workout entry
PUT /journal/entry/{id} - Update existing workout entry
POST /journal/exercise/{id}/complete - Toggle exercise completion

System:
GET /health - Server health check
```

### **Security Features**
- **JWT Authentication**: Secure token-based sessions
- **Password Hashing**: SHA-256 encrypted password storage
- **User Isolation**: Each user's data is completely separate
- **Session Management**: Automatic logout on token expiration
- **Input Validation**: Pydantic models ensure data integrity

## 🎨 User Interface

### **Design Philosophy**
- **Clean & Intuitive**: Easy navigation without clutter
- **Mobile-Friendly**: Responsive design for all devices
- **Accessibility**: Clear fonts, good contrast, logical flow
- **Performance**: Fast loading with minimal dependencies

### **Color Scheme**
- **Primary**: Blue gradient headers for professional look
- **Success**: Green for positive actions (save, complete)
- **Warning**: Yellow for edit functions
- **Info**: Teal for journal features
- **Clean**: White backgrounds with subtle shadows

## 🚀 Deployment Options

### **Local Development**
```bash
# Backend
cd backend
python simple_ai_server.py

# Frontend (serve static files)
cd frontend
python -m http.server 8080
```

### **Production Deployment**
- **Backend**: Deploy FastAPI with Uvicorn on cloud platforms
- **Frontend**: Serve static HTML files via CDN or web server
- **Database**: SQLite for development, PostgreSQL for production
- **AI**: Configure Amazon Bedrock credentials for production

## 🤝 Contributing

Agent Sportacus is designed to be extensible:
- **New Exercise Types**: Add support for different workout categories
- **Enhanced Analytics**: Implement progress charts and statistics
- **Social Features**: Add workout sharing and community features
- **Integrations**: Connect with fitness trackers and health apps
- **Mobile App**: Build native iOS/Android applications

## 📄 License

This project is built for educational and personal use. Ensure proper Amazon Bedrock licensing for commercial deployment.

---

**Ready to start your fitness journey with Agent Sportacus? 💪**

Your personal AI trainer is waiting to help you achieve your fitness goals!
