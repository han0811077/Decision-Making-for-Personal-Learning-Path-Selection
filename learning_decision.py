import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def main():
    st.set_page_config(page_title="学习路径决策系统", page_icon="📚", layout="wide")
    
    st.title("🌳 个人学习路径选择决策系统")
    st.markdown("基于多因素分析的智能学习推荐")
    st.markdown("---")
    
    # 侧边栏 - 用户输入
    st.sidebar.header("🔍 请输入您的学习条件")
    
    with st.sidebar:
        time_available = st.selectbox(
            "每日可用学习时间",
            ["1小时以下", "1-2小时", "2-4小时", "4小时以上"]
        )
        
        knowledge_level = st.selectbox(
            "当前知识水平",
            ["零基础", "初级", "中级", "高级"]
        )
        
        budget = st.slider("每月学习预算(元)", 0, 2000, 500)
        urgency = st.selectbox("学习目标紧迫度", ["宽松", "中等", "紧急"])
        learning_style = st.selectbox("学习风格偏好", ["视觉型", "听觉型", "动手型", "阅读型"])
    
    # 决策分析
    recommendation, confidence, reasoning = analyze_learning_path(
        time_available, knowledge_level, budget, urgency, learning_style
    )
    
    # 显示结果
    st.header("🎯 个性化学习推荐")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("推荐方案", recommendation)
    with col2:
        st.metric("推荐置信度", f"{confidence}%")
    with col3:
        effectiveness = calculate_expected_effectiveness(recommendation)
        st.metric("预期效果", f"{effectiveness}/100")
    
    # 显示进度条
    st.progress(confidence/100)
    
    # 决策推理过程
    st.subheader("🔍 决策推理过程")
    for i, step in enumerate(reasoning, 1):
        st.info(f"{i}. {step}")
    
    # 决策树可视化
    display_decision_tree_visualization()
    
    # 效用值对比
    display_utility_comparison()
    
    # 详细分析报告
    show_detailed_analysis(time_available, knowledge_level, budget, urgency, learning_style)

def analyze_learning_path(time, level, budget, urgency, style):
    """分析学习路径并返回推荐"""
    reasoning = []
    scores = []
    
    # 时间因素分析
    if time in ["1小时以下", "1-2小时"]:
        reasoning.append("⏰ **时间分析**: 每日可用时间有限，推荐碎片化学习方案")
        base_method = "微学习"
        scores.append(0.7)
    else:
        reasoning.append("⏰ **时间分析**: 每日学习时间充足，适合系统化深度学习")
        base_method = "系统学习"
        scores.append(0.9)
    
    # 知识水平分析
    if level in ["零基础", "初级"]:
        reasoning.append("🎓 **基础分析**: 当前基础较弱，需要分层渐进式教学")
        knowledge_method = "分层教学"
        scores.append(0.6)
    else:
        reasoning.append("🎓 **基础分析**: 已有扎实基础，适合项目驱动学习")
        knowledge_method = "项目实践"
        scores.append(0.8)
    
    # 预算分析
    if budget < 300:
        reasoning.append("💰 **预算分析**: 预算有限，优先利用免费优质资源")
        budget_method = "免费资源"
        scores.append(0.5)
    elif budget < 1000:
        reasoning.append("💰 **预算分析**: 预算适中，可选择性购买付费课程")
        budget_method = "付费课程"
        scores.append(0.7)
    else:
        reasoning.append("💰 **预算分析**: 预算充足，推荐高端定制方案")
        budget_method = "定制方案"
        scores.append(0.9)
    
    # 学习风格适配
    style_adaptations = {
        "视觉型": "+ 图文视频资料",
        "听觉型": "+ 音频课程播客", 
        "动手型": "+ 实践项目",
        "阅读型": "+ 电子书文档"
    }
    style_adapt = style_adaptations[style]
    reasoning.append(f"🎨 **风格适配**: 检测到{style}学习偏好")
    
    # 紧迫度分析
    if urgency == "紧急":
        reasoning.append("⚡ **紧迫度**: 学习目标紧迫，推荐强化训练模式")
        base_method = "强化训练"
        scores.append(0.8)
    else:
        scores.append(0.6)
    
    # 综合推荐
    recommendation = f"{base_method} + {knowledge_method} + {budget_method}"
    
    # 置信度计算
    confidence = int(np.mean(scores) * 100)
    
    return recommendation, confidence, reasoning

def calculate_expected_effectiveness(method):
    """计算预期效果分数"""
    effectiveness_scores = {
        "微学习": 70, "系统学习": 85, "强化训练": 90,
        "分层教学": 80, "项目实践": 85,
        "免费资源": 65, "付费课程": 80, "定制方案": 90
    }
    score = 70
    for key in effectiveness_scores:
        if key in method:
            score = max(score, effectiveness_scores[key])
    return score

