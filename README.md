# Mailing Service

## Description
Mailing Service is a Django-based application that allows users to manage and send email campaigns. It includes features for creating messages, managing recipients, scheduling mailings, and tracking mailing attempts.

## Features
- Create and manage email messages
- Manage email recipients
- Schedule mailings
- Track mailing attempts
- User authentication and authorization

## Installation

### Prerequisites
- Python >=3.11
- PostgreSQL
- Redis
- Django >=5.0

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/mailing-service.git
    cd mailing-service
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_HOST=your_database_host
    DATABASE_PORT=your_database_port
    EMAIL_HOST=your_email_host
    EMAIL_USE_TLS=True
    EMAIL_PORT=your_email_port
    EMAIL_HOST_USER=your_email_user
    EMAIL_HOST_PASSWORD=your_email_password
    ```

4. Apply database migrations:
    ```sh
    poetry run python manage.py migrate
    ```

5. Create a superuser (You can use custom command provided):
    ```sh
    python manage.py createadmin
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

7. Create managers group by running the following command:
    ```sh
    python manage.py create_managers_group
    ```

## Configuration
- **Email settings:** Update the email settings in `settings.py` to enable email verification and password reset functionalities.
- **Cache settings:** Configure Redis or any other caching backend in `settings.py` if you want to enable caching.

## Usage
1. Access the admin panel at `http://127.0.0.1:8000/admin` and log in with your superuser credentials.
2. Create messages and manage recipients.
3. Schedule mailings and track their status.
4. Supported sending emails via custom command:
    ```sh
    python manage.py send_mail "Title of the message" --recipients user1@example.com user2@example.com --message your message
    ```
5. You can schedule the mailing by using django-apscheduler using following command:
   ```sh
    python manage.py start_scheduler
    ```
