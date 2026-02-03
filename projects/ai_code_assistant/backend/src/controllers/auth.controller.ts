import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import UserModel, { IUserDocument } from '../models/user.model';
import { ClaudeUtil } from '../utils/claude.util';
import crypto from 'crypto';

// 用户认证控制器
export class AuthController {
  private claudeUtil: ClaudeUtil;
  private jwtSecret: string;
  private jwtExpiresIn: string;

  constructor() {
    this.claudeUtil = new ClaudeUtil();
    this.jwtSecret = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
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

      // 检查邮箱是否已存在
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

      // 验证旧 Token
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

  /**
   * 修改密码
   * PUT /api/auth/change-password
   */
  changePassword = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { currentPassword, newPassword } = req.body;
      const userId = (req as any).userId; // 从认证中间件获取

      // 验证输入
      if (!currentPassword || !newPassword) {
        return res.status(400).json({
          success: false,
          message: '当前密码和新密码是必填的',
        });
      }

      // 查找用户
      const user = await UserModel.findById(userId).select('+password') as IUserDocument;
      if (!user) {
        return res.status(404).json({
          success: false,
          message: '用户不存在',
        });
      }

      // 验证当前密码
      const isPasswordValid = await user.comparePassword(currentPassword);
      if (!isPasswordValid) {
        return res.status(401).json({
          success: false,
          message: '当前密码错误',
        });
      }

      // 更新密码
      user.password = newPassword;
      await user.save();

      // 返回结果
      return res.status(200).json({
        success: true,
        message: '密码修改成功',
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * 忘记密码
   * POST /api/auth/forgot-password
   */
  forgotPassword = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { email } = req.body;

      // 验证输入
      if (!email) {
        return res.status(400).json({
          success: false,
          message: '邮箱是必填的',
        });
      }

      // 查找用户
      const user = await UserModel.findOne({ email });
      if (!user) {
        // 为了安全，不告诉用户邮箱不存在
        return res.status(200).json({
          success: true,
          message: '如果该邮箱存在，重置密码的邮件已发送',
        });
      }

      // 生成重置 Token
      const resetToken = crypto.randomBytes(32).toString('hex');
      const resetExpires = new Date(Date.now() + 3600000); // 1 小时后过期

      // 生成临时密码
      const tempPassword = crypto.randomBytes(8).toString('hex');

      // 更新用户
      user.password = tempPassword;
      user.save();

      // 发送重置密码的邮件（这里只是示例，实际需要邮件服务器）
      // await sendResetPasswordEmail(user.email, tempPassword);

      // 返回结果
      return res.status(200).json({
        success: true,
        message: '重置密码的邮件已发送',
        // 开发环境：返回临时密码（生产环境应该通过邮件发送）
        // tempPassword: tempPassword, // 只在开发环境返回
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * 重置密码
   * POST /api/auth/reset-password
   */
  resetPassword = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { email, tempPassword, newPassword } = req.body;

      // 验证输入
      if (!email || !tempPassword || !newPassword) {
        return res.status(400).json({
          success: false,
          message: '邮箱、临时密码和新密码是必填的',
        });
      }

      // 查找用户
      const user = await UserModel.findOne({ email }).select('+password') as IUserDocument;
      if (!user) {
        return res.status(404).json({
          success: false,
          message: '用户不存在',
        });
      }

      // 验证临时密码
      const isPasswordValid = await user.comparePassword(tempPassword);
      if (!isPasswordValid) {
        return res.status(401).json({
          success: false,
          message: '临时密码错误或已过期',
        });
      }

      // 更新密码
      user.password = newPassword;
      await user.save();

      // 返回结果
      return res.status(200).json({
        success: true,
        message: '密码重置成功',
      });
    } catch (error) {
      next(error);
    }
  };

  /**
   * 获取用户信息
   * GET /api/auth/me
   */
  me = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = (req as any).userId; // 从认证中间件获取

      // 查找用户
      const user = await UserModel.findById(userId);
      if (!user) {
        return res.status(404).json({
          success: false,
          message: '用户不存在',
        });
      }

      // 返回用户信息
      return res.status(200).json({
        success: true,
        data: {
          userId: user._id,
          username: user.username,
          email: user.email,
          createdAt: user.createdAt,
        },
      });
    } catch (error) {
      next(error);
    }
  };
}

export default AuthController;
