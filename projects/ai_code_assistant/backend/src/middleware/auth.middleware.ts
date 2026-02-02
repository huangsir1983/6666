import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

dotenv.config();

interface JwtPayload {
  userId: string;
  email: string;
  iat: number;
  exp: number;
}

/**
 * 扩展 Request 接口以包含 user 信息
 */
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
      };
    }
  }
}

/**
 * 认证中间件
 */
export function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  try {
    // 从请求头获取 token
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      res.status(401).json({ error: '访问被拒绝，没有提供 token' });
      return;
    }

    // 验证 token
    const secret = process.env.JWT_SECRET || 'your_jwt_secret_here';
    const decoded = jwt.verify(token, secret) as JwtPayload;

    // 将用户信息添加到请求对象
    req.user = {
      id: decoded.userId,
      email: decoded.email,
    };

    next();
  } catch (error) {
    console.error('❌ Auth middleware error:', error);
    res.status(401).json({ error: '无效的 token' });
  }
}
