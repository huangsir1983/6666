import { Router } from 'express';
import AuthController from '../controllers/auth.controller.new';
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

// 错误处理中间件（必须在最后）
authRouter.use(errorHandler);

export default authRouter;
