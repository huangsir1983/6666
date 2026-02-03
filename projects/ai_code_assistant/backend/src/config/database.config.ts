import mongoose from 'mongoose';
import winston from 'winston';

// 创建日志记录器
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.simple(),
    }),
  ],
});

// 数据库配置
export const connectDB = async (): Promise<void> => {
  try {
    const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/ai-code-assistant';
    const MONGODB_URI_PRODUCTION = process.env.MONGODB_URI_PRODUCTION;

    // 连接数据库（生产环境优先）
    const uri = MONGODB_URI_PRODUCTION || MONGODB_URI;

    await mongoose.connect(uri, {
      maxPoolSize: 10,
      minPoolSize: 2,
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
    });

    logger.info('✅ Database connected successfully');
  } catch (error) {
    logger.error('❌ Database connection error:', error);
    process.exit(1);
  }
};

// 数据库关闭
export const disconnectDB = async (): Promise<void> => {
  try {
    await mongoose.disconnect();
    logger.info('✅ Database disconnected successfully');
  } catch (error) {
    logger.error('❌ Database disconnection error:', error);
    process.exit(1);
  }
};

// 数据库错误处理
mongoose.connection.on('error', (error) => {
  logger.error('❌ Database connection error:', error);
});

mongoose.connection.on('disconnected', () => {
  logger.warn('⚠️  Database disconnected');
});

mongoose.connection.on('reconnected', () => {
  logger.info('✅ Database reconnected successfully');
});
