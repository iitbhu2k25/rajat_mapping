# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app
RUN pip install --upgrade pip

# Copy the project files to the container
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install dependencies
COPY . .


# Expose the port Django runs on
EXPOSE 8000

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
