FROM node AS builder
COPY . .
RUN npm install
RUN npm run build

FROM nginx:alpine
COPY --from=builder ./build /usr/share/nginx/html
