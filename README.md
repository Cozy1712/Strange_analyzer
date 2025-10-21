# String Analyzer Service (Django + DRF)

## Overview
A RESTful API that analyzes strings and stores properties (length, palindrome check, unique chars, word count, sha256 hash, character frequency).

## Tech
- Python 3.11+ (works with 3.10+)
- Django >= 4.2
- Django REST Framework
- django-filter

## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Cozy1712/string-analyzer.git
cd string-analyzer
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### **Base URL**
```
http://127.0.0.1:8000/api/
```

---

### **1️⃣ Analyze String**
**POST** `/strings`

**Request:**
```json
{
  "value": "level"
}
```

**Response:**
```json
{
  "value": "level",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "character_frequency_map": {
      "l": 2,
      "e": 2,
      "v": 1
    }
  }
}
```

---

### **2️⃣ Retrieve Specific String**
**GET** `/strings/<string_value>`

Example:
```
GET /api/strings/level
```

---

### **3️⃣ Delete String**
**DELETE** `/strings/<string_value>`

Example:
```
DELETE /api/strings/level/delete
```

---

### **4️⃣ Filter by Natural Language**
**GET** `/strings/filter-by-natural-language?query=<your_query>`

Example:
```
GET /api/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings
```

**Response Example:**
```json
{
  "data": [
    {
      "value": "madam",
      "properties": {
        "is_palindrome": true,
        "word_count": 1,
        "length": 5
      }
    },
    {
      "value": "civic",
      "properties": {
        "is_palindrome": true,
        "word_count": 1,
        "length": 5
      }
    }
  ],
  "count": 2,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "is_palindrome": true,
      "word_count": 1
    }
  }
}
```

---

## 🧩 Project Structure

```
string_analyzer/
│
├── analyzer/
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
│
├── string_analyzer/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 💬 Example Natural Language Queries

| Query | Meaning |
|--------|----------|
| all single word palindromic strings | Returns palindromes that are one word long |
| strings longer than 10 | Returns strings with length > 10 |
| strings shorter than 5 | Returns strings with length < 5 |
| strings containing the letter a | Returns strings that include the character "a" |

---

GET /api/strings — list with filters

GET /api/strings/{string_value} — retrieve specific

DELETE /api/strings/{string_value} — delete

GET /api/strings/filter-by-natural-language?query=... — NL filter