def display_decision_tree_visualization():
    """使用文本和表格显示决策树结构"""
    st.subheader("🌳 决策树结构")
    
    # 使用文本显示决策树
    st.markdown("""
    **决策树结构示意图:**
    ```
    学习需求分析 (根节点)
    │
    ├── 时间可用性 (决策节点)
    │   ├── <2小时 → 碎片化学习 [效用:75]
    │   ├── 2-4小时 → 系统化学习 [效用:85]
    │   └── >4小时 → 强化训练 [效用:90]
    │
    ├── 知识基础 (决策节点)
    │   ├── 零基础 → 分层教学 [效用:80]
    │   ├── 有基础 → 项目实践 [效用:85]
    │   └── 进阶者 → 专题研究 [效用:88]
    │
    ├── 学习预算 (决策节点)
    │   ├── <300元 → 免费资源 [效用:70]
    │   ├── 300-1000元 → 付费课程 [效用:82]
    │   └── >1000元 → 定制方案 [效用:92]
    │
    └── 内容复杂度 (决策节点)
        ├── 基础 → 图文讲解 [效用:78]
        ├── 中等 → 案例教学 [效用:83]
        └── 复杂 → 项目驱动 [效用:87]
    ```
    """)
    
    # 决策节点详情表格
    st.subheader("📊 决策节点详情")
    decision_data = {
        '决策节点': ['时间评估', '知识评估', '预算评估', '复杂度评估'],
        '评估因素': ['每日可用学习时间', '当前知识水平', '每月学习预算', '学习内容难度'],
        '分支选项': ['3种时间方案', '3种基础方案', '3种预算方案', '3种难度方案'],
        '影响权重': ['30%', '25%', '25%', '20%']
    }
    
    df = pd.DataFrame(decision_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def display_utility_comparison():
    """显示效用值对比"""
    st.subheader("📈 各学习方案效用值对比")
    
    # 创建效用值数据
    utility_data = pd.DataFrame({
        '学习方案': ['碎片化学习', '系统化学习', '强化训练', '分层教学', 
                    '项目实践', '免费资源', '付费课程', '定制方案'],
        '效用值': [75, 85, 90, 80, 85, 65, 80, 90],
        '类型': ['时间方案', '时间方案', '时间方案', '基础方案', 
                '基础方案', '预算方案', '预算方案', '预算方案']
    })
    
    # 使用Plotly创建条形图
    try:
        fig = px.bar(
            utility_data, 
            x='学习方案', 
            y='效用值', 
            color='类型',
            title='各学习方案效用值评分对比',
            text='效用值',
            color_discrete_map={
                '时间方案': '#FF6B6B',
                '基础方案': '#4ECDC4', 
                '预算方案': '#45B7D1'
            }
        )
        
        # 美化图表
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title="学习方案",
            yaxis_title="效用值",
            yaxis_range=[0, 100],
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        # 如果Plotly出错，使用Streamlit原生图表
        st.warning("交互式图表加载中...")
        st.bar_chart(utility_data.set_index('学习方案')['效用值'])

def show_detailed_analysis(time, level, budget, urgency, style):
    """显示详细分析报告"""
    
    st.subheader("📋 详细分析报告")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 条件分析")
        
        conditions = [
            {"条件": "⏰ 时间条件", "选择": time, "分析": get_time_analysis(time)},
            {"条件": "🎓 知识条件", "选择": level, "分析": get_level_analysis(level)},
            {"条件": "💰 预算条件", "选择": f"{budget}元/月", "分析": get_budget_analysis(budget)},
            {"条件": "🎨 风格条件", "选择": style, "分析": get_style_analysis(style)},
            {"条件": "⚡ 紧迫度", "选择": urgency, "分析": get_urgency_analysis(urgency)}
        ]
        
        for condition in conditions:
            with st.expander(f"{condition['条件']}: {condition['选择']}"):
                st.write(condition['分析'])
    
    with col2:
        st.markdown("#### 💡 优化建议")
        
        suggestions = [
            "📅 **制定计划**: 根据可用时间安排固定学习时段",
            "🎯 **目标明确**: 设定具体可衡量的学习目标",
            "🔄 **定期复习**: 安排时间回顾已学内容",
            "🔍 **精选资源**: 优先选择评价高的学习材料",
            "👥 **社群学习**: 加入学习小组互相督促",
            "📝 **实践应用**: 学完立即动手实践",
            "⏱️ **时间管理**: 使用番茄工作法提高效率",
            "📊 **进度追踪**: 记录学习进度和成果"
        ]
        
        for suggestion in suggestions:
            st.write(f"• {suggestion}")

def get_time_analysis(time):
    analyses = {
        "1小时以下": "时间非常有限，建议利用碎片时间，重点学习核心概念",
        "1-2小时": "时间适中，可以安排固定学习时段，聚焦关键技能",
        "2-4小时": "时间充足，适合系统化学习，建立完整知识体系",
        "4小时以上": "时间充裕，可以进行深度学习，结合理论与实践"
    }
    return analyses.get(time, "时间条件分析")

def get_level_analysis(level):
    analyses = {
        "零基础": "从基础概念开始，需要大量示例和练习，建议循序渐进",
        "初级": "已有基本了解，可以快速回顾基础后进入核心内容",
        "中级": "具备一定基础，适合项目驱动学习，重点突破难点",
        "高级": "基础扎实，可以专注前沿技术和深度优化"
    }
    return analyses.get(level, "知识水平分析")

def get_budget_analysis(budget):
    if budget < 300:
        return "预算有限，但有很多优质免费资源可用，如开源教程、公开课等"
    elif budget < 1000:
        return "预算适中，可以选择性购买关键课程，结合免费资源使用"
    else:
        return "预算充足，可以考虑高端定制服务，获得个性化指导"

def get_style_analysis(style):
    analyses = {
        "视觉型": "适合视频教程、图表、思维导图等可视化学习材料",
        "听觉型": "适合音频课程、播客、讲解录音等听觉学习方式",
        "动手型": "适合编程实践、项目制作、实验操作等动手学习",
        "阅读型": "适合文档阅读、电子书、技术文章等文字学习"
    }
    return analyses.get(style, "学习风格分析")

def get_urgency_analysis(urgency):
    analyses = {
        "宽松": "学习进度可以放慢，注重理解深度和基础牢固",
        "中等": "需要制定明确学习计划，按部就班推进",
        "紧急": "需要强化训练，聚焦核心技能，快速提升"
    }
    return analyses.get(urgency, "紧迫度分析")

if __name__ == "__main__":
    main()