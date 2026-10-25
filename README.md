# 主日28 · 基督在他的筵席上丰丰富富地喂养我们的灵魂

2026-10-24 · v1.0.0 · GTser

| 链接 | 地址 |
| --- | --- |
| GitHub Pages | https://08-ser-gt-je-personal-20261003.github.io/lord-day28-feast-20261024-v1-GTser/ |
| Surge | https://lord-day28-feast-20261024-v1-gtser.surge.sh/ |
| 源码仓库 | https://github.com/08-Ser-GT-Je-Personal-20261003/lord-day28-feast-20261024-v1-GTser |

## 内容

原创欧陆改革宗讲章，按“喂养的信息、方式、吩咐”展开；含历史与上下文、逐段释经、救赎历史与圣约脉络、三经比较、14组讨论与答案、复习自测。六份认信原典来源统一为CCI，三经另有干净阅读与背诵页。原典库不是原创译文。

## 运行与维护

Python 3；安装 `requests beautifulsoup4`，运行 `python build.py`。构建会从CCI在线复核本讲引用章节；网络或原文差异会导致构建停止，防止静默替换。`python -m http.server 4188 -d dist` 预览。直接发布 `dist/`，无运行时依赖、无密钥、无数据库。

源码内容为 `content.html`；构建逻辑 `build.py`；认信规范快照 `confessions.json`；样式与交互位于 `dist/style.css`、`dist/app.js`，原创SVG在 `dist/assets/`。首次构建复用项目参考资料，独立仓库后续构建读取本仓库的 `confessions.json`。

GitHub Pages由工作流发布dist。Surge手动部署dist至上表域名。账号凭据不得写入源码、README或日志。

## 原文与验证

原文快照日期2026-10-17；本讲直接引用的三经、海德堡75–77、比利时35、多特第五项14于2026-10-25在线比对，记录在 `dist/source-verification.json`。原文词语标点不修改，版面空白单独处理。其余原典章节不宣称当天重抓。完整范围按CCI收录，不补其他译本结语。版本名日期保留起稿日2026-10-24，发布核验日期另见deployment.json。

浏览器验证见 `qa/report.json`；部署最终验证见 `deployment.json`。历史推断与经文明言分开；原创地图非比例、非考古复原。圣诗编号按用户原大纲保留，未猜测未指定诗本歌词。

所有原创讲解、图示可作为学习资料；认信译文权利归相关权利人，不对第三方译文附加本项目许可证。
