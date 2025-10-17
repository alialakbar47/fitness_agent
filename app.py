"""
FitFusion Studio - Gradio Deployment Script
Deploy to HuggingFace Spaces or run locally
"""

import google.generativeai as genai
import os
from datetime import datetime
from typing import Dict, List
import gradio as gr

# Configure API (use environment variable or Spaces secret)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables!")

genai.configure(api_key=GOOGLE_API_KEY)

# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

def record_customer_interest(name: str, email: str, interest: str, phone: str = "") -> str:
    """Record customer lead information"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lead_entry = f"""
{'='*60}
LEAD CAPTURED: {timestamp}
Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}
Interest: {interest}
{'='*60}
"""
    with open('leads.txt', 'a', encoding='utf-8') as f:
        f.write(lead_entry + '\n')
    return f"✅ Thank you {name}! Your information has been recorded. Our team will contact you at {email} within 24 hours to discuss {interest}."


def record_feedback(feedback: str, customer_name: str = "Anonymous", severity: str = "medium") -> str:
    """Record customer feedback or complaints"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_number = f"FB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    feedback_entry = f"""
{'='*60}
FEEDBACK RECEIVED: {timestamp}
Ticket #: {ticket_number}
From: {customer_name}
Severity: {severity.upper()}
Feedback: {feedback}
{'='*60}
"""
    with open('feedback.txt', 'a', encoding='utf-8') as f:
        f.write(feedback_entry + '\n')
    return f"✅ Thank you for your feedback! Ticket #{ticket_number} has been created. Our team will review this {severity} priority item and respond accordingly."


def book_trial_session(name: str, email: str, preferred_date: str, session_type: str) -> str:
    """Book a free trial session"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    booking_id = f"TRIAL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    session_map = {
        'personal_training': 'Personal Training Session',
        'group_class': 'Group Fitness Class',
        'nutrition': 'Nutrition Consultation'
    }
    session_name = session_map.get(session_type, session_type)
    
    booking_entry = f"""
{'='*60}
TRIAL SESSION BOOKED: {timestamp}
Booking ID: {booking_id}
Name: {name}
Email: {email}
Session Type: {session_name}
Preferred Date: {preferred_date}
Status: PENDING CONFIRMATION
{'='*60}
"""
    with open('bookings.txt', 'a', encoding='utf-8') as f:
        f.write(booking_entry + '\n')
    
    return f"""✅ Excellent! Your trial {session_name} has been requested.

Booking ID: {booking_id}
Preferred Date: {preferred_date}

We'll send a confirmation email to {email} within 2 hours with available time slots. 
Please bring comfortable workout clothes and arrive 10 minutes early. We're excited to meet you!"""


