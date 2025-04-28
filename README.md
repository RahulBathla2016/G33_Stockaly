# Stockaly

**Stockaly** is a simple yet powerful inventory management application built using **Django**.
It helps users easily manage and track their stock levels, deliveries, and suppliers.

---

## Features
- User authentication (login/logout)
- Add, update, and delete stock items
- Manage suppliers
- Track stock quantities
- Dashboard overview for stock status
- Clean and responsive UI

---

## Getting Started

Follow these steps to run Stockaly on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stockaly.git
cd stockaly
```

> Replace `your-username` with your GitHub username if needed.

---

### 2. Create and Activate a Virtual Environment

#### For Windows:
```bash
python -m venv env
env\Scripts\activate
```

#### For macOS/Linux:
```bash
python3 -m venv env
source env/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory (same level as `manage.py`) and add necessary environment variables such as:

```bash
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> You can generate a Django secret key using [this tool](https://djecrety.ir/).

---

### 5. Apply Migrations

```bash
python manage.py migrate
```

---

### 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompt to create an admin user.

---

### 7. Run the Development Server

```bash
python manage.py runserver
```

Now visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the application.

---

## Folder Structure

```
stockaly/
│
├── stockaly/           # Django project settings (project level)
├── inventory/          # App for managing inventory
├── suppliers/          # App for managing suppliers
├── manage.py
├── db.sqlite3
```

---

## Tech Stack

- **Backend:** Django 4.x
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (default Django DB)

---

## Contributing

Feel free to fork this repository and contribute by submitting a pull request. 🚀

---

## License

This project is licensed under the [MIT License].

"# G33_Stockaly" 
