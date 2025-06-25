# Assembly to C Decompiler Webapp (Django)

This is a Django-based web frontend for converting assembly code to C code. The current version displays a fixed C output for demonstration. In the future, it can be extended to call a backend or LLM for real decompilation.

## Features
- Modern, responsive web UI (no JavaScript frameworks required)
- Assembly code input field (editable)
- C output field (read-only, always visible)
- No database or user data required for core functionality

## Requirements
- Python 3.10+
- pip
- Django 5.x

## Setup Instructions

1. **Clone the repository or copy the project files.**

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Apply Django migrations (required for built-in features):**

   ```sh
   python manage.py migrate
   ```

4. **Run the development server:**

   ```sh
   python manage.py runserver
   ```

5. **Open your browser and go to:**
   [http://localhost:8000/decompile/](http://localhost:8000/decompile/)

## File Structure
- `assembly/` — Django app with views, templates, and static files
- `assembly_to_c/` — Django project settings and URLs
- `requirements.txt` — Python dependencies

## Future Implementation: Connecting to a Backend/LLM
To connect the frontend to a backend or LLM for real decompilation:
1. Replace the fixed C output in `assembly/views.py` with a call to your backend API or LLM model.
2. You can use Python's `requests` library or Django's `http` utilities to make HTTP requests to your backend.
3. Update the view to display the response from the backend in the C output field.

Example (pseudo-code):
```python
import requests
# ...
if request.method == 'POST':
    assembly_code = request.POST.get('assembly_code', '')
    response = requests.post('http://your-backend/api/decompile', json={'assembly': assembly_code})
    c_output = response.json().get('c_code', '')
```

## Notes
- The app does not require a database for its main function, but Django needs one for built-in features (sessions, admin, etc.).
- The default SQLite database is used for convenience.

## TODO
[ ] add .env file for environment variables
[ ] add section to query both models