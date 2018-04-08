FROM node:carbon

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run compile

EXPOSE 9009
CMD [ "npm", "start" ]