# 🗺️ 旅行内容配置指南

## 📋 概述

本指南介绍如何为不同的旅行页面配置个性化的行程内容，实现优雅的内容区别化。

---

## 🎯 设计理念

### 配置驱动
通过 `tripConfig.js` 集中管理所有旅行页面的内容配置，无需修改Vue组件代码。

### 结构化数据
使用结构化的数据格式，让内容易于维护和扩展。

### 自动渲染
Vue组件自动读取配置并渲染，保证所有页面样式统一。

---

## 📝 配置文件位置

```
cetapp/web/src/config/tripConfig.js
```

---

## 🔧 配置结构

### 完整配置示例（⭐ 最新版）

```javascript
{
  trip: {
    // 基础信息
    title: '2025年厦门旅行计划',
    backgroundColor: '#f0e68c',
    dates: {
      start: '2025-06-22',
      end: '2025-06-24'
    },
    icon: '🏖️',
    
    // 行程概览配置 ⭐
    overview: {
      // 0. 基本信息（可选，新增⭐）
      basicInfo: {
        participants: 'J.Grigg 和 Leo_Winston',  // 旅行人员
        departure: '南昌',                        // 出发地
        destination: '厦门',                      // 目的地
        transport: '高铁往返（221元×2）',        // 交通方式
        accommodation: '南枫云居酒店',            // 住宿信息
        duration: '3天2夜',                       // 行程时长
        budget: '约2200元/人',                    // 总体预算
        theme: '海滨+文化+美食'                   // 旅行主题
      },
      
      // 1. 行程亮点（数组）
      highlights: [
        '🏝️ 厦门植物园 - 热带雨林奇观，傍晚光线柔和',
        '🌊 鼓浪屿 - 文艺岛屿，海上花园漫步',
        '🏖️ 曾厝垵 - 文艺小店探秘，体验海滨慢生活',
        '🚴 环岛路 - 海边骑行，欣赏无敌海景'
      ],
      
      // 2. 行程安排（数组，增强版⭐）
      itinerary: [
        { 
          day: '第一天（6月22日）',                       // 天数标识
          time: '14:04抵达',                              // 时间点（新增⭐）
          content: '14:04抵达厦门北站 → 入住酒店 → 16:00-18:00厦门植物园 → 晚餐海鲜',  // 详细内容
          highlight: '🌿 植物园环境优美，适合拍照'      // 当日亮点（新增⭐）
        },
        { 
          day: '第二天（6月23日）', 
          time: '05:21日出',
          content: '4:20起床看日出 → 09:00-13:00鼓浪屿 → 14:30-17:30八市+中山路',
          highlight: '🏝️ 鼓浪屿文艺岛屿；🛍️ 八市烟火气浓厚'
        },
        { 
          day: '第三天（6月24日）',
          time: '15:54返程',
          content: '上午鸿山公园 → 南普陀寺 → 午餐 → 15:54高铁返程',
          highlight: '🏯 普陀寺体验佛教文化'
        }
      ],
      
      // 3. 预算参考（对象）
      budget: {
        items: [
          { name: '往返高铁', amount: 442, note: '南昌-厦门 221×2' },
          { name: '景点门票', amount: 120, note: '学生票' },
          { name: '地铁+市内交通', amount: 100, note: '含地铁、短打车' },
          { name: '住宿', amount: 800, note: '南枫云居2晚' },
          { name: '餐饮', amount: 600, note: '特色海鲜+小吃' },
          { name: '其他消费', amount: 138, note: '零食、纪念品' }
        ],
        total: 2200
      },
      
      // 4. 实用提示（可选，新增⭐）
      tips: [
        '📸 最佳拍照时间：早晚光线柔和',
        '🌅 日出时间05:21，建议4:20起床',
        '🎫 提前购买学生票，节省费用',
        '🏖️ 提前预定靠近植物园的酒店',
        '🍜 必尝：沙茶面、海蛎煎、花生汤'
      ]
    }
  }
}
```

---

## 📖 字段说明

### 0. 基本信息 (basicInfo) ⭐ 新增

**类型**: `Object` (可选)

**说明**: 旅行的基本信息，以卡片形式展示，字段全部可选

