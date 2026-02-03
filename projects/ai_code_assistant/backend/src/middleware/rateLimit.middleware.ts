import { Request, Response, NextFunction } from 'express';
import redisClient from '../config/redis.config';

// 限流配置接口
export interface IRateLimitConfig {
  windowMs: number; // 时间窗口（毫秒）
  maxRequests: number; // 最大请求数
  message?: string; // 限流消息
  skipSuccessfulRequests?: boolean; // 跳过成功的请求
  skipFailedRequests?: boolean; // 跳过失败的请求
}

// 限流中间件类
export class RateLimitMiddleware {
  private config: IRateLimitConfig;

  constructor(config?: IRateLimitConfig) {
    this.config = {
      windowMs: 60 * 1000, // 1分钟
      maxRequests: 100, // 100请求/分钟
      message: 'Too many requests, please try again later.',
      skipSuccessfulRequests: false,
      skipFailedRequests: false,
      ...config,
    };
  }

  // 限流中间件
  middleware = async (req: Request, res: Response, next: NextFunction) => {
    try {
      // 如果跳过成功的请求，则继续
      if (this.config.skipSuccessfulRequests && res.statusCode < 400) {
        return next();
      }

      // 如果跳过失败的请求，则继续
      if (this.config.skipFailedRequests && res.statusCode >= 400) {
        return next();
      }

      // 获取用户ID（从JWT Token或Session）
      const userId = (req as any).userId || 'anonymous';

      // 创建限流Key
      const key = `ratelimit:${userId}`;
      
      // 获取当前请求数
      const currentCount = await redisClient.getRateLimit(key) || 0;

      // 检查是否超过限流
      if (currentCount >= this.config.maxRequests) {
        return res.status(429).json({
          success: false,
          message: this.config.message || 'Too many requests, please try again later.',
          data: {
            resetTime: new Date(Date.now() + this.config.windowMs).toISOString(),
            limit: this.config.maxRequests,
            window: this.config.windowMs / 1000, // 秒
          },
        });
      }

      // 增加请求数
      await redisClient.setRateLimit(key, currentCount + 1, Math.floor(this.config.windowMs / 1000));

      // 继续下一个中间件
      next();
    } catch (error) {
      next(error);
    }
  };
}

// 创建限流中间件实例
export const createRateLimitMiddleware = (config?: IRateLimitConfig) => {
  return new RateLimitMiddleware(config || {}).middleware;
};

export default RateLimitMiddleware;
