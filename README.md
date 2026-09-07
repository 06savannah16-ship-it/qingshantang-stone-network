# 刻石成网：晴山堂 263 年

一个以张书颜 2025 年 5 月 30 日硕士论文终稿和个人整理拓片为基础的数字人文可视化原型。

## 项目内容

- 以 12 件代表性拓片呈现 1370–1632 年间的家族记忆与文人交游。
- 支持按时间、书体、记忆主题切换布局，并按时期、书体、主题、体裁交叉筛选。
- 点击条目可查看高清拓片、人物关系、研究者解读、AI 初步描述与证据状态。
- “文人关系网”把书写者、作品与家族人物／空间放在同一张图中，悬停可追踪关系，点击可查看作品解释。
- 对不确定的日期和书体明确标注“待复核”，不把模型推断当作史实。

## 开源复用

展示层基于 [VIKUS Viewer](https://github.com/cpietsch/vikus-viewer)（MIT License），复用其文化藏品时间布局、主题筛选和高分辨率图像浏览能力。图像预处理使用 [vikus-viewer-script](https://github.com/cpietsch/vikus-viewer-script)（ISC License）。原始开源许可见 `LICENSE.md`，本项目修改说明见 `NOTICE.md`。

## 本地运行

### 最简单的方法（Mac）

双击 `START.command`，然后在浏览器打开 `http://localhost:4173`。关闭终端窗口即可停止预览。

### 命令行方法

直接双击 HTML 无法加载本地 CSV，需要从项目目录启动一个静态服务器：

```bash
python3 -m http.server 4173
```

然后打开 `http://localhost:4173`。

## 重新生成藏品数据

`scripts/build_collection.py` 会从原图目录提取 12 件代表作、统一为 JPEG，并生成 `data/data.csv`、`data/timeline.csv`、`data/network.json` 和 `data/config.json`。完整原始扫描库不包含在公开仓库中；站点只保留 12 件经过压缩的展示图，重新构建时需自行提供源目录。

首次重建前安装图像依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
python3 scripts/build_collection.py \
  --source-dir "/path/to/晴山堂石刻扫描" \
  --extra-dir "/path/to/晴山堂石刻扫描pdf"
```

图像纹理随后由 VIKUS Viewer Script 生成。

若只修改题名、年代、人物关系或说明文字，可跳过原图复制：

```bash
python3 scripts/build_collection.py \
  --source-dir "/path/to/晴山堂石刻扫描" \
  --extra-dir "/path/to/晴山堂石刻扫描pdf" \
  --skip-images
```

日常浏览这个已经生成好的版本不需要安装 Python 图像依赖，也不需要 Node.js。

## 当前边界

这是秋招投递用 MVP，不是完整的晴山堂数据库。当前只使用 12 件代表作，重点展示研究问题、信息架构、视觉呈现与人机协作方法。完整的 76 方石刻与 94 篇作品资料暂不公开。

面试与作品集用的一页项目说明见 `PORTFOLIO_BRIEF.md`。
