import { Router } from 'express';
import AuthController from '../controllers/auth.controller';
import { authMiddleware } from '../middleware/auth.middleware';
import { errorHandler } from '../middleware/error.middleware';

// 创建认证路由
const authRouter = Router();
const authController = new AuthController();

// 用户注册
authRouter.post('/register', authController.register);

// 用户登录
authRouter.post('/login', authController.login);

// 验证 Token
authRouter.post('/verify', authController.verify);

// 刷新 Token
authRouter.post('/refresh', authController.refresh);

// 修改密码（需要认证）
authRouter.put('/change-password', authMiddleware, authController.changePassword);

// 忘记密码
authRouter.post('/forgot-password', authController.forgotPassword);

// 重置密码
authRouter.post('/reset-password', authController.resetPassword);

// 获取用户信息（需要认证）
authRouter.get('/me', authMiddleware, authController.me);

// 错误处理中间件
authRouter.use(errorHandler);

export default authRouter;
