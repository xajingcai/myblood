# 个人血压管理仓库

目标：把可追溯的研究证据转为可执行计划，用规范家庭测压验证变化，并检验预测。

## 开始使用
1. 复制 [个人资料模板](data/profile-template.md) 到 private/profile.md 后填写，不知道的保留“未知”。
2. 阅读 [测量流程](protocols/measurement.md)，与医生确认测量安排和个人目标。
3. 按 [记录说明](data/README.md) 新建 private/readings.json（初始内容为 []），保存真实读数。
4. 执行 `python scripts/check.py` 检查记录；执行 `python scripts/report.py` 查看描述性汇总。
5. 补齐资料后，按 [计划模板](plans/current.md) 制定适用于自己的方案。
6. 按 [预测规则](predictions/README.md) 登记预测，再用后续数据检验。

当前状态：个人资料未填写；无真实读数；未制定个体治疗方案；未生成降压预测。

## 导航
- [智能体规则](AGENTS.md)
- [证据索引](evidence/index.md) / [证据卡模板](evidence/template.md)
- [每周复盘](reviews/template.md)
- [预测登记模板](predictions/template.md)
- [维护工作流](workflows/weekly-review.md)

## 本地与 GitHub
远端仓库：https://github.com/xajingcai/myblood 。本仓库不包含个人健康资料和真实读数。
private/ 默认不受 Git 跟踪；计划和复盘也可能包含敏感信息，推送前逐项查看暂存内容，远端使用私有仓库。
个人数据需另行加密备份；.gitignore 不等于加密，也不能撤回已提交的秘密。
不要在没有删除敏感历史的情况下把私有仓库改为公开。

这是辅助记录和共同决策工具，不能代替诊断或医生处方。不为获取基线而推迟必要治疗。
