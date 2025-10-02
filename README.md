# 📝 Django Todo Backend with Firebase Authentication

This is a **learning project** where I built a backend in **Django REST Framework** to understand backend development, authentication, and permission handling.  

The project started from a skeleton backend and was extended to a **fully functioning Todo API** with **Firebase Authentication (OAuth)** and **role-based permissions**.  

It demonstrates:
- Django model design
- RESTful API endpoints
- Authentication & authorization (with Firebase JWTs)
- Role-based access control (admin vs user)
- API documentation _(currently under works)_



## 🚀 Features

- **User Registration**
  - `/register-user/` → Register a normal user (created both in Firebase & local DB).
  - `/register-admin/` → Register an admin user (`is_staff=True` locally).

- **Authentication**
  - Firebase ID tokens validated with a custom DRF authentication class.
  - Protected endpoints require `Authorization: Bearer <idToken>`.

- **User Management**
  - `/users/` → Public endpoint showing all users (without todos).
  - `/users/<id>/` → Private endpoint (owner or admin only).

- **Todo Lists**
  - Authenticated CRUD endpoints.
  - Users can only manage their own lists.
  - Admins can manage all lists.
  - Owner is automatically assigned on creation.

- **Todo Items**
  - Authenticated CRUD endpoints.
  - Users can only access items assigned to them.
  - Admins can manage all items.
  - Users can assign tasks to other users.



## 🔐 Permission Rules

- **Users**
  - Must be authenticated to use TodoList/TodoItem endpoints.
  - Can only CRUD their own resources.
  - Can assign items to others from their own lists.

- **Admins**
  - Can CRUD all TodoLists and TodoItems.
  - Can see all users.

- **Public**
  - `/users/` is publicly available (basic info only).



## ⚙️ Setup Instructions

Before proceeding, make sure you have a [virtual environment](https://docs.python.org/3/library/venv.html) set up and activated. Continue once your virtual environment is **active**.

### 1. Clone and install dependencies
```bash
git clone https://github.com/ShadmanSahil/django-rest-todo
cd django-rest-todo
pip install -r requirements.txt
```

### 2. FireBase setup

- Create a Firebase project and enable Email/Password authentication.
- Generate a service account key (JSON).
- Load the credentials in firebase.py.
- Or configure environment variables for cleaner secrets management.

### Run migrations and server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Authentication in Postman

Since Firebase issues JWT ID tokens, you need to log in to Firebase first to get a token.

Use a pre-request script in Postman to sign in:

```code
const postRequest = {
  url: 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + pm.variables.get('API_KEY'),
  method: 'POST',
  header: { 'Content-Type': 'application/json' },
  body: {
    mode: 'raw',
    raw: JSON.stringify({
      email: pm.variables.get('AUTH_EMAIL'),
      password: pm.variables.get('AUTH_PASSWORD'),
      returnSecureToken: true
    })
  }
};

pm.sendRequest(postRequest, (error, response) => {
  const json = response.json();
  pm.variables.set('AUTH_TOKEN', json.idToken);
});
```

Then add this header to protected requests:
```code
Authorization: Bearer {{AUTH_TOKEN}}
```

## 📚 API Overview

### Users
- POST /register-user/ → Register normal user
- POST /register-admin/ → Register admin
- GET /users/ → Public, list users
- GET /users/<id>/ → Private, view specific user

### TodoLists

- GET /list/ → User’s own lists (admins see all)
- POST /list/ → Create a list
- PUT /list/<id>/ → Update list
- DELETE /list/<id>/ → Delete list

### Todo Items
- `GET /item/` → Items assigned to user (admins see all)  
- `POST /item/` → Create item in own list  
- `PUT /item/<id>/` → Update item  
- `DELETE /item/<id>/` → Delete item

🚧 A complete **Postman collection** is under works and will be provided shortly.



## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Auth**: Firebase Authentication (JWT validation via Firebase Admin SDK)  
- **Database**: SQLite (easy to swap for Postgres/MySQL)  
- **Docs/Testing**: DRF Spectacular & Postman  



## ✨ Learning Goals

This project was built to **learn backend development with Django** while integrating **real-world authentication flows** using Firebase.  

Key takeaways:
- Designing secure REST APIs  
- Handling role-based permissions  
- Bridging external identity providers (Firebase) with local DB models  
- API testing automation in Postman

---

### Get in Touch!

👋🏽 [Say Hi!](https://www.linkedin.com/in/shadmansahil/)



