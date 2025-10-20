from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta
from database import db
from strands_fitness_agent import fitness_agent
import traceback

app = FastAPI(title="Agent Sportacus API")
security = HTTPBearer()

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "fitness_app_secret_key_2024"
ALGORITHM = "HS256"

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    fitness_level: str
    primary_goal: str
    weight: float
    height: float
    age: int
    activity_level: str
    workout_frequency: str
    workout_duration: str
    target_weight: float = None
    timeline: str
    motivation: str
    preferred_time: str
    workout_location: str
    sleep_hours: str
    stress_level: str
    dietary_restrictions: str = ""
    medical_conditions: str = ""
    preferences: dict = {}

class AgentRequest(BaseModel):
    type: str
    message: str = ""

class WorkoutExercise(BaseModel):
    name: str
    sets: int = None
    reps: int = None
    weight: float = None
    duration: int = None
    notes: str = ""
    completed: bool = False

class WorkoutEntry(BaseModel):
    date: str
    title: str
    notes: str = ""
    exercises: list[WorkoutExercise] = []

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"user_id": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/auth/register")
async def register(user: UserCreate):
    user_id = db.create_user(user.username, user.password)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    token = create_access_token(user_id)
    return {"access_token": token, "user_id": user_id}

@app.post("/auth/login")
async def login(user: UserLogin):
    user_id = db.authenticate_user(user.username, user.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(user_id)
    return {"access_token": token, "user_id": user_id}

@app.post("/profile/save")
async def save_profile(profile: UserProfile, user_id: int = Depends(verify_token)):
    try:
        db.save_user_profile(user_id, profile.dict())
        return {"message": "Profile saved successfully"}
    except Exception as e:
        print(f"Profile save error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/get")
async def get_profile(user_id: int = Depends(verify_token)):
    try:
        profile = db.get_user_profile(user_id)
        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    except Exception as e:
        print(f"Profile get error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/chat")
async def chat_with_agent(request: AgentRequest, user_id: int = Depends(verify_token)):
    try:
        print(f"Agent request: {request.type}, message: {request.message}")
        
        # Get user profile for context
        profile = db.get_user_profile(user_id)
        print(f"User profile: {profile}")
        
        # Build simple context
        context = f"""User Profile:
- Fitness Level: {profile.get('fitness_level', 'beginner')}
- Goal: {profile.get('primary_goal', 'general_fitness')}
- Age: {profile.get('age', 25)}, Weight: {profile.get('weight', 150)} lbs, Height: {profile.get('height', 70)} inches
- Activity Level: {profile.get('activity_level', 'moderately_active')}
- Use imperial measurements (pounds, inches, feet) in all responses"""
        
        if profile.get('dietary_restrictions'):
            context += f"\n- Dietary Restrictions: {profile['dietary_restrictions']}"
        if profile.get('medical_conditions'):
            context += f"\n- Medical Conditions: {profile['medical_conditions']}"
        
        # Check if user wants to save workout to journal
        save_to_journal = any(phrase in request.message.lower() for phrase in [
            'save to journal', 'add to journal', 'transfer to journal', 
            'log this workout', 'save this workout', 'add this to my journal'
        ])
        
        # Create prompt based on request type
        if request.type == 'workout_plan':
            prompt = f"{context}\n\nCreate a personalized workout plan for this user."
        elif request.type == 'nutrition_advice':
            prompt = f"{context}\n\nProvide personalized nutrition advice for this user."
        elif request.type == 'chat':
            if save_to_journal:
                prompt = f"{context}\n\nUser wants to save a workout to their journal. Parse their message and create a structured workout entry. Format your response as: WORKOUT_ENTRY followed by JSON with date, title, exercises array. Then provide a friendly confirmation message.\n\nUser message: {request.message}"
            else:
                prompt = f"{context}\n\nUser question: {request.message}\n\nProvide helpful fitness advice."
        else:
            prompt = f"{context}\n\nProvide general fitness guidance."
        
        print(f"Sending prompt to agent: {prompt[:200]}...")
        
        # Call Strands agent
        response = fitness_agent(prompt)
        print(f"Agent response: {str(response)[:200]}...")
        
        # Check if response contains workout entry to save
        response_str = str(response)
        if save_to_journal and 'WORKOUT_ENTRY' in response_str:
            try:
                # Extract JSON from response
                import re
                json_match = re.search(r'WORKOUT_ENTRY\s*({.*?})(?=\n|$)', response_str, re.DOTALL)
                if json_match:
                    import json as json_lib
                    workout_data = json_lib.loads(json_match.group(1))
                    
                    # Save to journal
                    entry_id = db.save_workout_entry(user_id, workout_data)
                    
                    # Return success message
                    return {"response": f"✅ Workout saved to your journal! You can view and track it in your Workout Journal. {response_str.split('WORKOUT_ENTRY')[0] if 'WORKOUT_ENTRY' in response_str else ''}"}
            except Exception as e:
                print(f"Error saving workout from chat: {e}")
        
        return {"response": response_str}
        
    except Exception as e:
        print(f"Agent chat error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.post("/journal/save")
async def save_workout_entry(entry: WorkoutEntry, user_id: int = Depends(verify_token)):
    try:
        entry_id = db.save_workout_entry(user_id, entry.dict())
        return {"message": "Workout saved successfully", "entry_id": entry_id}
    except Exception as e:
        print(f"Journal save error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/journal/entries")
async def get_workout_entries(user_id: int = Depends(verify_token)):
    try:
        entries = db.get_workout_entries(user_id)
        return entries
    except Exception as e:
        print(f"Journal get error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/journal/exercise/{exercise_id}/complete")
async def toggle_exercise_completion(exercise_id: int, completed: bool, user_id: int = Depends(verify_token)):
    try:
        db.update_exercise_completion(exercise_id, completed)
        return {"message": "Exercise updated successfully"}
    except Exception as e:
        print(f"Exercise update error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/journal/entry/{entry_id}")
async def get_workout_entry(entry_id: int, user_id: int = Depends(verify_token)):
    try:
        entry = db.get_workout_entry(entry_id, user_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Workout entry not found")
        return entry
    except Exception as e:
        print(f"Journal get entry error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/journal/entry/{entry_id}")
async def update_workout_entry(entry_id: int, entry: WorkoutEntry, user_id: int = Depends(verify_token)):
    try:
        db.update_workout_entry(entry_id, user_id, entry.dict())
        return {"message": "Workout updated successfully"}
    except Exception as e:
        print(f"Journal update error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "simple_ai"}

# Serve frontend files
@app.get("/")
async def serve_auth():
    from fastapi.responses import FileResponse
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "auth.html")
    return FileResponse(frontend_path)

@app.get("/auth.html")
async def serve_auth_html():
    from fastapi.responses import FileResponse
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "auth.html")
    return FileResponse(frontend_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)