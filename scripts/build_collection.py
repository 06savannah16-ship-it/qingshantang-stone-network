#!/usr/bin/env python3
"""Prepare the curated Qingshan Hall rubbing collection for VIKUS Viewer."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image, ImageOps


ITEMS = [
    {
        "id": "001",
        "filename": "倪瓒 题《本中书室图》  整.jpg",
        "year": 1370,
        "date": "洪武三年（1370）",
        "title": "题《本中书室图》",
        "creator": "倪瓒",
        "recipient": "徐麒（字本中）",
        "period": "明早期",
        "script": "行楷（待复核）",
        "genre": "题诗",
        "theme": "家族记忆",
        "relationship": "父辈旧交题赠少年徐麒",
        "human_note": "原画已佚，题字经刻石与拓本保存下来；它把一件消失的书画转化为徐氏家族记忆的起点。",
        "confidence": "日期明确；书体标签待研究者复核",
    },
    {
        "id": "002",
        "filename": "解缙 詩 題心遠先生喻蜀歸圖•南州信義世皆知.JPG",
        "year": 1405,
        "date": "明早期（暂置约 1405）",
        "title": "题心远先生喻蜀归图",
        "creator": "解缙",
        "recipient": "徐麒（号心远）",
        "period": "明早期",
        "script": "行书（待复核）",
        "genre": "题诗",
        "theme": "功业与归隐",
        "relationship": "文人题赠徐麒奉使归乡",
        "human_note": "与徐麒奉使西蜀、功成归隐的家族叙事相连，题赠把个人经历转化为可传承的公共声望。",
        "confidence": "事件与人物明确；具体作年待考",
    },
    {
        "id": "003",
        "filename": "沈度 詩 題退庵•幽居俯寥廓 .jpg",
        "year": 1425,
        "date": "明早期（暂置约 1425）",
        "title": "题退庵",
        "creator": "沈度",
        "recipient": "徐忞（号退庵）",
        "period": "明早期",
        "script": "楷书（待复核）",
        "genre": "题诗",
        "theme": "义民与隐居",
        "relationship": "名士题赠徐氏第二代文化空间",
        "human_note": "‘退庵’与徐氏不逐仕进、读书修身的家族形象相连，是空间命名参与身份建构的例子。",
        "confidence": "人物关系明确；具体作年待考",
    },
    {
        "id": "004",
        "filename": "明 王直 敕书楼赞.JPG",
        "source_group": "extra",
        "year": 1440,
        "date": "正统年间（1436—1449，暂置 1440）",
        "title": "敕书楼赞",
        "creator": "王直",
        "recipient": "徐忞",
        "period": "明早期",
        "script": "楷书（待复核）",
        "genre": "赞",
        "theme": "君恩与义民",
        "relationship": "朝廷旌表之后的名士题赞",
        "human_note": "敕书楼把赈灾义举、国家认可与家族空间连接起来，是徐氏声望形成的重要节点。",
        "confidence": "正统年间及事件关系由终稿明确；具体作年待考",
    },
    {
        "id": "005",
        "filename": "李東陽 銘 明故中書舍人徐君（頤）菇志銘（文壁重錄） 完整版.jpg",
        "year": 1510,
        "date": "正德庚午（1510）",
        "title": "明故中书舍人徐君墓志铭",
        "creator": "李东阳撰、文徵明书",
        "recipient": "徐颐",
        "period": "明中期",
        "script": "小楷",
        "genre": "墓志铭",
        "theme": "家族记忆",
        "relationship": "名臣撰文与吴门书家重录",
        "human_note": "撰文与书写由不同名士完成，说明石刻既保存文本，也物化了徐氏与文化精英之间的协作网络。",
        "confidence": "日期与书体由论文明确",
    },
    {
        "id": "006",
        "filename": "文壁 赞 《内翰徐公像赞》 完整版.JPG",
        "year": 1509,
        "date": "约正德四年（1509）",
        "title": "内翰徐公像赞",
        "creator": "文徵明",
        "recipient": "徐颐",
        "period": "明中期",
        "script": "隶书",
        "genre": "像赞",
        "theme": "肖像与身份",
        "relationship": "吴门书家为徐氏先人作像赞",
        "human_note": "这是法帖中少见的隶书作品，为观察文徵明早期书风和明代隶体提供了独特样本。",
        "confidence": "书体与作者年龄由论文明确",
    },
    {
        "id": "007",
        "filename": "祝允明 赞 中翰徐公赞 完整版.jpg",
        "year": 1515,
        "date": "正德十年仲春既望（1515 年农历二月二十六日）",
        "title": "中翰徐公赞",
        "creator": "祝允明",
        "recipient": "徐颐",
        "period": "明中期",
        "script": "小楷",
        "genre": "赞",
        "theme": "肖像与身份",
        "relationship": "吴门书家为徐氏先人题赞",
        "human_note": "作品位于祝允明小楷持续成熟的阶段，提按、转折与欹正关系构成重要的视觉观察线索。",
        "confidence": "日期与书体明确；对象据终稿同章谱系表述核为徐颐",
    },
    {
        "id": "008",
        "filename": "陈继儒 叙 寿江阴徐太君王孺人八十叙 1.JPG",
        "year": 1624,
        "date": "天启四年（1624）",
        "title": "寿江阴徐太君王孺人八十叙",
        "creator": "陈继儒",
        "recipient": "王孺人",
        "period": "明晚期",
        "script": "行书",
        "genre": "寿叙",
        "theme": "母仪与纪念",
        "relationship": "王孺人八十寿辰的文人题赠",
        "human_note": "围绕王孺人寿辰形成的集中创作，把家庭纪念转化为跨地域的文人共同书写。",
        "confidence": "事件年份与书体由论文明确",
    },
    {
        "id": "009",
        "filename": "高攀龙 完整版.jpg",
        "year": 1624,
        "date": "天启四年（1624）",
        "title": "题《秋圃晨机图》诗（“吾闻东海有贤母”）",
        "creator": "高攀龙",
        "recipient": "王孺人、徐霞客",
        "period": "明晚期",
        "script": "行书（待复核）",
        "genre": "题画诗",
        "theme": "母仪与东林交游",
        "relationship": "东林领袖参与徐母寿辰题赠",
        "human_note": "原画已失，题诗成为东林人物与徐氏交往的物证，也让女性家族记忆留在男性文人网络之中。",
        "confidence": "事件、诗文开篇与东林交游由终稿明确；书体待复核",
    },
    {
        "id": "010",
        "filename": "董其昌 墓铭 明故徐豫庵隐君暨配王孺人合葬墓志铭  1.jpg",
        "year": 1625,
        "date": "天启五年（1625）",
        "title": "明故徐豫庵隐君暨配王孺人合葬墓志铭",
        "creator": "董其昌",
        "recipient": "徐有勉、王孺人",
        "period": "明晚期",
        "script": "行楷",
        "genre": "墓志铭",
        "theme": "父母纪念",
        "relationship": "徐霞客远行求书于董其昌",
        "human_note": "徐霞客‘匍匐五百里’求得此作，书写行为本身成为孝道、名家声望与家族纪念的连接点。",
        "confidence": "年份、书体与求书经过由论文明确",
    },
    {
        "id": "011",
        "filename": "明•陳仁錫 晴山堂記.JPG",
        "source_group": "extra",
        "year": 1624,
        "date": "天启四年寿辰语境（1624，暂置）",
        "title": "晴山堂记",
        "creator": "陈仁锡",
        "recipient": "晴山堂、徐氏家族",
        "period": "明晚期",
        "script": "行书（待复核）",
        "genre": "记",
        "theme": "空间与传承",
        "relationship": "友人为家族纪念空间作记",
        "human_note": "‘人亡而不亡者石，石忘而不忘者文’概括了晴山堂以材料保存记忆的核心逻辑。",
        "confidence": "文本、作者与王孺人八十寿辰语境明确；具体作年、书体待复核",
    },
    {
        "id": "012",
        "filename": "黄道周 诗 灯下依韵和徐振之诗 1.jpg",
        "year": 1632,
        "date": "崇祯五年（1632）",
        "title": "灯下依韵和徐振之诗（“野水笑人旷”）",
        "creator": "黄道周",
        "recipient": "徐霞客",
        "period": "明晚期",
        "script": "行草（待复核）",
        "genre": "唱和诗",
        "theme": "知己与唱和",
        "relationship": "黄道周与徐霞客诗文唱和",
        "human_note": "作为现存序列中最晚的作品之一，它将家族题赠传统收束到徐霞客本人的知己交往。",
        "confidence": "年份、唱和关系与诗组线索由终稿明确；书体待复核",
    },
]


TIMELINE = [
    (1370, "家族记忆的起点", "倪瓒为十岁的徐麒题《本中书室图》。", "原画后来失佚，题字经刻石与拓本保存。"),
    (1440, "明初题赠网络形成", "徐麒、徐忞两代获得名士题赠。", "正统年间的赈灾旌表、义民身份与敕书楼共同塑造徐氏声望；具体年份暂置。"),
    (1510, "吴门书家进入收藏", "李东阳、文徵明、祝允明等参与撰写与书录。", "晴山堂中期作品见证家族向科举与士大夫文化靠近。"),
    (1624, "王孺人八十寿辰", "《秋圃晨机图》引发二十余位名士题咏。", "家庭纪念扩展为晚明文人共同创作。"),
    (1625, "父母纪念", "徐霞客求董其昌书合葬墓志铭。", "名家书写、远行求索与孝道叙事汇合。"),
    (1632, "法帖序列收束", "黄道周与徐霞客的唱和成为晚期代表。", "从六代家族记忆转向徐霞客个人的知己网络。"),
]


def build(source_dir: Path, extra_dir: Path, output_dir: Path, skip_images: bool = False) -> None:
    data_dir = output_dir / "data"
    source_out = output_dir / "source-images"
    data_dir.mkdir(parents=True, exist_ok=True)
    source_out.mkdir(parents=True, exist_ok=True)

    rows = []
    for item in ITEMS:
        if not skip_images:
            origin = (extra_dir if item.get("source_group") == "extra" else source_dir) / item["filename"]
            if not origin.exists():
                raise FileNotFoundError(origin)
            destination = source_out / f"{item['id']}.jpg"
            with Image.open(origin) as image:
                image = ImageOps.exif_transpose(image).convert("RGB")
                image.save(destination, "JPEG", quality=94, optimize=True)
        keywords = ",".join([
            item["period"], item["script"].replace("（待复核）", ""), item["genre"],
            item["theme"], item["creator"].split("、")[0]
        ])
        rows.append({
            "keywords": keywords,
            "year": item["year"],
            "_title": item["title"],
            "_creator": item["creator"],
            "_date": item["date"],
            "_recipient": item["recipient"],
            "_period": item["period"],
            "_script": item["script"],
            "_genre": item["genre"],
            "_theme": item["theme"],
            "_relationship": item["relationship"],
            "_human_note": item["human_note"],
            "_confidence": item["confidence"],
            "_source": "张书颜硕士论文 2025 年 5 月 30 日终稿及个人整理的晴山堂拓片图像",
            "id": item["id"],
        })

    with (data_dir / "data.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with (data_dir / "timeline.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["year", "title", "text", "extra"],
            lineterminator="\n",
        )
        writer.writeheader()
        for year, title, text, extra in TIMELINE:
            writer.writerow({"year": year, "title": title, "text": text, "extra": extra})

    config = {
        "project": {"name": "刻石成网：晴山堂 263 年", "quality": 1},
        "searchEnabled": True,
        "sortKeywords": ["明早期", "明中期", "明晚期", "家族记忆", "母仪与纪念", "母仪与东林交游", "父母纪念", "知己与唱和", "小楷", "隶书", "行书", "行楷", "行草"],
        "loader": {
            "info": "data/info.md",
            "timeline": "data/timeline.csv",
            "items": "data/data.csv",
            "layouts": [
                {"title": "时间", "type": "group", "groupKey": "year", "columns": 1},
                {"title": "书体", "type": "group", "groupKey": "_script", "columns": 1},
                {"title": "记忆主题", "type": "group", "groupKey": "_theme", "columns": 1},
            ],
            "textures": {
                "medium": {"size": 128, "url": "data/sprites/spritesheet.json"},
                "detail": {"size": 1024, "url": "data/1024/"},
                "big": {"size": 4096, "url": "data/4096/"},
            },
        },
        "style": {
            "fontColor": "#2d2a26",
            "fontColorActive": "#f3eee2",
            "fontBackground": "#8e2f25",
            "textShadow": "1px 1px 0px #eee7d8",
            "canvasBackground": "#d9d2c2",
            "timelineBackground": "#f3eee2",
            "timelineFontColor": "#2d2a26",
            "backgroundHeader": "#1d1c1a",
            "fontColorHeader": "#c46a57",
            "detailBackground": "#f1ecdf",
            "infoBackground": "#23211e",
            "infoFontColor": "#f3eee2",
            "searchbarBackground": "#8e2f25",
        },
        "projection": {"columns": 1},
        "filter": {
            "type": "crossfilter",
            "dimensions": [
                {"label": "时期", "source": "_period"},
                {"label": "书体", "source": "_script"},
                {"label": "主题", "source": "_theme"},
                {"label": "体裁", "source": "_genre"},
            ],
        },
        "detail": {
            "structure": [
                {"name": "作品", "source": "_title", "display": "wide", "type": "text"},
                {"name": "作者", "source": "_creator", "display": "column", "type": "text"},
                {"name": "年代", "source": "_date", "display": "column", "type": "text"},
                {"name": "书体", "source": "_script", "display": "column", "type": "text"},
                {"name": "对象", "source": "_recipient", "display": "column", "type": "text"},
                {"name": "关系", "source": "_relationship", "display": "wide", "type": "text"},
                {"name": "研究者解读", "source": "_human_note", "display": "wide", "type": "text"},
                {"name": "证据状态", "source": "_confidence", "display": "wide", "type": "text"},
                {"name": "资料来源", "source": "_source", "display": "wide", "type": "text"},
            ]
        },
    }
    (data_dir / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    info = """# 刻石成网：晴山堂 263 年