def check_class_availability(class_type: str, preferred_day: str) -> str:
    """Check available class times for specific class types"""
    schedule = {
        'yoga': {
            'monday': ['6:00 AM', '12:00 PM', '6:30 PM'],
            'tuesday': ['6:30 AM', '5:30 PM', '7:00 PM'],
            'wednesday': ['6:00 AM', '12:00 PM', '6:30 PM'],
            'thursday': ['6:30 AM', '5:30 PM'],
            'friday': ['6:00 AM', '12:00 PM', '5:30 PM'],
            'saturday': ['8:00 AM', '10:00 AM'],
            'sunday': ['9:00 AM', '11:00 AM']
        },
        'hiit': {
            'monday': ['6:30 AM', '5:30 PM', '7:00 PM'],
            'tuesday': ['6:00 AM', '12:00 PM', '6:00 PM'],
            'wednesday': ['6:30 AM', '5:30 PM', '7:00 PM'],
            'thursday': ['6:00 AM', '6:00 PM'],
            'friday': ['6:30 AM', '5:00 PM'],
            'saturday': ['9:00 AM'],
            'sunday': ['10:00 AM']
        },
        'spin': {
            'monday': ['6:00 AM', '5:00 PM'],
            'tuesday': ['6:30 AM', '6:30 PM'],
            'wednesday': ['6:00 AM', '5:00 PM'],
            'thursday': ['6:30 AM', '6:30 PM'],
            'friday': ['6:00 AM', '5:00 PM'],
            'saturday': ['8:30 AM', '10:30 AM'],
            'sunday': ['9:30 AM']
        },
        'strength': {
            'monday': ['6:30 AM', '12:00 PM', '6:00 PM'],
            'tuesday': ['6:00 AM', '5:30 PM'],
            'wednesday': ['6:30 AM', '12:00 PM', '6:00 PM'],
            'thursday': ['6:00 AM', '5:30 PM'],
            'friday': ['6:30 AM', '12:00 PM'],
            'saturday': ['9:00 AM'],
            'sunday': ['10:00 AM']
        },
        'pilates': {
            'monday': ['7:00 AM', '12:30 PM', '5:30 PM'],
            'tuesday': ['7:00 AM', '6:00 PM'],
            'wednesday': ['7:00 AM', '12:30 PM', '5:30 PM'],
            'thursday': ['7:00 AM', '6:00 PM'],
            'friday': ['7:00 AM', '12:30 PM'],
            'saturday': ['10:00 AM'],
            'sunday': ['11:00 AM']
        },
        'dance': {
            'tuesday': ['7:00 PM'],
            'thursday': ['7:00 PM'],
            'saturday': ['11:00 AM'],
            'sunday': ['2:00 PM']
        }
    }
    
    class_type = class_type.lower().strip()
    preferred_day = preferred_day.lower().strip()
    
    if preferred_day in ['today', 'tomorrow']:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        current_day = datetime.now().weekday()
        if preferred_day == 'tomorrow':
            current_day = (current_day + 1) % 7
        preferred_day = days[current_day]
    
    if class_type not in schedule:
        available_classes = ', '.join(schedule.keys())
        return f"⚠️  Class type '{class_type}' not found. Available classes: {available_classes}"
    
    if preferred_day not in schedule[class_type]:
        return f"⚠️  No {class_type} classes scheduled for {preferred_day.capitalize()}. Try another day!"
    
    times = schedule[class_type][preferred_day]
    times_str = '\n'.join([f"  • {time}" for time in times])
    
    return f"""✅ {class_type.capitalize()} classes available on {preferred_day.capitalize()}:

{times_str}

Each class is 60 minutes. Book your spot by telling me your name, email, and preferred time!"""


def execute_tool(tool_call):
    """Execute a tool function call from Gemini"""
    function_name = tool_call.name
    function_args = tool_call.args
    
    try:
        if function_name == "record_customer_interest":
            result = record_customer_interest(
                name=function_args.get("name"),
                email=function_args.get("email"),
                interest=function_args.get("interest"),
                phone=function_args.get("phone", "")
            )
        elif function_name == "record_feedback":
            result = record_feedback(
                feedback=function_args.get("feedback"),
                customer_name=function_args.get("customer_name", "Anonymous"),
                severity=function_args.get("severity", "medium")
            )
        elif function_name == "book_trial_session":
            result = book_trial_session(
                name=function_args.get("name"),
                email=function_args.get("email"),
                preferred_date=function_args.get("preferred_date"),
                session_type=function_args.get("session_type")
            )
        elif function_name == "check_class_availability":
            result = check_class_availability(
                class_type=function_args.get("class_type"),
                preferred_day=function_args.get("preferred_day")
            )
        else:
            result = f"Error: Unknown function {function_name}"
        
        return result
        
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

# ============================================================================
# BUSINESS INFO & SYSTEM PROMPT
# ============================================================================

BUSINESS_INFO = """FitFusion Studio is an AI-powered fitness and wellness center offering personal training, group classes (Yoga, HIIT, Spin, Strength, Pilates, Dance), nutrition coaching, and wellness programs.

Location: 456 Wellness Avenue, Downtown District
Hours: Mon-Fri 5AM-10PM, Sat-Sun 7AM-8PM
Contact: hello@fitfusionstudio.com | (555) 123-4567

Membership Options:
- Starter: $79/month (unlimited classes, AI app, open gym)
- Growth: $149/month (Starter + 2 PT sessions/month, nutrition consult)
- Elite: $249/month (Growth + 4 PT sessions/month, unlimited nutrition, recovery services)
- Free trial class for new members!

Team: Sarah Mitchell (Founder), Dr. James Chen (Nutrition Director), Maria Rodriguez (Group Fitness Director), Alex Kumar (Technology Lead)"""

