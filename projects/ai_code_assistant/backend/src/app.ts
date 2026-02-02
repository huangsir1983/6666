import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import codeRoutes from './routes/code.routes';
import { errorMiddleware } from './middleware/error.middleware';

dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(helmet()); // 安全头
app.use(cors()); // CORS
app.use(morgan('dev')); // 日志
app.use(express.json()); // 解析 JSON
app.use(express.urlencoded({ extended: true })); // 解析 URL 编码

// 健康检查
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    message: 'OpenClaw Code Assistant API is running',
    timestamp: new Date().toISOString(),
  });
});

// API 路由
app.use('/api/v1/code', codeRoutes);

// 错误处理
app.use(errorMiddleware);

// 404 处理
app.use((req: Request, res: Response) => {
  res.status(404).json({ error: '路由不存在' });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 OpenClaw Code Assistant API is running on port ${PORT}`);
  console.log(`📝 Health check: http://localhost:${PORT}/health`);
  console.log(`📚 API docs: http://localhost:${PORT}/api/v1/code`);
});

export default app;
