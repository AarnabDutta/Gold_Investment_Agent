# Gold Investment AI Agent 🏆

A sophisticated conversational AI agent for digital gold investment education and purchasing, featuring real-time price tracking and secure transaction management via Supabase.

## 🌟 Key Features

- **Intelligent Conversation:** AI-powered investment guidance using Meta's Llama model
- **Real-time Pricing:** Live gold rates from trusted API sources
- **Seamless Purchase Flow:** Natural transition from inquiry to transaction
- **Secure Data Handling:** Phone and email verification for purchases
- **Transaction Logging:** Automated Supabase database integration
- **Multi-Channel Access:** CLI, REST API, and web UI ready
- **Session Management:** Full support for multi-turn conversations

## 🛠️ Tech Stack

- **Python 3.9+** - Core language
- **FastAPI** - High-performance API framework
- **Supabase** - PostgreSQL database backend
- **OpenRouter** - LLM API integration
- **API Ninjas** - Gold price data provider
- **python-dotenv** - Environment management

## 📁 Project Structure

```
gold-investment/
├── main.py                      # CLI entry point
├── api_app.py                   # FastAPI application
├── flow/
│   └── agent_flow_controller.py # Conversation flow manager
├── nodes/
│   ├── gold_investment_node.py  # Investment logic
│   └── gold_purchase_node.py    # Purchase processing
├── utils/
│   ├── gold_price_api.py       # Price fetching
│   └── amount_parser.py        # Amount extraction
├── database/
│   └── supabase_client.py      # Database operations
└── tests/                      # Test suite
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gold-investment.git
cd gold-investment

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```ini
# Gold Price API
GOLDPRICE_API_URL=https://api.api-ninjas.com/v1/commodityprice?name=gold
GOLDPRICE_API_KEY=your_api_ninjas_key

# OpenRouter API
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_API_KEY=your_openrouter_key
LLAMA_MODEL_ID=meta-llama/llama-3.3-8b-instruct:free

# Supabase API
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Database Setup

Run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE gold_purchases (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    grams DECIMAL(10,4) NOT NULL,
    amount_inr DECIMAL(10,2) NOT NULL,
    price_per_gram DECIMAL(10,2) NOT NULL,
    purchase_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Running the Application

```bash
# CLI Mode (Interactive)
python main.py

# API Mode (Development)
uvicorn api_app:app --reload --port 8000
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|---------|------------|
| `/agent` | POST | Stateful chat with full investment flow |
| `/investment-chat` | POST | Single-turn investment queries |
| `/purchase` | POST | Direct purchase processing |
| `/transactions` | GET | Purchase history and audit |
| `/` | GET | Health check |

### Sample API Request

```json
POST /agent
{
    "user_id": "John",
    "message": "I want to buy gold worth ₹5000"
}
```



## 🔄 Agent Flow

```
[Start] 
   │
   └──► [Get User Name]
            │
            ▼
 ┌─────────────────────────────┐
 │ Q&A / gold_investment_node  │
 └─────────────────────────────┘
   │   │        │
   │   │        └───────────────┐
   │   │   (purchase intent)    │
   │   v                        │
   │ [Live Price Query]         │
   │   │                        │
   │   │                        ▼
   │   │                ┌─────────────────────────────┐
   │   └───────────────►│ Purchase/gold_purchase_node │
   │                    └─────────────────────────────┘
   │                              │
   │                      [Ask Phone & Email]
   │                              │
   │                      (valid  │ invalid)
   │                   ┌──────────┴─────────┐
   │                   v                    v
   │             [Write to DB]       [Re-ask Details]
   │                   │
   │             [Show Receipt]
   └───────────────────┘
```

### Flow Explanation

1. **Initial Interaction**
   - User starts the conversation
   - System asks for user's name
   - Session is initialized

2. **Investment Q&A Mode**
   - Handles general investment queries
   - Processes live price requests
   - Detects purchase intentions
   - Uses LlamaInstructLLM for responses

3. **Price Queries**
   - Direct access to real-time gold rates
   - Returns current price per gram
   - Source: API Ninjas commodities API

4. **Purchase Flow**
   - Triggered by purchase intent
   - Processes amount in INR or grams
   - Validates user contact details
   - Completes transaction in database

5. **State Management**
   - Maintains conversation context
   - Handles multi-turn dialogue
   - Preserves pending transactions
   - Returns to Q&A mode after purchase

## 🔒 Security Notes

- API keys are managed via environment variables
- User data is validated before database insertion
- Phone numbers must be 10 digits (Indian format)
- Email addresses are validated with regex
- Supabase provides additional security layers

## 🌐 Deployment

1. Choose a platform (Railway, Render, Heroku)
2. Configure environment variables
3. Deploy using platform-specific commands
4. Set up SSL for secure communication

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_llm.py
```

## 📘 Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact

- **Author:** Aarnab Dutta
- **Email:** aarnabsnp@gmail.com
- **GitHub:**  

## 🙏 Acknowledgments

- Meta AI for Llama model
- OpenRouter for API access
- API Ninjas for gold price data
- Supabase team for database platform