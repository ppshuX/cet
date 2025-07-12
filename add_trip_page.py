#!/usr/bin/env python
"""
快速添加新trip页面的脚本
使用方法：python add_trip_page.py trip3 "Trip3页面"
注意：页面名称应该按递增顺序：trip2, trip3, trip4...
"""

import os
import sys

def get_next_trip_number():
    """获取下一个trip页面编号"""
    trip_dir = 'cetapp/templates/cetapp'
    if not os.path.exists(trip_dir):
        return 2
    
    existing_trips = []
    for file in os.listdir(trip_dir):
        if file.startswith('trip') and file.endswith('.html'):
            try:
                # 提取数字部分
                if file == 'trip.html':
                    existing_trips.append(1)
                else:
                    num = int(file.replace('trip', '').replace('.html', ''))
                    existing_trips.append(num)
            except ValueError:
                continue
    
    if not existing_trips:
        return 2
    
    return max(existing_trips) + 1

def add_new_trip_page(page_name, title):
    """快速添加新的trip页面"""
    
    # 1. 创建HTML模板文件
    template_content = f'''{{% load static %}}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            line-height: 1.8;
            background-color: #f0e68c;
            margin: 0;
            padding: 2rem;
            color: #333;
        }}

        h1, h2 {{
            color: #2c3e50;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 2rem;
        }}

        section {{
            background: #fff;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}

        ul {{
            padding-left: 1.2rem;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}

        table, th, td {{
            border: 1px solid #ccc;
        }}

        th, td {{
            padding: 0.75rem;
            text-align: left;
        }}

        th {{
            background-color: #f0f0f0;
        }}

        .total {{
            font-weight: bold;
            background-color: #fcfcfc;
        }}

        .progress-container {{
            background: #e0e0e0;
            border-radius: 20px;
            overflow: hidden;
            height: 24px;
            margin: 1.5rem 0;
        }}

        .progress-bar {{
            background: #4caf50;
            height: 100%;
            width: 0%;
            text-align: center;
            color: white;
            line-height: 24px;
            font-size: 14px;
        }}

        .check-in {{
            display: inline-block;
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background-color: #3498db;
            color: #fff;
            border: none;
            border-radius: 6px;
            cursor: not-allowed;
        }}

        .comments textarea {{
            width: 100%;
            height: 80px;
            padding: 0.5rem;
            border-radius: 6px;
            border: 1px solid #ccc;
            margin-bottom: 0.5rem;
        }}

        .comments button {{
            padding: 0.5rem 1rem;
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }}

        .comment-list {{
            margin-top: 1rem;
        }}

        .comment {{
            background: #f0f0f0;
            padding: 0.5rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            position: relative;
        }}

        .comment time {{
            display: block;
            font-size: 12px;
            color: #888;
            margin-top: 0.25rem;
        }}

        .comment .delete-btn {{
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: none;
            border: none;
            color: #c0392b;
            font-size: 16px;
            cursor: pointer;
        }}

        .stats {{
            margin-top: 1rem;
            color: #555;
        }}

        /* 行程计划特定样式 */
        .trip-plan {{
            background: #fff;
            color: #234;
            padding: 2rem 2.5rem;
            margin-bottom: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }}

        .trip-plan h3 {{
            color: #2366b4;
            font-weight: bold;
            margin-bottom: 1.2rem;
        }}

        .trip-plan p strong {{
            color: #e67e22;
        }}

        .trip-plan p {{
            margin-bottom: 0.7rem;
            font-size: 1.08rem;
        }}

        .schedule-table {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin: 2rem 0;
        }}

        .schedule-table table {{
            margin: 0;
        }}

        .schedule-table th {{
            background: #667eea;
            color: white;
            padding: 1rem;
            font-weight: 600;
        }}

        .schedule-table td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #eee;
        }}

        .schedule-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        .schedule-table tr:hover {{
            background-color: #e3f2fd;
        }}

        .time-slot {{
            font-weight: bold;
            color: #667eea;
        }}

        .location {{
            color: #333;
        }}

        .notes {{
            color: #666;
            font-style: italic;
        }}

        .emoji {{
            font-size: 1.2em;
            margin-right: 0.5rem;
        }}

        .current-row {{
            background: #e3f2fd !important;
            transition: background 0.3s;
        }}

        @media (max-width: 768px) {{
            .schedule-table {{
                font-size: 0.9rem;
            }}

            .schedule-table td,
            .schedule-table th {{
                padding: 0.5rem;
            }}
        }}
    </style>
    <script>
        function getCookie(name) {{
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {{
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {{
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {{
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }}
                }}
            }}
            return cookieValue;
        }}
        const csrftoken = getCookie('csrftoken');
    </script>
</head>
<body>
    <br>
    <h2 style="text-align:center; font-size:1.2rem;">{title}</h2>

    <div style="position: absolute; top: 20px; right: 20px;">
        {{% if user.is_authenticated %}}
        👋 你好啊，{{{{ user.username }}}}！
        <form id="logoutForm" action="{{% url 'logout' %}}?next=/cetapp/{page_name}/" method="post" style="display:inline;">
            {{% csrf_token %}}
            <button type="submit"
                style="background:none; border:none; color:#2366b4; cursor:pointer; font-size:1rem;">退出</button>
        </form>
        {{% else %}}
        <a href="{{% url 'login' %}}?next={{{{ request.path }}}}">登录</a> /
        <a href="{{% url 'register' %}}?next={{{{ request.path }}}}">注册</a>
        {{% endif %}}
    </div>

    <section>
        <h2>🌊 旅行进度条</h2>
        <div class="progress-container">
            <div id="progressBar" class="progress-bar" style="width:50%;">加载中...</div>
        </div>
    </section>

    <!-- 行程计划内容 -->
    <section class="trip-plan">
        <h3><span class="emoji">📍</span> {title}</h3>
        <p><strong>成员：</strong>请填写成员</p>
        <p><strong>出发时间：</strong>请填写出发时间</p>
        <p><strong>预算：</strong>请填写预算</p>
    </section>

    <!-- 行程安排表格 -->
    <section>
        <h4><span class="emoji">📅</span> 行程安排</h4>
        <table id="schedule-table">
            <tr>
                <th>时间段</th>
                <th>地点 / 活动</th>
                <th>备注</th>
            </tr>
            <!-- 示例行程行，请根据实际情况修改 -->
            <tr data-start="2025-01-01 08:00" data-end="2025-01-01 09:00">
                <td class="time-slot">08:00 – 09:00</td>
                <td class="location">示例活动1</td>
                <td class="notes">示例备注</td>
            </tr>
            <tr data-start="2025-01-01 09:00" data-end="2025-01-01 10:00">
                <td class="time-slot">09:00 – 10:00</td>
                <td class="location">示例活动2</td>
                <td class="notes">示例备注</td>
            </tr>
            <!-- 请继续添加更多行程行，记得为每行添加 data-start 和 data-end 属性 -->
        </table>
    </section>

    <!-- 评论区 -->
    <section class="comments">
        <h2>�� 打卡与留言</h2>
        <div style="text-align: left; margin-bottom: 10px;">
            <button id="toggleOrderBtn" class="btn btn-secondary">🔃 切换评论顺序</button>
        </div>
        <button id="checkInBtn" class="check-in" onclick="checkIn()">📍 去打卡</button>
        {{% if user.is_superuser %}}
        <form id="commentForm" method="POST" enctype="multipart/form-data">
            {{% csrf_token %}}
            <textarea id="commentInput" name="content" placeholder="写下你的留言或建议..."></textarea>
            <input type="file" name="image" accept="image/*">
            <button type="submit">💬 发表评论</button>
        </form>
        {{% else %}}
        <p style="color: gray;">🛡️ 当前仅站主可发表评论，欢迎打卡浏览。</p>
        {{% endif %}}
        <div class="comment-list" id="commentList" data-order="asc">
            {{% for comment in comments %}}
            <div class="comment" style="margin-bottom: 24px; position: relative;">
                <strong>{{{{ comment.user.username }}}} : &nbsp;</strong>
                {{{{ comment.content|linebreaksbr }}}}
                {{% if comment.image %}}
                <div style="margin-top: 10px; text-align: center;">
                    <img src="{{{{ comment.image.url }}}}" alt="comment image" onclick="showImageModal(this.src)" style="display: inline-block;
                                                          max-width: 100%;
                                                          max-height: 600px;
                                                          border-radius: 12px;
                                                          box-shadow: 0 6px 16px rgba(0,0,0,0.15);
                                                          transition: all 0.3s ease;
                                                          cursor: pointer;">
                </div>
                {{% endif %}}
                <div style="color: #aaa; font-size: 12px; margin-top: 6px; text-align: right;">
                    {{{{ comment.timestamp|date:"Y-m-d H:i" }}}}
                </div>
                {{% if comment.user == user or user.is_superuser %}}
                <button class="delete-btn" onclick="deleteComment(this, {{{{ comment.id }}}})"
                    style="position: absolute; top: 0; right: 0;">
                    🗑️
                </button>
                {{% endif %}}
            </div>
            {{% endfor %}}
        </div>
    </section>

    <!-- 图片查看模态框 -->
    <div id="imageModal" style="
        display: none;
        position: fixed;
        z-index: 10000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.9);
        backdrop-filter: blur(5px);">
        <div style="
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;">
            <img id="modalImage" src="" alt="大图" style="
                max-width: 95%;
                max-height: 95%;
                object-fit: contain;
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);" />
            <button id="closeModal" style="
                position: absolute;
                top: 20px;
                right: 30px;
                color: #f1f1f1;
                font-size: 40px;
                font-weight: bold;
                background: none;
                border: none;
                cursor: pointer;
                z-index: 10001;">&times;</button>
        </div>
    </div>

    <script>
        function parseTime(str) {{
            // 支持"2025-07-12 08:00"或"08:00"等格式
            if (!str) return null;
            if (str.length <= 5) {{
                // 仅时间，补全日期
                const today = new Date();
                str = today.getFullYear() + '-' + (today.getMonth() + 1).toString().padStart(2, '0') + '-' + today.getDate().toString().padStart(2, '0') + ' ' + str;
            }}
            return new Date(str.replace(/-/g, '/'));
        }}

        function updateProgress() {{
            const rows = document.querySelectorAll('#schedule-table tr[data-start]');
            if (rows.length === 0) return;

            // 获取所有开始/结束时间
            const startTimes = Array.from(rows).map(row => parseTime(row.dataset.start));
            const endTimes = Array.from(rows).map(row => parseTime(row.dataset.end));
            const tripStart = startTimes[0];
            const tripEnd = endTimes[endTimes.length - 1];
            const now = new Date();

            // 计算百分比
            let percent = 0;
            if (now <= tripStart) percent = 0;
            else if (now >= tripEnd) percent = 100;
            else percent = ((now - tripStart) / (tripEnd - tripStart) * 100).toFixed(0);

            // 更新进度条
            const bar = document.getElementById('progressBar');
            bar.style.width = percent + '%';
            bar.textContent = percent + '%';

            // 高亮当前行
            rows.forEach(row => row.classList.remove('current-row'));
            for (let i = 0; i < rows.length; i++) {{
                const s = parseTime(rows[i].dataset.start);
                const e = parseTime(rows[i].dataset.end);
                if (now >= s && now < e) {{
                    rows[i].classList.add('current-row');
                    break;
                }}
            }}
        }}
        setInterval(updateProgress, 60 * 1000); // 每分钟刷新
        updateProgress();

        // 页面加载时更新统计信息
        window.addEventListener('load', function () {{
            fetch('/cetapp/{page_name}/views_likes/')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('views').textContent = data.views;
                    document.getElementById('likes').textContent = data.likes;
                }});
        }});

        // 点赞功能
        document.getElementById('like-btn').addEventListener('click', function () {{
            fetch('/cetapp/{page_name}/like/', {{
                method: 'POST',
                headers: {{
                    'X-CSRFToken': csrftoken
                }}
            }})
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('likes').textContent = data.likes;
                }});
        }});

        // 添加评论
        const commentForm = document.getElementById('commentForm');
        if (commentForm) {{
            commentForm.addEventListener('submit', function (e) {{
                e.preventDefault();
                const formData = new FormData(this);

                fetch('/cetapp/{page_name}/add_comment/', {{
                    method: 'POST',
                    body: formData
                }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.status === 'ok') {{
                            location.reload();
                        }}
                    }});
            }});
        }}

        // 删除评论
        function deleteComment(btn, commentId) {{
            if (confirm('确定要删除这条评论吗？')) {{
                const form = btn.closest('form');
                const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
                const csrftoken = csrfInput ? csrfInput.value : getCookie('csrftoken');

                fetch(`/cetapp/{page_name}/delete_comment/${{commentId}}/`, {{
                    method: 'POST',
                    headers: {{
                        'X-CSRFToken': csrftoken
                    }}
                }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.status === 'ok') {{
                            location.reload();
                        }}
                    }});
            }}
        }}

        // 图片模态框
        function showImageModal(src) {{
            document.getElementById('modalImage').src = src;
            document.getElementById('imageModal').style.display = 'flex'; // Use flex for centering
        }}

        function closeImageModal() {{
            document.getElementById('imageModal').style.display = 'none';
        }}

        // 切换评论顺序
        let commentsReversed = false;
        document.getElementById('toggleOrderBtn').addEventListener('click', function () {{
            const commentList = document.getElementById('commentList');
            const comments = Array.from(commentList.children);
            comments.reverse();
            commentList.innerHTML = '';
            comments.forEach(comment => commentList.appendChild(comment));
            commentsReversed = !commentsReversed;
        }});

        // 文件选择
        function updateFileName(input) {{
            const fileName = input.files[0] ? input.files[0].name : '未选择任何文件';
            document.getElementById('fileName').textContent = fileName;
        }}
    </script>
</body>
</html>'''

    # 2. 写入模板文件
    template_path = f'cetapp/templates/cetapp/{page_name}.html'
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ 已创建模板文件: {template_path}")
    
    # 3. 生成URL配置代码
    url_code = f'''
# 在 cetapp/urls.py 中添加以下代码：
from .utils import add_trip_page_urls

# 添加 {page_name} 页面的URL
urlpatterns.extend(add_trip_page_urls('{page_name}'))
'''
    
    print(f"\n📝 需要在 cetapp/urls.py 中添加以下代码：")
    print(url_code)
    
    # 4. 生成视图函数代码
    view_code = f'''
# 在 cetapp/views.py 中添加以下代码：
def {page_name}(request):
    return trip_page_generic(request, '{page_name}')
'''
    
    print(f"\n📝 需要在 cetapp/views.py 中添加以下代码：")
    print(view_code)
    
    # 5. 生成使用说明
    usage_guide = f'''
🎯 使用说明：
1. 模板文件已创建：{template_path}
2. 请在 cetapp/urls.py 中添加URL配置
3. 请在 cetapp/views.py 中添加视图函数
4. 编辑 {page_name}.html 文件，修改行程表内容
5. 为每个行程行添加 data-start 和 data-end 属性，例如：
   <tr data-start="2025-01-01 08:00" data-end="2025-01-01 09:00">
     <td class="time-slot">08:00 – 09:00</td>
     <td class="location">活动内容</td>
     <td class="notes">备注</td>
   </tr>

✨ 功能特性：
- ✅ 进度条根据时间动态显示百分比
- ✅ 自动高亮当前进行中的行程行
- ✅ 每分钟自动刷新进度
- ✅ 评论、点赞、浏览量统计
- ✅ 图片上传和放大查看
- ✅ 评论顺序切换
- ✅ 响应式设计
'''
    
    print(usage_guide)

def main():
    if len(sys.argv) != 3:
        print("使用方法：python add_trip_page.py <页面名称> <页面标题>")
        print("示例：python add_trip_page.py trip3 \"Trip3页面\"")
        return
    
    page_name = sys.argv[1]
    title = sys.argv[2]
    
    # 检查页面名称格式
    if not page_name.startswith('trip'):
        print("❌ 页面名称必须以 'trip' 开头")
        return
    
    # 检查是否已存在
    template_path = f'cetapp/templates/cetapp/{page_name}.html'
    if os.path.exists(template_path):
        print(f"❌ 页面 {page_name} 已存在")
        return
    
    add_new_trip_page(page_name, title)

if __name__ == "__main__":
    main() 