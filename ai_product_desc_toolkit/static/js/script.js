// 全局变量
let currentEmailContent = '';

// 页面加载完成
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI 邮件营销工具已加载');
});

// 表单提交
document.getElementById('emailForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // 禁用按钮
    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
    const btnText = document.getElementById('btnText');
    const originalText = btnText.textContent;
    btnText.innerHTML = '⏳ 生成中...';

    // 获取表单数据
    const data = {
        product_name: document.getElementById('productName').value,
        product_features: document.getElementById('productFeatures').value,
        target_audience: document.getElementById('targetAudience').value,
        email_type: document.getElementById('emailType').value,
        tone: document.getElementById('tone').value
    };

    try {
        // 调用 API
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // 显示结果
            showResult(result.content);
        } else {
            alert('生成失败：' + result.error);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }

    // 恢复按钮
    btn.disabled = false;
    btnText.textContent = originalText;
});

// 显示结果
function showResult(content) {
    currentEmailContent = content;
    
    const resultSection = document.getElementById('resultSection');
    const emailContent = document.getElementById('emailContent');
    
    // 解析标题和内容
    const lines = content.split('\n');
    let title = '';
    let body = '';
    let foundBody = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.startsWith('主题：') || line.startsWith('Subject:')) {
            title = line.replace(/^主题：|Subject:/i, '').trim();
        } else if (line.trim() === '') {
            foundBody = true;
        } else if (foundBody) {
            body += line + '\n';
        }
    }

    if (!title) {
        title = '营销邮件';
    }

    document.getElementById('emailTitle').textContent = title;
    emailContent.textContent = body;
    
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 复制邮件
async function copyEmail() {
    const emailContent = document.getElementById('emailContent').textContent;
    const title = document.getElementById('emailTitle').textContent;
    
    const fullEmail = `主题：${title}\n\n${emailContent}`;
    
    try {
        await navigator.clipboard.writeText(fullEmail);
        alert('邮件内容已复制到剪贴板！');
    } catch (err) {
        // 备用方案：使用 textarea 复制
        const textarea = document.createElement('textarea');
        textarea.value = fullEmail;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('邮件内容已复制到剪贴板！');
    }
}

// 清空结果
function clearResult() {
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('emailContent').textContent = '';
    document.getElementById('emailTitle').textContent = '';
    currentEmailContent = '';
}

// 批量生成
async function generateBatch() {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = '⏳ 生成中...';

    const data = {
        product_name: document.getElementById('productName').value,
        product_features: document.getElementById('productFeatures').value,
        target_audiences: document.getElementById('targetAudience').value.split(/[,；]/).map(s => s.trim()).filter(s => s),
        email_type: document.getElementById('emailType').value,
        tone: document.getElementById('tone').value,
        count: parseInt(document.getElementById('batchCount').value)
    };

    try {
        const response = await fetch('/batch_generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showBatchResults(result.emails);
        } else {
            alert('批量生成失败：' + result.error);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }

    btn.disabled = false;
    btn.textContent = originalText;
}

// 显示批量结果
function showBatchResults(emails) {
    const batchSection = document.getElementById('batchSection');
    const batchResults = document.getElementById('batchResults');
    
    batchResults.innerHTML = '';
    
    emails.forEach((email, index) => {
        const item = document.createElement('div');
        item.className = 'batch-item';
        
        const lines = email.content.split('\n');
        let title = '邮件 ' + (index + 1);
        let body = '';
        let foundBody = false;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (line.startsWith('主题：') || line.startsWith('Subject:')) {
                title = line.replace(/^主题：|Subject:/i, '').trim();
            } else if (line.trim() === '') {
                foundBody = true;
            } else if (foundBody) {
                body += line + '\n';
            }
        }

        item.innerHTML = `
            <h4>${title}</h4>
            <pre>${body}</pre>
            <button class="btn btn-secondary" onclick="copyBatchEmail(${index})">📋 复制</button>
        `;
        
        batchResults.appendChild(item);
    });

    batchSection.style.display = 'block';
    batchSection.scrollIntoView({ behavior: 'smooth' });
}

// 复制批量邮件
async function copyBatchEmail(index) {
    const batchResults = document.getElementById('batchResults');
    const items = batchResults.querySelectorAll('.batch-item');
    const item = items[index];
    
    const title = item.querySelector('h4').textContent;
    const body = item.querySelector('pre').textContent;
    
    const fullEmail = `主题：${title}\n\n${body}`;
    
    try {
        await navigator.clipboard.writeText(fullEmail);
        alert(`邮件 ${index + 1} 已复制到剪贴板！`);
    } catch (err) {
        const textarea = document.createElement('textarea');
        textarea.value = fullEmail;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert(`邮件 ${index + 1} 已复制到剪贴板！`);
    }
}

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter：生成
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('emailForm').dispatchEvent(new Event('submit'));
    }
    
    // Ctrl/Cmd + B：批量生成
    if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
        e.preventDefault();
        if (document.getElementById('batchSection').style.display !== 'none') {
            generateBatch();
        }
    }
});

console.log('JavaScript 已加载');
