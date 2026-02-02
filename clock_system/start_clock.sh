#!/bin/bash
#
# ⏰ 内部时钟系统 - 一键启动脚本
#

echo "======================================"
echo "⏰  内部时钟系统 - 一键启动"
echo "======================================"
echo ""

# 第一步：验证时钟脚本
echo "📋 第一步：验证时钟脚本..."
cd /root/.openclaw/workspace
python3 clock_system/clock_system_verify.py

if [ $? -eq 0 ]; then
    echo "   ✅ 验证成功"
else
    echo "   ❌ 验证失败，请检查日志"
    exit 1
fi

echo ""
echo "⏱️  等待 2 秒..."
sleep 2

# 第二步：停止旧的服务（如果存在）
echo ""
echo "📋 第二步：停止旧的服务（如果存在）..."

systemctl is-active --quiet clock_system.service
if [ $? -eq 0 ]; then
    echo "   服务正在运行，准备停止..."
    systemctl stop clock_system.service
    echo "   ✅ 服务已停止"
else
    echo "   服务未运行，跳过停止"
fi

echo ""
echo "⏱️  等待 2 秒..."
sleep 2

# 第三步：安装服务文件
echo ""
echo "📋 第三步：安装 Systemd 服务文件..."

cp clock_system/clock_system.service /etc/systemd/system/
systemctl daemon-reload

if [ $? -eq 0 ]; then
    echo "   ✅ 服务文件安装成功"
    echo "   ✅ Systemd 已重新加载"
else
    echo "   ❌ 服务文件安装失败"
    exit 1
fi

echo ""
echo "⏱️  等待 2 秒..."
sleep 2

# 第四步：启动服务
echo ""
echo "📋 第四步：启动 Systemd 服务..."

systemctl start clock_system.service
systemctl enable clock_system.service

if [ $? -eq 0 ]; then
    echo "   ✅ 服务启动成功"
    echo "   ✅ 服务已设置为开机自启"
else
    echo "   ❌ 服务启动失败，请检查日志"
    exit 1
fi

echo ""
echo "⏱️  等待 5 秒，让服务启动..."
sleep 5

# 第五步：验证服务状态
echo ""
echo "📋 第五步：验证服务状态..."

systemctl is-active --quiet clock_system.service
if [ $? -eq 0 ]; then
    echo "   ✅ 服务正在运行"
    systemctl status clock_system.service
else
    echo "   ❌ 服务未运行"
    exit 1
fi

echo ""
echo "📊 第六步：查看服务日志..."

journalctl -u clock_system -n 20 --no-pager

echo ""
echo "======================================"
echo "⏰  内部时钟系统启动成功！"
echo "======================================"
echo ""

echo "📋 服务信息："
echo "   服务名称：clock_system.service"
echo "   服务状态：运行中"
echo "   时区：GMT+8 (Beijing)"
echo "   同步间隔：1 小时"
echo ""

echo "📊 时钟日志："
echo "   日志文件：clock_system/clock_log.txt"
echo "   时钟数据：clock_system/clock_data.json"
echo ""

echo "🔍 查看服务状态："
echo "   systemctl status clock_system.service"
echo ""

echo "📄 查看服务日志："
echo "   journalctl -u clock_system -f"
echo ""

echo "⏱️  查看时钟数据："
echo "   cat clock_system/clock_data.json"
echo ""

echo "⏰  下次同步时间："
echo "   服务启动后 1 小时"
echo ""

echo "💡 提示："
echo "   1. 服务已在后台自动运行"
echo "   2. 每小时自动同步一次时间"
echo "   3. 可以使用上面的命令查看状态和日志"
echo "   4. 时钟会与格林威治时间（GMT）同步"
echo "   5. 时钟数据会保存在 clock_system/clock_data.json"
echo ""

echo "🛑  停止服务："
echo "   systemctl stop clock_system.service"
echo ""

echo "🚀 重启服务："
echo "   systemctl restart clock_system.service"
echo ""

echo "======================================"
echo "✅ 启动完成！"
echo "======================================"
echo ""

echo "📞 现在时钟系统已在后台自动运行！"
echo ""
echo "⏰  每小时自动同步一次时间！"
echo ""
echo "⏱️  下次同步：服务启动后 1 小时"
