import { Router } from 'express';
import {
  generateCodeController,
  explainCodeController,
  optimizeCodeController,
  diagnoseErrorController,
} from '../controllers/code.controller';
import { authMiddleware } from '../middleware/auth.middleware';

const router = Router();

// 所有代码相关的路由都需要认证
router.use(authMiddleware);

/**
 * @route   POST /api/v1/code/generate
 * @desc    生成代码
 * @access  Private
 */
router.post('/generate', generateCodeController);

/**
 * @route   POST /api/v1/code/explain
 * @desc    解释代码
 * @access  Private
 */
router.post('/explain', explainCodeController);

/**
 * @route   POST /api/v1/code/optimize
 * @desc    优化代码
 * @access  Private
 */
router.post('/optimize', optimizeCodeController);

/**
 * @route   POST /api/v1/code/diagnose
 * @desc    诊断错误
 * @access  Private
 */
router.post('/diagnose', diagnoseErrorController);

export default router;
