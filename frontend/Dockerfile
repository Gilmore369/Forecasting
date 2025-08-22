FROM node:20-alpine

# Set working directory for the React application
WORKDIR /app

# Copy only package manifests first to install dependencies.  This
# leverages Docker layer caching so that npm install is not
# re‑executed if only source files change.
COPY package.json ./
COPY package-lock.json* ./

# Install NPM dependencies.  Using --omit=dev prevents installation
# of any development dependencies; create-react-app scaffolds do not
# typically have dev dependencies aside from react-scripts.
RUN npm install --omit=dev

# Copy the rest of the application code into the container
COPY public ./public
COPY src ./src

# Expose port 3000 to the host so that we can access the app
EXPOSE 3000

# Start the development server.  The --host flag allows external
# connections (e.g. from your browser).  The environment variable
# CHOKIDAR_USEPOLLING enables file watching inside a container.
ENV CHOKIDAR_USEPOLLING=true
CMD ["npm", "start"]