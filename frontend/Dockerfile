FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy app
COPY . .

# Build app
RUN npm run build

# Expose port
EXPOSE 3000

# Run preview server
CMD ["npm", "run", "preview"]
