import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import mongoose from 'mongoose';
import path from 'path';
import fs from 'fs';

// 导入路由
import codeRouter from './routes/code.routes';
import authRouter from './routes/auth.routes.new';

// 导入中间件
import { errorHandler } from './middleware/error.middleware';

// 导入配置
import { connectDB } from './config/database.config';

// 加载环境变量
dotenv.config();

// 创建 Express 应用
const app: Application = express();

// 中间件配置
app.use(helmet()); // 安全头
app.use(cors()); // 跨域资源共享
app.use(express.json()); // JSON 请求解析
app.use(express.urlencoded({ extended: true })); // URL 编码请求解析
app.use(morgan('dev')); // 日志中间件（开发环境）

// 静态文件
const uploadsDir = path.join(__dirname, '..', 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}
app.use('/uploads', express.static(uploadsDir));

// 路由
app.use('/api/code', codeRouter);
app.use('/api/auth', authRouter);

// 健康检查
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    message: 'OpenClaw Code Assistant API is running',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    features: {
      code_generation: true,
      code_explanation: true,
      code_optimization: true,
      code_diagnostics: true,
      user_authentication: true,
      api_rate_limiting: false, // 待实现
      rag_system: false, // 待实现
    },
  });
});

// 根路径
app.get('/', (req: Request, res: Response) => {
  res.json({
    message: 'OpenClaw Code Assistant API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      code: '/api/code',
      auth: '/api/auth',
    },
    documentation: 'https://github.com/huangsir1983/6666',
  });
});

// 404 处理
app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
  });
});

// 错误处理中间件（必须在最后）
app.use(errorHandler);

// 数据库连接
const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/ai-code-assistant';

const startServer = async () => {
  try {
    // 连接数据库
    await connectDB();
    console.log('✅ Database connected successfully');

    // 启动服务器
    app.listen(PORT, () => {
      console.log(`✅ Server is running on port ${PORT}`);
      console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
      console.log(`📊 API Endpoints:`);
      console.log(`   - Health: http://localhost:${PORT}/health`);
      console.log(`   - Code: http://localhost:${PORT}/api/code`);
      console.log(`   - Auth: http://localhost:${PORT}/api/auth`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
};

// 启动服务器
startServer();

export default app;
