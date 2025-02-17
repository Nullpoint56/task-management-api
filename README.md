# Task Management API

A FastAPI application for managing tasks, providing CRUD operations along with smart task suggestions based on task title and completion sequences.

## Repository

Hosted on GitHub:
[https://github.com/Nullpoint56/task-management-api.git](https://github.com/Nullpoint56/task-management-api.git)

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Nullpoint56/task-management-api.git
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate Environment and Install Dependencies:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Install:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application:**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

## Live API Documentation

For detailed API documentation, once the application is running, visit:
- [Swagger UI](http://localhost:8000/docs) for interactive API exploration.
- [ReDoc](http://localhost:8000/redoc) for a detailed API reference.

## Example Requests

### **Create Task**:
```http
POST /tasks/
Content-Type: application/json

{
  "title": "Complete Project Report",
  "description": "Finalize the report details for Project A",
  "due_date": "2023-11-15T12:00:00Z",
  "status": "pending"
}
```

### **Get All Tasks**:
```http
GET /tasks/?skip=0&limit=10
```

### **Update Task**:
```http
PUT /tasks/1
Content-Type: application/json

{
  "title": "Updated Task Title",
  "status": "completed"
}
```

### **Delete Task**:
```http
DELETE /tasks/1
```

### **Get Task Suggestions**:
```http
GET /tasks/suggestions/
```