**支持字段**:
```javascript
basicInfo: {
  participants: String,   // 旅行人员
  departure: String,      // 出发地
  destination: String,    // 目的地
  transport: String,      // 交通方式
  accommodation: String,  // 住宿信息
  duration: String,       // 行程时长
  budget: String,         // 总体预算
  theme: String,          // 旅行主题
  departureTime: String,  // 出发时间
  returnTime: String,     // 返程时间
  // ...可根据需要添加自定义字段
}
```

**示例**:
```javascript
basicInfo: {
  participants: 'J.Grigg 和 Leo_Winston',
  departure: '南昌',
  destination: '厦门',
  transport: '高铁往返（221元×2）',
  accommodation: '南枫云居酒店（近植物园，2晚）'
}
```

**渲染效果**:
- 网格布局，自适应列数
- 每项显示为独立卡片
- Emoji图标 + 标签 + 内容
- 移动端单列显示

---

### 1. 行程亮点 (highlights)

**类型**: `Array<String>`

**说明**: 旅行的核心亮点，每条以 Emoji + 标题 + 简介 格式呈现

**格式建议**:
```javascript
'🏝️ 景点名称 - 简短描述'
```

**示例**:
```javascript
highlights: [
  '🏝️ 厦门植物园 - 热带雨林奇观',
  '🌊 鼓浪屿 - 海上花园漫步',
  '🏖️ 曾厝垵 - 文艺小店探秘'
]
```

**渲染效果**:
- 左侧蓝色边框卡片
- 悬停时有动画效果
- 自动换行

---

### 2. 行程安排 (itinerary) ⭐ 增强版

**类型**: `Array<Object>`

**对象结构**:
```javascript
{
  day: String,         // 时间标签（第一天、上午、Day 1等）
  time: String,        // 时间点（新增⭐，可选）
  content: String,     // 行程内容（详细）
  highlight: String    // 当日亮点（新增⭐，可选）
}
```

**示例（基础版）**:
```javascript
itinerary: [
  { day: '第一天', content: '厦门植物园 → 鼓浪屿' },
  { day: '第二天', content: '曾厝垵 → 环岛路' }
]
```

**示例（增强版⭐ 推荐）**:
```javascript
itinerary: [
  { 
    day: '第一天（6月22日）', 
    time: '14:04抵达',
    content: '14:04抵达厦门北站 → 入住酒店 → 16:00-18:00厦门植物园 → 晚餐海鲜',
    highlight: '🌿 植物园环境优美，适合拍照'
  },
  { 
    day: '第二天（6月23日）', 
    time: '05:21日出',
    content: '4:20起床看日出 → 09:00-13:00鼓浪屿 → 14:30-17:30八市+中山路',
    highlight: '🏝️ 鼓浪屿文艺岛屿；🛍️ 八市烟火气浓厚'
  }
]
```

**渲染效果**:
- 独立卡片样式，带阴影
- 标题栏显示day和time
- 内容详细，支持长文本
- highlight以蓝色高亮框显示
- 悬停时卡片上浮动画

**灵活用法**:

一日游：
```javascript
itinerary: [
  { day: '上午', content: '出发前往景区' },
  { day: '中午', content: '野餐午餐' },
  { day: '下午', content: '返程' }
]
```

多日游：
```javascript
itinerary: [
  { day: 'Day 1', content: 'Arrival → Check-in → City Tour' },
  { day: 'Day 2', content: 'Beach → Seafood → Sunset' },
  { day: 'Day 3', content: 'Temple → University → Departure' }
]
```

---

### 3. 预算参考 (budget)

**类型**: `Object`

**结构**:
```javascript
{
  items: Array<{
    name: String,   // 项目名称
    amount: Number, // 金额（元）
    note: String    // 备注说明
  }>,
  total: Number     // 总计金额
}
```

**示例**:
```javascript
budget: {
  items: [
    { name: '交通', amount: 500, note: '往返车费' },
    { name: '住宿', amount: 800, note: '2晚酒店' },
    { name: '餐饮', amount: 600, note: '特色美食' },
    { name: '门票', amount: 300, note: '景点门票' }
  ],
  total: 2200
}
```

