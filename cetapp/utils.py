"""
工具函数：帮助快速添加新的trip页面
"""

def add_trip_page_urls(page_name):
    """
    为新的trip页面生成URL配置
    
    使用方法：
    from .utils import add_trip_page_urls
    from . import views
    
    # 在urls.py中添加
    urlpatterns.extend(add_trip_page_urls('trip2'))
    """
    from django.urls import path
    from . import views
    
    urls = [
        path(f'{page_name}/', lambda request: views.trip_page_generic(request, page_name), name=f'{page_name}'),
        path(f'{page_name}/add_comment/', lambda request: views.add_comment_generic(request, page_name), name=f'{page_name}_add_comment'),
        path(f'{page_name}/delete_comment/<int:comment_id>/', lambda request, comment_id: views.delete_comment_generic(request, page_name, comment_id), name=f'{page_name}_delete_comment'),
        path(f'{page_name}/views_likes/', lambda request: views.views_likes_generic(request, page_name), name=f'{page_name}_views_likes'),
        path(f'{page_name}/checkin/', lambda request: views.checkin_view_generic(request, page_name), name=f'{page_name}_checkin'),
    ]
    
    # trip4使用专门的点赞函数，不使用通用函数
    if page_name != 'trip4':
        urls.append(path(f'{page_name}/like/', lambda request: views.like_view_generic(request, page_name), name=f'{page_name}_like'))
    
    return urls

def create_trip_page_template(page_name, title="新页面"):
    """
    生成新的trip页面HTML模板内容
    
    使用方法：
    from .utils import create_trip_page_template
    content = create_trip_page_template('trip2', 'Trip2页面')
    # 然后将content保存到cetapp/templates/cetapp/trip2.html
    """
    return f'''{{% load static %}}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{{% static 'bootstrap/bootstrap.min.css' %}}">
    <link rel="stylesheet" href="{{% static 'css/index.css' %}}">
    <style>
        /* 在这里添加页面特定的样式 */
    </style>
</head>
<body>
    <!-- 页面内容 -->
    <div class="container">
        <h1>{title}</h1>
        <!-- 在这里添加您的页面内容 -->
    </div>

    <!-- 评论区 -->
    <div class="container mt-4">
        <h3>评论区</h3>
        <div id="comments-container">
            {{% for comment in comments %}}
            <div class="comment-item border rounded p-3 mb-3">
                <div class="d-flex justify-content-between">
                    <strong>{{{{ comment.user.username }}}}</strong>
                    <small>{{{{ comment.timestamp|date:"Y-m-d H:i" }}}}</small>
                </div>
                <div class="mt-2">
                    {{{{ comment.content|linebreaks }}}}
                    {{% if comment.image %}}
                    <img src="{{{{ comment.image.url }}}}" class="img-fluid mt-2" style="max-width: 300px;" onclick="openImageModal(this.src)">
                    {{% endif %}}
                </div>
                {{% if user.is_superuser or comment.user == user %}}
                <button class="btn btn-sm btn-danger mt-2" onclick="deleteComment({{{{ comment.id }}}})">删除</button>
                {{% endif %}}
            </div>
            {{% endfor %}}
        </div>
    </div>

    <!-- 添加评论表单 -->
    {{% if user.is_superuser %}}
    <div class="container mt-4">
        <h4>添加评论</h4>
        <form id="comment-form" enctype="multipart/form-data">
            {{% csrf_token %}}
            <div class="mb-3">
                <textarea class="form-control" name="content" rows="3" placeholder="请输入评论内容..."></textarea>
            </div>
            <div class="mb-3">
                <input type="file" class="form-control" name="image" accept="image/*">
            </div>
            <button type="submit" class="btn btn-primary">发表评论</button>
        </form>
    </div>
    {{% endif %}}

    <!-- 统计信息 -->
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-6">
                <p>浏览量：<span id="views-count">{{{{ stats.views }}}}</span></p>
            </div>
            <div class="col-md-6">
                <p>点赞数：<span id="likes-count">{{{{ stats.likes }}}}</span></p>
                <button class="btn btn-success" onclick="likePage()">点赞</button>
            </div>
        </div>
    </div>

    <!-- 图片模态框 -->
    <div class="modal fade" id="imageModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-body text-center">
                    <img id="modalImage" src="" class="img-fluid">
                </div>
            </div>
        </div>
    </div>

    <script src="{{% static 'bootstrap/bootstrap.bundle.min.js' %}}"></script>
    <script>
        const pageName = '{page_name}';
        
        // 点赞功能
        function likePage() {{
            fetch(`/cetapp/${{pageName}}/like/`, {{
                method: 'POST',
                headers: {{
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }}
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById('likes-count').textContent = data.likes;
            }});
        }}

        // 添加评论
        document.getElementById('comment-form').addEventListener('submit', function(e) {{
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(`/cetapp/${{pageName}}/add_comment/`, {{
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

        // 删除评论
        function deleteComment(commentId) {{
            if (confirm('确定要删除这条评论吗？')) {{
                fetch(`/cetapp/${{pageName}}/delete_comment/${{commentId}}/`, {{
                    method: 'POST',
                    headers: {{
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
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
        function openImageModal(src) {{
            document.getElementById('modalImage').src = src;
            new bootstrap.Modal(document.getElementById('imageModal')).show();
        }}

        // 页面加载时更新统计信息
        window.addEventListener('load', function() {{
            fetch(`/cetapp/${{pageName}}/views_likes/`)
            .then(response => response.json())
            .then(data => {{
                document.getElementById('views-count').textContent = data.views;
                document.getElementById('likes-count').textContent = data.likes;
            }});
        }});
    </script>
</body>
</html>''' 