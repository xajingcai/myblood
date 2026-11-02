# 原始记录格式

真实记录放在 private/readings.json，顶层是数组。下面仅为格式示意，不能复制为真实测量：

```json
{
  "timestamp": "2026-11-02T07:00:00+08:00",
  "session_id": "2026-11-02-am",
  "period": "morning",
  "reading_index": 1,
  "systolic": 128,
  "diastolic": 78,
  "pulse": 68,
  "included": true,
  "exclusion_reason": "",
  "notes": "示意数据，不是真实读数；记录休息、手臂、症状、服药时间等"
}
```

单位：血压 mmHg，心率 次/分。period 使用 morning/evening/other。
同一测量时段 session_id 相同，两次 reading_index 分别1、2，时间为实际测量时间。
异常读数保留原值；included=false 时填写具体排除理由。不要仅因读数高而排除。
附加症状、测量条件、近期用药和生活变化。可增加字段，检查器不删除字段。
汇总使用本地日期：先按时段求均值，再按日期求均值，最后各天等权；不等于所有读数混合平均。