**渲染效果**:
- 表格形式展示
- 总计行加粗并高亮
- 自动计算总和（手动设置total）

---

### 4. 实用提示 (tips) ⭐ 新增

**类型**: `Array<String>` (可选)

**说明**: 旅行的实用建议和提示，帮助用户更好规划

**格式建议**:
```javascript
'🔸 Emoji + 提示内容'
```

**示例**:
```javascript
tips: [
  '📸 最佳拍照时间：早晚光线柔和',
  '🌅 日出时间05:21，建议4:20起床',
  '🎫 提前购买学生票，节省费用',
  '🏖️ 提前预定靠近植物园的酒店',
  '🍜 必尝：沙茶面、海蛎煎、花生汤',
  '🚇 购买地铁一日票，更划算',
  '☀️ 昆明紫外线强，注意防晒'
]
```

**渲染效果**:
- 浅黄色背景，醒目提示
- 每条tips显示为独立卡片
- 左侧橙色边框
- 悬停时轻微移动动画

**分类建议**:
- 📸 拍照技巧
- 🎫 门票/预约提示
- 🍜 美食推荐
- 🚇 交通建议
- ☀️ 天气/防晒
- 💰 省钱技巧
- 🏨 住宿建议

---

## 🎨 实际案例

### 案例1：一日游（三岔河）

```javascript
trip1: {
  title: '2025年7月三岔河一日游计划',
  dates: {
    start: '2025-07-15',
    end: '2025-07-15'  // 同一天
  },
  icon: '🏞️',
  overview: {
    highlights: [
      '🏞️ 三岔河湿地公园 - 自然氧吧',
      '🦢 观鸟胜地 - 邂逅野生鸟类',
      '🚶 湿地栈道 - 悠闲漫步'
    ],
    itinerary: [
      { day: '上午', content: '出发前往三岔河，游览湿地公园' },
      { day: '中午', content: '野餐或农家乐午餐' },
      { day: '下午', content: '湿地栈道漫步，观鸟摄影，返程' }
    ],
    budget: {
      items: [
        { name: '交通', amount: 100, note: '往返车费' },
        { name: '餐饮', amount: 80, note: '午餐' },
        { name: '门票', amount: 20, note: '湿地公园门票' }
      ],
      total: 200
    }
  }
}
```

---

### 案例2：三日游（昆明）

```javascript
trip3: {
  title: '昆明三天两夜旅行',
  dates: {
    start: '2025-09-01',
    end: '2025-09-03'
  },
  icon: '🌸',
  overview: {
    highlights: [
      '🌺 石林 - 天下第一奇观',
      '🦋 滇池 - 高原明珠',
      '🌸 翠湖公园 - 海鸥喂食',
      '🍄 野生菌火锅 - 舌尖上的云南'
    ],
    itinerary: [
      { day: '第一天', content: '抵达昆明 → 翠湖公园 → 云南大学' },
      { day: '第二天', content: '石林一日游 → 彝族歌舞表演' },
      { day: '第三天', content: '滇池海埂大坝 → 民族村 → 返程' }
    ],
    budget: {
      items: [
        { name: '交通', amount: 600, note: '往返+市内交通' },
        { name: '住宿', amount: 500, note: '2晚酒店' },
        { name: '餐饮', amount: 450, note: '野生菌+特色菜' },
        { name: '门票', amount: 250, note: '石林+民族村' }
      ],
      total: 1800
    }
  }
}
```

---

## 🚀 如何添加新旅行

### 步骤1：打开配置文件

```bash
cetapp/web/src/config/tripConfig.js
```

### 步骤2：添加新配置

```javascript
export const tripConfigs = {
  // ... 现有配置
  
  // 新增旅行 ⭐
  trip5: {
    title: '新旅行标题',
    backgroundColor: '#f0e68c',
    dates: {
      start: '2025-11-01',
      end: '2025-11-03'
    },
    icon: '🗺️',
    overview: {
      highlights: [
        '📍 亮点1',
        '📍 亮点2',
        '📍 亮点3'
      ],
      itinerary: [
        { day: '第一天', content: '行程内容' },
        { day: '第二天', content: '行程内容' }
      ],
      budget: {
        items: [
          { name: '交通', amount: 0, note: '' },
          { name: '住宿', amount: 0, note: '' }
        ],
        total: 0
      }
    }
  }
}
```

