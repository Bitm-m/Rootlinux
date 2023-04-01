
<h4 align="center">通过Cloudflare Workers自动续期Freenom域名(.cf .ga .gq .ml .tk)。</h4>

 喜欢这个项目？给颗Star吧！
</p>

## py版
只有张三才可以触发

https://{replit}/?name=%E5%BC%A0%E4%B8%89

## 部署

打开你的 [Cloudflare管理面板](https://dash.cloudflare.com)


在账号主页左侧侧边栏选择Workers


在Workers页面，选择创建服务，设置好服务名称，选择HTTP处理程序。


在刚刚创建的Workers界面，选择“快速编辑”。


返回刚刚创建的Workers页面，选择“设置”，再选择“变量”。


在变量页面，添加以下变量和变量值：

- SECRET_USERNAME变量，填入Freenom用户名

- SECRET_PASSWORD变量，填入Freenom密码

- TGBOT_TOKEN变量,填入Tg-bot TGBOT_TOKEN

- TGBOT_CHAT_ID变量,填入Tg-bot TGBOT_CHAT_ID





（可选）勾选两个变量的“加密”选项（可极大程度降低Freenom用户名和密码泄露的概率）。


返回创建的Workers页面，选择“触发器”。


在触发器界面，选择添加Cron触发器。在“添加Cron触发器”界面，设置触发器，保存。推荐执行时间为一天一次。


在同一界面的路由选项中禁用默认路由（通常为 服务名.子域名.workers.dev）。

## 测试

（快速编辑-预览 访问）在快速编辑界面中的“预览”访问已部署的Workers。顺利的话，你将看到你账户内所有域名的剩余日期。
_请注意，通过预览访问不会触发续期任务，仅用于测试是否可以获取账户内所有域名的剩余日期。_

（触发Cron）进入“快速编辑”，选择“设定时间”，再选择“触发计划的事件”。查看下方Console是否有输出域名剩余日期。（如有可续期的域名，会输出是否续期成功。）




