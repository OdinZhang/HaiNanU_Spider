# 海南大学教务系统爬虫

今天是大年三十，但是，我就是不想去看春晚，所以决定新开一个项目来把我这几天做的爬虫给上传上来，由于海南大学的教务系统使用的是强智的教务系统，但是，其在登录界面进行了一点修改，需要Ajax请求和使用JavaScript计算encoded，经过我的不懈努力，终于将其攻破（但是我就是不想发布，不服咋地？），因此决定先发一个简单版本的爬虫，功能上绝对可以用，目测是学校疏忽了没有把改动给更新进去，目测是强智系统预留的一个，基本原理是登录之后退出到登录界面，那个链接是一个非常简单的链接，没有什么复杂操作就可以登录，我也不知道为什么不是和最初的登陆界面是一个url，直接看代码就可以了。