从 1370 年倪瓒为徐麒题写《本中书室图》，到 1632 年黄道周与徐霞客唱和，晴山堂石刻把六代家族记忆与晚明文人交游压进石面。

本次最小展览从 76 方现存石刻、88 位名士的 94 篇作品中选择 12 件代表作。你可以切换“时间 / 书体 / 记忆主题”，也可以按时期、书体、主题和体裁筛选。点击拓片查看高清细节与研究注释。

终稿附表将 94 篇作品分为明早期 37 篇、明中期 13 篇、明晚期 44 篇；书体包括小楷 31 篇、行书 55 篇、草书 7 篇、隶书 1 篇。公开原型只呈现其中的策展样本，不等同于完整数据库。

## 研究范围

数据与解释以张书颜硕士论文《家族记忆与文人交游——晴山堂石刻的艺术价值与文化传承》2025 年 5 月 30 日终稿（中国美术学院）为准，并结合个人整理的拓片图像。公开版本只展示代表性条目，不公开完整论文数据库。
"""
    (data_dir / "info.md").write_text(info, encoding="utf-8")

    network = {
        "works": [
            {
                "id": item["id"],
                "title": item["title"],
                "year": item["year"],
                "date": item["date"],
                "creator": item["creator"],
                "recipient": item["recipient"],
                "relationship": item["relationship"],
                "theme": item["theme"],
                "human_note": item["human_note"],
                "confidence": item["confidence"],
                "image": f"data/1024/{item['id']}.jpg",
            }
            for item in ITEMS
        ]
    }
    (data_dir / "network.json").write_text(
        json.dumps(network, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--extra-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="只重建 CSV/JSON/说明文件，不重新复制原始图像。",
    )
    args = parser.parse_args()
    build(args.source_dir, args.extra_dir, args.output_dir, skip_images=args.skip_images)


if __name__ == "__main__":
    main()
