#!/bin/bash

# GitHub 推送测试脚本 v2（非交互式）

echo "=========================================="
echo "GitHub 推送测试 v2（非交互式）"
echo "=========================================="
echo ""

# 配置凭证存储
git config --global credential.helper store

# 直接存储凭证
echo "protocol=https
host=github.com
username=huangsir1983
password=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" | git credential-store store

echo "凭证已存储！"
echo ""

# 尝试推送
echo "尝试推送到 GitHub..."
git push -u origin master

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="
