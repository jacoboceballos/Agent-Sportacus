from strands import Agent
from strands_tools import http_request
import json

SYSTEM_PROMPT = """You are FitBot, an expert personal trainer and nutritionist. You provide:

1. Personalized workout plans based on fitness level and goals
2. Nutrition advice and meal planning
3. Exercise form corrections and safety tips
4. Motivation and progress tracking
5. Injury prevention guidance

For workout plans, consider:
- Beginner: Basic exercises, lower reps (Push-ups 3x8, Squats 3x10, Plank 3x30s)
- Intermediate: More variety, moderate intensity (Push-ups 3x15, Squats 3x20, Lunges 3x12)
- Advanced: Complex movements, high intensity (Burpees 4x10, Jump squats 4x15, Mountain climbers 4x20)

For nutrition, factor in:
- Weight loss: Caloric deficit (weight * 22 calories)
- Muscle gain: Caloric surplus (weight * 35 calories)
- General fitness: Maintenance (weight * 28 calories)

Keep responses concise, actionable, and encouraging. Always prioritize safety."""

fitness_agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[http_request]
)

def interactive_trainer():
    """Interactive terminal testing for FitBot agent"""
    print("🏋️ FitBot Agent - Strands SDK Mode")
    print("Type your fitness questions or 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'q', 'exit']:
                print("Stay fit! 💪")
                break
                
            if not user_input:
                continue
                
            print("\n🤖 FitBot thinking...")
            response = fitness_agent(user_input)
            print(f"\n{response}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    interactive_trainer()