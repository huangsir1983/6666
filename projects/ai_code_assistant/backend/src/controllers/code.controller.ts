import { Request, Response } from 'express';
import { generateCode, explainCode, optimizeCode, diagnoseError } from '../utils/claude.util';
import pool from '../config/database.config';

/**
 * 代码生成控制器
 */
export async function generateCodeController(
  req: Request,
  res: Response
): Promise<void> {
  try {
    const { requirement, language, context } = req.body;
    const userId = (req as any).user.id;

    // 验证输入
    if (!requirement || !language) {
      res.status(400).json({ error: '需求描述和编程语言是必需的' });
      return;
    }

    // 调用 AI 生成代码
    const result = await generateCode(requirement, language, context);

    // 保存到数据库
    await pool.query(
      `INSERT INTO code_history (user_id, code_type, input_data, output_data, language)
       VALUES ($1, 'generate', $2, $3, $4)`,
      [
        userId,
        JSON.stringify({ requirement, language, context }),
        JSON.stringify(result),
        language,
      ]
    );

    res.json({
      id: Date.now().toString(),
      code: result.code,
      explanation: result.explanation,
      language,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('❌ Generate code error:', error);
    res.status(500).json({ error: '代码生成失败' });
  }
}

/**
 * 代码解释控制器
 */
export async function explainCodeController(
  req: Request,
  res: Response
): Promise<void> {
  try {
    const { code, language } = req.body;
    const userId = (req as any).user.id;

    // 验证输入
    if (!code || !language) {
      res.status(400).json({ error: '代码和编程语言是必需的' });
      return;
    }

    // 调用 AI 解释代码
    const result = await explainCode(code, language);

    // 保存到数据库
    await pool.query(
      `INSERT INTO code_history (user_id, code_type, input_data, output_data, language)
       VALUES ($1, 'explain', $2, $3, $4)`,
      [
        userId,
        JSON.stringify({ code, language }),
        JSON.stringify(result),
        language,
      ]
    );

    res.json({
      id: Date.now().toString(),
      explanation: result.explanation,
      keyPoints: result.keyPoints,
      bestPractices: result.bestPractices,
      language,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('❌ Explain code error:', error);
    res.status(500).json({ error: '代码解释失败' });
  }
}

/**
 * 代码优化控制器
 */
export async function optimizeCodeController(
  req: Request,
  res: Response
): Promise<void> {
  try {
    const { code, language, optimizationGoals } = req.body;
    const userId = (req as any).user.id;

    // 验证输入
    if (!code || !language) {
      res.status(400).json({ error: '代码和编程语言是必需的' });
      return;
    }

    // 调用 AI 优化代码
    const result = await optimizeCode(code, language, optimizationGoals);

    // 保存到数据库
    await pool.query(
      `INSERT INTO code_history (user_id, code_type, input_data, output_data, language)
       VALUES ($1, 'optimize', $2, $3, $4)`,
      [
        userId,
        JSON.stringify({ code, language, optimizationGoals }),
        JSON.stringify(result),
        language,
      ]
    );

    res.json({
      id: Date.now().toString(),
      originalCode: code,
      optimizedCode: result.optimizedCode,
      improvements: result.improvements,
      performanceDiff: result.performanceDiff,
      language,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('❌ Optimize code error:', error);
    res.status(500).json({ error: '代码优化失败' });
  }
}

/**
 * 错误诊断控制器
 */
export async function diagnoseErrorController(
  req: Request,
  res: Response
): Promise<void> {
  try {
    const { code, errorMessage, language } = req.body;
    const userId = (req as any).user.id;

    // 验证输入
    if (!code || !errorMessage || !language) {
      res.status(400).json({ error: '代码、错误信息和编程语言是必需的' });
      return;
    }

    // 调用 AI 诊断错误
    const result = await diagnoseError(code, errorMessage, language);

    // 保存到数据库
    await pool.query(
      `INSERT INTO code_history (user_id, code_type, input_data, output_data, language)
       VALUES ($1, 'diagnose', $2, $3, $4)`,
      [
        userId,
        JSON.stringify({ code, errorMessage, language }),
        JSON.stringify(result),
        language,
      ]
    );

    res.json({
      id: Date.now().toString(),
      errorType: result.errorType,
      errorCause: result.errorCause,
      fixSuggestion: result.fixSuggestion,
      fixedCode: result.fixedCode,
      preventionTips: result.preventionTips,
      language,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('❌ Diagnose error:', error);
    res.status(500).json({ error: '错误诊断失败' });
  }
}
