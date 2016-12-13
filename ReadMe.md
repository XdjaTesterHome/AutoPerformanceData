## 常用的django命令

- django-admin.py startproject project-name  用于创建一个project
- python manage.py startapp app-name  用于创建一个应用
- python manage.py makemigrations
  python manage.py migrate  用于同步数据库
- python manage.py runserver 开发服务器，开发时使用
- python manage.py flush  用于清空数据库
- python manage.py createsuperuser  用于创建超级管理员
- python manage.py changepassword username 用于修改用户密码
- python manage.py dumpdata appname > appname.json
  python manage.py loaddata appname.json   数据导入数据迁移
- python manage.py 可以查看更多命令
- python manage.py collectstatic  收集静态文件到配置的静态目录STATIC_ROOT下