SYSTEM_PROMPT = f"""You are the friendly AI assistant for FitFusion Studio, an AI-powered fitness and wellness center.

BUSINESS INFORMATION:
{BUSINESS_INFO}

YOUR ROLE:
- Answer questions about services, pricing, classes, team, and facilities
- Collect customer contact info when they show interest (use record_customer_interest)
- Book trial sessions (use book_trial_session)
- Check class schedules (use check_class_availability)
- Record feedback and complaints (use record_feedback)
- Be motivating, supportive, and professional

GUIDELINES:
1. Use business info to answer questions - don't make things up
2. When someone expresses interest, use record_customer_interest tool
3. For trial bookings, use book_trial_session tool
4. For class times, use check_class_availability tool
5. For feedback/complaints, use record_feedback tool (severity: low/medium/high)
6. Be encouraging and friendly, but not pushy

Remember: Help people start their fitness journey with FitFusion Studio!"""

# ============================================================================
# TOOL DECLARATIONS
# ============================================================================

tools = [
    {
        "function_declarations": [
            {
                "name": "record_customer_interest",
                "description": "Records a potential customer's contact information and interest",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Customer's full name"},
                        "email": {"type": "string", "description": "Customer's email"},
                        "interest": {"type": "string", "description": "What they're interested in"},
                        "phone": {"type": "string", "description": "Optional phone number"}
                    },
                    "required": ["name", "email", "interest"]
                }
            },
            {
                "name": "record_feedback",
                "description": "Records customer feedback, complaints, or suggestions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "feedback": {"type": "string", "description": "The feedback text"},
                        "customer_name": {"type": "string", "description": "Customer name (default: Anonymous)"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level"}
                    },
                    "required": ["feedback"]
                }
            },
            {
                "name": "book_trial_session",
                "description": "Books a free trial session for a potential customer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Customer's full name"},
                        "email": {"type": "string", "description": "Customer's email"},
                        "preferred_date": {"type": "string", "description": "Preferred date"},
                        "session_type": {"type": "string", "enum": ["personal_training", "group_class", "nutrition"], "description": "Type of session"}
                    },
                    "required": ["name", "email", "preferred_date", "session_type"]
                }
            },
            {
                "name": "check_class_availability",
                "description": "Checks available time slots for a specific class type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "class_type": {"type": "string", "enum": ["yoga", "hiit", "spin", "strength", "pilates", "dance"], "description": "Type of class"},
                        "preferred_day": {"type": "string", "description": "Day of week or 'today'/'tomorrow'"}
                    },
                    "required": ["class_type", "preferred_day"]
                }
            }
        ]
    }
]

# ============================================================================
# AGENT CLASS
# ============================================================================

class FitFusionAgent:
    """Main agent class for FitFusion Studio chatbot"""
    
    def __init__(self, system_prompt: str, tools: List[Dict]):
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash',
            tools=tools,
            system_instruction=system_prompt
        )
        self.chat = self.model.start_chat(history=[])
    
    def send_message(self, user_message: str) -> str:
        """Send a message to the agent and get response"""
        try:
            response = self.chat.send_message(user_message)
            
            # Check if model wants to call a function
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                tool_result = execute_tool(function_call)
                
                # Send tool result back to model
                response = self.chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_call.name,
                                response={'result': tool_result}
                            )
                        )]
                    )
                )
            
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

# Initialize agent
agent = FitFusionAgent(SYSTEM_PROMPT, tools)

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

def gradio_chat_function(message, history):
    """Wrapper function for Gradio ChatInterface"""
    response = agent.send_message(message)
    return response

# Create Gradio interface
demo = gr.ChatInterface(
    fn=gradio_chat_function,
    title="🏋️ FitFusion Studio AI Assistant",
    description="""
    Welcome to FitFusion Studio! I'm your AI-powered fitness assistant. I can help you with:
    
    • 📋 Information about our services, classes, and pricing
    • 📅 Checking class schedules and availability  
    • 🎯 Booking free trial sessions
    • 💪 Collecting your information if you're interested in joining
    • 💬 Recording your feedback and suggestions
    
    **Try asking:** "What classes do you offer?" or "I want to book a trial session"
    """,
    examples=[
        "What services do you offer?",
        "What are your membership prices?",
        "What yoga classes are available on Monday?",
        "I'm interested in personal training",
        "I want to book a trial class",
        "Tell me about your team",
    ],
    theme=gr.themes.Soft(),
    chatbot=gr.Chatbot(height=500),
)

if __name__ == "__main__":
    demo.launch()
