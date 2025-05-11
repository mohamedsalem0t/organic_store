# Organic Store Project

Welcome to the Organic Store Project! This project is a full-stack web application built using **Django** for the backend and **React** for the frontend. It allows users to browse products, view categories, and perform various interactions with the system.

## Features

- **User Authentication**: Register, login, and manage user sessions.
- **Category Listing**: Display a list of product categories.
- **Product Search**: Ability to search products in the store.
- **Responsive Design**: Optimized for both desktop and mobile views.
- **API Integration**: The frontend fetches data from the Django REST API.

## Technologies Used

- **Backend**: 
  - Django
  - Django REST Framework
  - SQLite (Database)
- **Frontend**: 
  - React
  - Axios (for API requests)
  - React Router (for routing)
- **Authentication**: JWT (JSON Web Tokens)

## Project Structure

### Backend

- **Django Project**: Contains the API and authentication system.
- **Django Models**: Includes models for `Category`, `Product`, and others.
- **API**: Exposes endpoints for the categories and products, handled by Django REST Framework.
- **Authentication**: JWT-based login and registration functionality.

### Frontend

- **React App**: Renders the user interface with functionality like category listing, product display, and search.
- **Components**:
  - `Header`: Displays the top navigation bar with search functionality.
  - `HomePage`: Displays categories and the welcome message.
  - `Login`, `Register`: User authentication pages.

## Installation

### Backend Setup (Django)

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/mohamedsalem0t/organic_store.git
    cd organic_store/backend
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows use venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Start the Server**:
    ```bash
    python manage.py runserver
    ```
    This will start the backend server on `http://localhost:8000`.

### Frontend Setup (React)

1. **Navigate to the frontend directory**:
    ```bash
    cd ../frontend
    ```

2. **Install Dependencies**:
    ```bash
    npm install
    ```

3. **Start the Development Server**:
    ```bash
    npm start
    ```

    This will start the React app on `http://localhost:3000`.

### Environment Configuration

For local development, you can modify the backend API URL in the frontend code (in `HomePage.js`, `axios.get('http://localhost:8000/api/categories/')`) to match the backend URL if needed.

## Usage

- **HomePage**: Displays a list of categories with their names and descriptions.
- **Login**: User login page with validation.
- **Register**: User registration page.
- **Search**: Users can search for products in the top navigation bar.
- **Category Detail**: Clicking a category will redirect users to that category's page.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-xyz`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push your changes (`git push origin feature-xyz`).
5. Open a pull request to merge your changes into the main repository.

## License

This project is licensed under the MIT License.

## GitHub Repository

You can find the full project code and updates on the official GitHub repository:

[GitHub Repository: Organic Store](https://github.com/mohamedsalem0t/organic_store)
