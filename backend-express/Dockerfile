FROM node:20-alpine

# Instalar herramientas necesarias para compilar librerías nativas como argon2
RUN apk add --no-cache python3 make g++

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
