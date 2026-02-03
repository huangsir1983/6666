#!/bin/bash

# GitHub 推送测试脚本 v2

echo "=========================================="
echo "GitHub 推送测试 v2"
echo "=========================================="
echo ""

# 配置凭证存储
git config --global credential.helper cache
git config --global credential.cache "cache --timeout=3600"

# 输入凭证（手动）
echo "请输入 GitHub 用户名："
read username
echo ""
echo "请输入 GitHub Token："
read token
echo ""

# 存储凭证
echo "protocol=https
host=github.com
username=$username
password=$token" | git credential-cache store

echo "凭证已存储！"
echo ""

# 尝试推送
echo "尝试推送到 GitHub..."
git push -u origin master

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="
