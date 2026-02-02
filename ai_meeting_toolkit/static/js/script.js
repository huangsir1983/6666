// AI 会议记录总结工具 - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('AI 会议记录总结工具已加载');
});

document.getElementById('meetingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const btn = document.getElementById('summarizeBtn');
    btn.disabled = true;
    const btnText = document.getElementById('btnText');
    const originalText = btnText.textContent;
    btnText.innerHTML = '⏳ 生成中...';

    const data = {
        meeting_content: document.getElementById('meetingContent').value,
        summary_type: document.getElementById('summaryType').value,
        output_format: document.getElementById('outputFormat').value
    };

    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showResult(result.summary);
        } else {
            alert('生成失败：' + result.error);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }

    btn.disabled = false;
    btnText.textContent = originalText;
});

function showResult(content) {
    const resultSection = document.getElementById('resultSection');
    const summaryContent = document.getElementById('summaryContent');
    summaryContent.textContent = content;
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function copySummary() {
    const content = document.getElementById('summaryContent').textContent;
    navigator.clipboard.writeText(content).then(() => {
        alert('总结内容已复制到剪贴板！');
    });
}

function clearResult() {
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('summaryContent').textContent = '';
    document.getElementById('actionSection').style.display = 'none';
    document.getElementById('actionItems').innerHTML = '';
}

async function extractActionItems() {
    const meetingContent = document.getElementById('meetingContent').value;
    
    try {
        const response = await fetch('/action_items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ meeting_content: meetingContent })
        });

        const result = await response.json();

        if (result.action_items) {
            showActionItems(result.action_items);
        } else {
            alert('提取失败：' + result.error);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }
}

function showActionItems(items) {
    const actionSection = document.getElementById('actionSection');
    const actionItemsDiv = document.getElementById('actionItems');
    
    actionItemsDiv.innerHTML = '';
    items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'action-item';
        itemDiv.innerHTML = `<strong>任务：</strong> ${item.task}<br><strong>负责人：</strong> ${item.owner}<br><strong>截止日期：</strong> ${item.deadline}<br><strong>优先级：</strong> ${item.priority}`;
        actionItemsDiv.appendChild(itemDiv);
    });
    
    actionSection.style.display = 'block';
    actionSection.scrollIntoView({ behavior: 'smooth' });
}

async function exportActionItems() {
    const items = document.getElementById('actionItems').querySelectorAll('.action-item');
    const text = Array.from(items).map(item => item.innerText).join('\n\n');
    
    navigator.clipboard.writeText(text).then(() => {
        alert('行动项已导出到剪贴板！');
    });
}

async function generateBatch() {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = '⏳ 生成中...';

    const data = {
        meeting_content: document.getElementById('meetingContent').value,
        summary_types: document.getElementById('summaryTypes').value.split(',').map(s => s.trim())
    };

    try {
        const response = await fetch('/batch_summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showBatchResults(result.summaries);
        } else {
            alert('批量生成失败：' + result.error);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }

    btn.disabled = false;
    btn.textContent = originalText;
}

function showBatchResults(summaries) {
    const batchSection = document.getElementById('batchSection');
    const batchResults = document.getElementById('batchResults');
    
    batchResults.innerHTML = '';
    summaries.forEach((summary, index) => {
        const div = document.createElement('div');
        div.className = 'batch-item';
        div.innerHTML = `
            <h4>总结 ${summary.id} - ${summary.type}</h4>
            <pre>${summary.content}</pre>
            <button class="btn btn-secondary" onclick="copySummary(${index})">📋 复制</button>
        `;
        batchResults.appendChild(div);
    });

    batchSection.style.display = 'block';
    batchSection.scrollIntoView({ behavior: 'smooth' });
}

console.log('JavaScript 已加载');
