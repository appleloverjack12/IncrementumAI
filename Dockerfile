FROM node:20-slim

WORKDIR /app

COPY package.json ./

RUN npm install --ignore-scripts

RUN cd node_modules/bun && node install.js || true

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npx", "elizaos", "start"]