# Django LabA

These instructions will guide you through setting up your project locally. To get a local copy up and running follow these simple steps.

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.11 installed on your machine
- pip (Python package manager)
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/malinanu/labela_backend_assignment.git
cd labela_backend_assignment
```
##
2.  **Set up a Python virtual environment** 
```bash
python -m venv venv
```

3.  **On Windows, activate the virtual environment with:**
```bash
.\venv\Scripts\activate
```

4.  **On Unix or MacOS, activate the virtual environment with:**

```bash
source venv/bin/activate
```


5.  **Install the requirements**
```bash
pip install -r requirements.txt
```
6.  **Apply the migrations**
```bash
python manage.py migrate
```

7.  **Create a superuser account for Django admin**

```bash
python manage.py createsuperuser
```
8.  **To run the Django development server**
```bash
python manage.py runserver
````