### 步骤3：后端添加数据

在Django后端创建对应的 `SiteStat` 记录：

```python
# init_trip_data.py
trips = ['trip', 'trip1', 'trip2', 'trip3', 'trip4', 'trip5']  # 添加新trip
```

### 步骤4：测试

访问: `http://localhost:8080/#/trip/trip5`

---

## ✨ 高级技巧

### 1. 使用富文本内容

在 `content` 字段中使用箭头符号：

```javascript
{ day: '第一天', content: '植物园 → 午餐 → 鼓浪屿 → 晚餐 → 酒店' }
```

### 2. 预算精确控制

手动计算total，确保准确：

```javascript
budget: {
  items: [
    { name: '交通', amount: 500, note: '' },
    { name: '住宿', amount: 800, note: '' }
  ],
  total: 1300  // 手动设置
}
```

### 3. 灵活的时间标签

```javascript
// 一日游
{ day: '上午/中午/下午' }

// 多日游
{ day: '第一天/第二天/第三天' }

// 英文
{ day: 'Day 1/Day 2/Day 3' }

// 日期
{ day: '6月22日' }
```

### 4. Emoji使用建议

| 类型 | 推荐Emoji |
|------|-----------|
| 景点 | 🏛️ 🏰 🗼 🏔️ 🏖️ |
| 活动 | 🚶 🚴 🏊 🎭 🎨 |
| 美食 | 🍜 🍲 🥘 🍱 🍰 |
| 交通 | 🚗 🚌 🚄 ✈️ 🚢 |
| 自然 | 🌸 🌺 🌳 🏞️ 🌊 |

---

## 📊 配置对比

### 现有5个旅行页面

| Trip | 标题 | 天数 | 预算 | 亮点数 |
|------|------|------|------|--------|
| trip | 厦门旅行 | 3天 | ¥2200 | 4个 |
| trip1 | 三岔河一日游 | 1天 | ¥200 | 4个 |
| trip2 | 曲靖两日游 | 2天 | ¥850 | 4个 |
| trip3 | 昆明三天两夜 | 3天 | ¥1800 | 4个 |
| trip4 | 长沙慢旅行 | 3天 | ¥2050 | 4个 |

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **亮点控制在3-5个** - 易于阅读
2. **行程按时间顺序** - 逻辑清晰
3. **预算项目4-6个** - 详略得当
4. **使用统一格式** - 保持一致

### ❌ 避免问题

1. **亮点过多** - 超过7个会显得杂乱
2. **内容过长** - 每条控制在30字内
3. **预算遗漏** - 确保total正确
4. **时间冲突** - 检查日期逻辑

---

## 📚 相关文档

- **[组件使用指南](../cetapp/web/src/components/COMPONENTS_GUIDE.md)** - TripOverview组件详解
- **[样式迁移说明](STYLE_MIGRATION.md)** - 样式设计理念
- **[迁移完成总结](MIGRATION_COMPLETE.md)** - 整体架构说明

---

## 🔄 更新流程

### 修改现有旅行内容

1. 编辑 `tripConfig.js`
2. 修改对应trip的 `overview` 配置
3. 保存文件
4. 刷新浏览器（自动热更新）

### 无需重启

Vue CLI的热更新会自动刷新，配置立即生效！

---

## 💡 FAQ

### Q: 可以省略某些字段吗？

A: 可以！如果某个trip没有配置 `overview`，会显示"行程内容正在筹划中"。

### Q: 如何添加图片？

A: 当前版本使用配置文件，暂不支持图片。未来可扩展为从后端API获取富文本内容。

### Q: 预算total必须手动计算吗？

A: 是的，建议手动设置确保准确。也可以在组件中实现自动计算。

### Q: 能否支持Markdown格式？

A: 当前版本不支持。如需富文本，建议使用独立的内容组件（高级方案）。

---

**更新日期**: 2025-10-27  
**版本**: 1.0  
**作者**: AI Assistant

**开始配置您的旅行内容吧！** ✨

