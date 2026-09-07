#!/bin/zsh
cd "${0:A:h}"
echo "刻石成网已启动：请在浏览器打开 http://localhost:4173"
echo "关闭这个窗口即可停止预览。"
python3 -m http.server 4173
