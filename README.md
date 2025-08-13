# Easy CheckIn

A web-based attendance tracking system designed to work on both tablets and desktop computers. This application allows students to mark their attendance when they arrive at class using a kiosk interface, and provides instructors and administrators with tools to manage students, classes, and view attendance reports.

## Features

- **Responsive Design**: Works on both tablets and desktop computers
- **Kiosk Mode**: Easy-to-use interface for students to mark attendance
- **User Management**: Admin can create instructor and admin accounts
- **Student Management**: Add, edit, and view student information
- **Class Management**: Create and manage dance classes with schedules
- **Attendance Tracking**: Record and view student attendance
- **Reporting**: Generate attendance reports by class and date range

## Tech Stack

- **Backend**: Python with Flask framework
- **Database**: SQLite (default) with option to use PostgreSQL
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Containerization**: Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning the repository)

## Installation and Setup

### Using Docker Compose (Recommended)

1. Clone or download this repository:
   ```
   git clone <repository-url>
   cd dance-attendance-app
   ```

2. Build and start the containers:
   ```
   docker-compose up -d
   ```

3. Access the application at `http://localhost:5000`

### Manual Setup (Development)

1. Clone or download this repository:
   ```
   git clone <repository-url>
   cd dance-attendance-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export SECRET_KEY=your_secret_key
   ```

5. Run the application:
   ```
   flask run
   ```

6. Access the application at `http://localhost:5000`

## Initial Setup

When you first run the application, you'll need to create an admin user. You can do this by running:

```
docker-compose exec web flask create-admin
```

Or, if running locally:

```
flask create-admin
```

This will prompt you to create an admin username and password.

## Usage

### Student Attendance

1. Students access the application on a tablet or computer set up in kiosk mode
2. They select their class from the home screen
3. They find their name in the list and tap/click the "Check In" button

### Administrator/Instructor

1. Log in using the admin/instructor credentials
2. Access the dashboard to manage students, classes, and view reports
3. Add new students and classes as needed
4. Generate attendance reports by class and date range

## Customization

### Using PostgreSQL Instead of SQLite

1. Uncomment the PostgreSQL section in `docker-compose.yml`
2. Update the `DATABASE_URL` environment variable in `docker-compose.yml`
3. Rebuild the containers:
   ```
   docker-compose down
   docker-compose up -d
   ```

### Changing the Secret Key

For production use, change the `SECRET_KEY` environment variable in `docker-compose.yml` to a secure random string.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Flask and its extensions
- Bootstrap 5
- Font Awesome
