import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import UserModel, { IUserDocument } from '../models/user.model';
import crypto from 'crypto';

// 用户认证控制器
export class AuthController {
  private jwtSecret: string;
  private jwtExpiresIn: string;

  constructor() {
    this.jwtSecret = process.env.JWT_SECRET || 'your-secret-key-change-in-production-use-uuid-or-random-string';
    this.jwtExpiresIn = process.env.JWT_EXPIRES_IN || '7d';
  }

  /**
   * 用户注册
   * POST /api/auth/register
   */
  register = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { username, email, password } = req.body;

      // 验证输入
      if (!username || !email || !password) {
        return res.status(400).json({
          success: false,
          message: '用户名、邮箱和密码是必填的',
        });
      }

      // 检查用户名是否已存在
      const existingUser = await UserModel.findOne({ username });
      if (existingUser) {
        return res.status(400).json({
          success: false,
          message: '用户名已存在',
        });
      }

      // 检查邮箱是否已注册
      const existingEmail = await UserModel.findOne({ email });
      if (existingEmail) {
        return res.status(400).json({
          success: false,
          message: '邮箱已被注册',
        });
      }

      // 创建新用户
      const newUser = await UserModel.create({
        username,
        email,
        password, // 将会被 bcrypt 自动加密
      });

      // 生成 JWT Token
      const token = jwt.sign(
        { userId: newUser._id, username: newUser.username },
        this.jwtSecret,
        { expiresIn: this.jwtExpiresIn }
      );

      // 返回注册结果
      return res.status(201).json({
        success: true,
        message: '注册成功',
        data: {
          userId: newUser._id,
          username: newUser.username,
          email: newUser.email,
          token,
        },
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * 用户登录
   * POST /api/auth/login
   */
  login = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { email, password } = req.body;

      // 验证输入
      if (!email || !password) {
        return res.status(400).json({
          success: false,
          message: '邮箱和密码是必填的',
        });
      }

      // 查找用户
      const user = await UserModel.findOne({ email }).select('+password') as IUserDocument;
      if (!user) {
        return res.status(401).json({
          success: false,
          message: '邮箱或密码错误',
        });
      }

      // 验证密码
      const isPasswordValid = await user.comparePassword(password);
      if (!isPasswordValid) {
        return res.status(401).json({
          success: false,
          message: '邮箱或密码错误',
        });
      }

      // 生成 JWT Token
      const token = jwt.sign(
        { userId: user._id, username: user.username },
        this.jwtSecret,
        { expiresIn: this.jwtExpiresIn }
      );

      // 返回登录结果
      return res.status(200).json({
        success: true,
        message: '登录成功',
        data: {
          userId: user._id,
          username: user.username,
          email: user.email,
          token,
        },
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * 验证 Token
   * POST /api/auth/verify
   */
  verify = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { token } = req.body;

      // 验证输入
      if (!token) {
        return res.status(400).json({
          success: false,
          message: 'Token 是必填的',
        });
      }

      // 验证 Token
      const decoded = jwt.verify(token, this.jwtSecret) as { userId: string; username: string };

      // 查找用户
      const user = await UserModel.findById(decoded.userId);
      if (!user) {
        return res.status(401).json({
          success: false,
          message: 'Token 无效',
        });
      }

      // 返回验证结果
      return res.status(200).json({
        success: true,
        message: 'Token 有效',
        data: {
          userId: user._id,
          username: user.username,
          email: user.email,
          token,
        },
      });
    } catch (error) {
      if (error instanceof jwt.TokenExpiredError) {
        return res.status(401).json({
          success: false,
          message: 'Token 已过期',
        });
      } else if (error instanceof jwt.JsonWebTokenError) {
        return res.status(401).json({
          success: false,
          message: 'Token 无效',
        });
      } else {
        next(error);
      }
    }
  };

  /**
   * 刷新 Token
   * POST /api/auth/refresh
   */
  refresh = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { token } = req.body;

      // 验证输入
      if (!token) {
        return res.status(400).json({
          success: false,
          message: 'Token 是必填的',
        });
      }

      // 验证旧 Token（忽略过期）
      const decoded = jwt.verify(token, this.jwtSecret, { ignoreExpiration: true }) as { userId: string; username: string };

      // 查找用户
      const user = await UserModel.findById(decoded.userId);
      if (!user) {
        return res.status(401).json({
          success: false,
          message: 'Token 无效',
        });
      }

      // 生成新 Token
      const newToken = jwt.sign(
        { userId: user._id, username: user.username },
        this.jwtSecret,
        { expiresIn: this.jwtExpiresIn }
      );

      // 返回刷新结果
      return res.status(200).json({
        success: true,
        message: 'Token 刷新成功',
        data: {
          userId: user._id,
          username: user.username,
          email: user.email,
          token: newToken,
        },
      });
    } catch (error) {
      next(error);
    }
  };
}

export default AuthController;
