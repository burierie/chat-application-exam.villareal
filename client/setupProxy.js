import { createProxyMiddleware } from 'http-proxy-middleware';

export default function (app) {
  app.use(
    '/create_room/{roomName}',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
    })
  );

  app.use(
    '/join_room/{roomName}',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
    })
  );
};