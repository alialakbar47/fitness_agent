# FitFusion Studio - AI-Powered Business Assistant

An intelligent chatbot for FitFusion Studio, a fictional fitness and wellness center. Built with Google Gemini API and Gradio, featuring 4 tool functions for lead collection, feedback, bookings, and class availability.

## 🎯 Features

- **Information Queries**: Answers questions about services, pricing, team, and facilities
- **Lead Collection**: Captures potential customer information automatically
- **Trial Bookings**: Books free trial sessions for interested customers
- **Class Schedules**: Checks and shares available class times
- **Feedback Recording**: Logs customer feedback with priority levels

## 🏗️ Project Structure

```
business_bot/
├── me/
│   ├── about_business.pdf          # Business profile document (included)
│   └── business_summary.txt        # Business summary text
├── business_agent.ipynb            # Main Jupyter notebook
├── app.py                          # Gradio deployment script
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not committed)
├── .env.example                    # Template for environment variables
└── README.md                       # This file
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env and add your Google API key
# Get your key from: https://makersuite.google.com/app/apikey
```

Your `.env` file should contain:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

#### Option A: Using Jupyter Notebook

```powershell
jupyter notebook business_agent.ipynb
```

Then run all cells in order.

#### Option B: Using Standalone App

```powershell
python app.py
```

The Gradio interface will launch at `http://localhost:7860`

## 🧪 Testing

The notebook includes comprehensive testing checkpoints:

1. **Tool Testing**: Tests each of the 4 tools individually
2. **API Connection**: Verifies Gemini API connectivity
3. **Agent Testing**: Tests full conversation flow with tool calling
4. **Interface Testing**: Launches Gradio UI for manual testing

### Test Scenarios

Try these example queries:

- "What services do you offer?"
- "I'm interested in personal training" (tests lead collection)
- "What yoga classes are on Monday?" (tests availability check)
- "I want to book a trial session" (tests booking)
- "The gym was great today!" (tests feedback)

## 🛠️ Tools Implemented

### 1. record_customer_interest

Captures lead information when someone expresses interest.

- **Input**: name, email, interest, phone (optional)
- **Output**: Confirmation message, logs to `leads.txt`

### 2. record_feedback

Records customer feedback, complaints, or suggestions.

- **Input**: feedback, customer_name, severity (low/medium/high)
- **Output**: Ticket number, logs to `feedback.txt`

### 3. book_trial_session

Books a free trial session for potential customers.

- **Input**: name, email, preferred_date, session_type
- **Output**: Booking confirmation with ID, logs to `bookings.txt`

### 4. check_class_availability

Checks available time slots for specific class types.

- **Input**: class_type, preferred_day
- **Output**: List of available times

## 📊 Data Files

The agent creates and maintains three log files:

- `leads.txt` - Customer interest records
- `feedback.txt` - Feedback and complaints
- `bookings.txt` - Trial session bookings

## 🏢 About FitFusion Studio

FitFusion Studio is a fictional AI-powered fitness and wellness center featuring:

- Personal Training with AI analytics
- Group Classes (Yoga, HIIT, Spin, Strength, Pilates, Dance)
- Nutrition Coaching with AI meal planning
- Wellness Programs

**Membership Tiers:**

- Starter: $79/month
- Growth: $149/month
- Elite: $249/month

**Location:** 456 Wellness Avenue, Downtown District  
**Hours:** Mon-Fri 5AM-10PM, Sat-Sun 7AM-8PM  
**Contact:** hello@fitfusionstudio.com | (555) 123-4567

## 🚢 Deployment (Optional)

### Deploy to HuggingFace Spaces

1. Create a new Space at https://huggingface.co/spaces
2. Choose "Gradio" as the SDK
3. Upload: `app.py`, `requirements.txt`, `README.md`
4. Add `GOOGLE_API_KEY` as a Space secret in Settings
5. The app will auto-deploy!

## 🔧 Technical Details

- **AI Model**: Google Gemini 1.5 Flash
- **Framework**: Gradio for UI
- **Language**: Python 3.8+
- **Tool Calling**: Gemini Function Calling API

## 📝 Assignment Requirements

✅ Fictional business with complete identity  
✅ PDF document (about_business.pdf)  
✅ Text summary (business_summary.txt)  
✅ 4 tool functions implemented (exceeds minimum of 2)  
✅ System prompt with character and context  
✅ Gradio ChatInterface  
✅ Full implementation in Jupyter notebook  
✅ Comprehensive testing and debugging

## 🎬 Quick Start Guide

1. **First time setup:**

   ```powershell
   pip install -r requirements.txt
   # Add your API key to .env file
   ```

2. **Run the chatbot:**

   ```powershell
   python app.py
   ```

3. **Test the agent:**
   - Ask about services
   - Express interest (provide name & email)
   - Check class schedules
   - Book a trial session
   - Leave feedback

## 📚 Learning Resources

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Function Calling Guide](https://ai.google.dev/docs/function_calling)

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"

- Check `.env` file exists in project root
- Verify key is correctly formatted
- Restart Python kernel/terminal after adding key

### Gradio won't launch

- Check if port 7860 is available
- Try: `demo.launch(server_port=7861)`

### Tool not called

- Check tool descriptions are clear
- Verify user message matches tool use case
- Review system prompt instructions
