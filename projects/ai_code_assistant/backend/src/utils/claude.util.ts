import axios from 'axios';
import claudeConfig from '../config/claude.config';

interface ClaudeMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ClaudeResponse {
  id: string;
  type: string;
  content: Array<{
    type: string;
    text: string;
  }>;
  model: string;
  stop_reason: string;
}

/**
 * 调用 Claude API
 */
export async function callClaudeAPI(messages: ClaudeMessage[]): Promise<ClaudeResponse> {
  try {
    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      {
        model: claudeConfig.model,
        max_tokens: claudeConfig.maxTokens,
        temperature: claudeConfig.temperature,
        messages,
      },
      {
        headers: {
          'x-api-key': claudeConfig.apiKey,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error('❌ Claude API error:', error);
    throw new Error('Failed to call Claude API');
  }
}

/**
 * 生成代码
 */
export async function generateCode(
  requirement: string,
  language: string,
  context?: string
): Promise<{ code: string; explanation: string }> {
  const messages: ClaudeMessage[] = [
    {
      role: 'user',
      content: `请用 ${language} 编写代码，满足以下需求：

需求：${requirement}

${context ? `上下文：${context}` : ''}

请返回：
1. 完整的代码
2. 代码的简要说明

请以以下格式返回：
\`\`\`代码
// 代码内容
\`\`\`

说明：代码的简要说明`,
    },
  ];

  const response = await callClaudeAPI(messages);

  // 解析响应
  const content = response.content[0].text;

  // 提取代码和说明
  const codeMatch = content.match(/```(?:[\w]*)\n([\s\S]*?)\n```/);
  const code = codeMatch ? codeMatch[1].trim() : '';

  const explanationMatch = content.match(/说明：(.*)/s);
  const explanation = explanationMatch ? explanationMatch[1].trim() : '代码已生成。';

  return { code, explanation };
}

/**
 * 解释代码
 */
export async function explainCode(
  code: string,
  language: string
): Promise<{
  explanation: string;
  keyPoints: string[];
  bestPractices: string[];
}> {
  const messages: ClaudeMessage[] = [
    {
      role: 'user',
      content: `请解释以下 ${language} 代码：

\`\`\`${language}
${code}
\`\`\`

请提供：
1. 代码的整体功能说明
2. 关键点（3-5 个）
3. 最佳实践建议（3-5 个）

请以以下格式返回：
整体功能说明：[说明]

关键点：
1. [点1]
2. [点2]
...

最佳实践：
1. [实践1]
2. [实践2]
...`,
    },
  ];

  const response = await callClaudeAPI(messages);
  const content = response.content[0].text;

  // 解析响应
  const explanationMatch = content.match(/整体功能说明：(.*)/s);
  const explanation = explanationMatch ? explanationMatch[1].trim() : '代码已解释。';

  const keyPointsMatch = content.match(/关键点：([\s\S]*?)(?=\n最佳实践：|$)/s);
  const keyPoints = keyPointsMatch
    ? keyPointsMatch[1]
        .trim()
        .split('\n')
        .filter((line) => line.trim())
        .map((line) => line.replace(/^\d+\.\s*/, '').trim())
    : [];

  const bestPracticesMatch = content.match(/最佳实践：([\s\S]*?)$/s);
  const bestPractices = bestPracticesMatch
    ? bestPracticesMatch[1]
        .trim()
        .split('\n')
        .filter((line) => line.trim())
        .map((line) => line.replace(/^\d+\.\s*/, '').trim())
    : [];

  return { explanation, keyPoints, bestPractices };
}

/**
 * 优化代码
 */
export async function optimizeCode(
  code: string,
  language: string,
  optimizationGoals: string[] = ['性能', '可读性']
): Promise<{
  optimizedCode: string;
  improvements: string[];
  performanceDiff?: {
    timeComplexity: string;
    spaceComplexity: string;
  };
}> {
  const messages: ClaudeMessage[] = [
    {
      role: 'user',
      content: `请优化以下 ${language} 代码，优化目标：${optimizationGoals.join('、')}：

\`\`\`${language}
${code}
\`\`\`

请提供：
1. 优化后的代码
2. 改进点（3-5 个）
3. 如果可能，提供时间复杂度和空间复杂度的对比

请以以下格式返回：
\`\`\`优化后的代码
// 代码内容
\`\`\`

改进点：
1. [改进1]
2. [改进2]
...

复杂度对比：
时间复杂度：[原复杂度] → [新复杂度]
空间复杂度：[原复杂度] → [新复杂度]`,
    },
  ];

  const response = await callClaudeAPI(messages);
  const content = response.content[0].text;

  // 解析响应
  const codeMatch = content.match(/```(?:[\w]*)\n([\s\S]*?)\n```/);
  const optimizedCode = codeMatch ? codeMatch[1].trim() : '';

  const improvementsMatch = content.match(/改进点：([\s\S]*?)(?=\n复杂度对比：|$)/s);
  const improvements = improvementsMatch
    ? improvementsMatch[1]
        .trim()
        .split('\n')
        .filter((line) => line.trim())
        .map((line) => line.replace(/^\d+\.\s*/, '').trim())
    : [];

  const performanceDiffMatch = content.match(/复杂度对比：([\s\S]*?)$/s);
  let performanceDiff;
  if (performanceDiffMatch) {
    const timeComplexityMatch = performanceDiffMatch[1].match(/时间复杂度：(.*)/);
    const spaceComplexityMatch = performanceDiffMatch[1].match(/空间复杂度：(.*)/);
    performanceDiff = {
      timeComplexity: timeComplexityMatch ? timeComplexityMatch[1].trim() : '',
      spaceComplexity: spaceComplexityMatch ? spaceComplexityMatch[1].trim() : '',
    };
  }

  return { optimizedCode, improvements, performanceDiff };
}

/**
 * 诊断错误
 */
export async function diagnoseError(
  code: string,
  errorMessage: string,
  language: string
): Promise<{
  errorType: string;
  errorCause: string;
  fixSuggestion: string;
  fixedCode?: string;
  preventionTips: string[];
}> {
  const messages: ClaudeMessage[] = [
    {
      role: 'user',
      content: `请诊断以下 ${language} 代码错误：

\`\`\`${language}
${code}
\`\`\`

错误信息：${errorMessage}

请提供：
1. 错误类型
2. 错误原因
3. 修复建议
4. 如果可能，提供修复后的代码
5. 预防措施（3-5 个）

请以以下格式返回：
错误类型：[类型]

错误原因：[原因]

修复建议：[建议]

修复后的代码：
\`\`\`${language}
// 代码内容
\`\`\`

预防措施：
1. [措施1]
2. [措施2]
...`,
    },
  ];

  const response = await callClaudeAPI(messages);
  const content = response.content[0].text;

  // 解析响应
  const errorTypeMatch = content.match(/错误类型：(.*)/);
  const errorType = errorTypeMatch ? errorTypeMatch[1].trim() : '';

  const errorCauseMatch = content.match(/错误原因：([\s\S]*?)(?=\n修复建议：|$)/s);
  const errorCause = errorCauseMatch ? errorCauseMatch[1].trim() : '';

  const fixSuggestionMatch = content.match(/修复建议：([\s\S]*?)(?=\n修复后的代码：|$)/s);
  const fixSuggestion = fixSuggestionMatch ? fixSuggestionMatch[1].trim() : '';

  const fixedCodeMatch = content.match(/修复后的代码：\s*\n```(?:[\w]*)\n([\s\S]*?)\n```/);
  const fixedCode = fixedCodeMatch ? fixedCodeMatch[1].trim() : undefined;

  const preventionTipsMatch = content.match(/预防措施：([\s\S]*?)$/s);
  const preventionTips = preventionTipsMatch
    ? preventionTipsMatch[1]
        .trim()
        .split('\n')
        .filter((line) => line.trim())
        .map((line) => line.replace(/^\d+\.\s*/, '').trim())
    : [];

  return { errorType, errorCause, fixSuggestion, fixedCode, preventionTips };
}
