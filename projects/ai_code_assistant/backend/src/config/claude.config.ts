import dotenv from 'dotenv';

dotenv.config();

export const claudeConfig = {
  apiKey: process.env.CLAUDE_API_KEY || '',
  model: process.env.CLAUDE_MODEL || 'claude-3-5-sonnet-20241022',
  maxTokens: 4096,
  temperature: 0.7,
};

// 验证配置
if (!claudeConfig.apiKey) {
  console.warn('⚠️  CLAUDE_API_KEY is not set. AI features will not work.');
}

export default claudeConfig;
