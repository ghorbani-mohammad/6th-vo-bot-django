# Base image
FROM python:3.11.5

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y ca-certificates curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
      | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" \
      > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Install npm dependencies and build assets
# RUN npm install && \
#     npm run build && \
#     npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css
RUN npm install --save-dev babel-loader @babel/core @babel/preset-env @babel/preset-react mini-css-extract-plugin css-loader postcss-loader css-minimizer-webpack-plugin webpack webpack-cli webpack-dev-server
RUN npm install
RUN npm run build
RUN npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css

# Collect static files (skip if handled during deployment)
RUN python manage.py collectstatic --no-input

# Run the application with Gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
