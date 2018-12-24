# LittleSa ---- 小萨

> 一个面向女朋友的基于wxpy的生活助手 v2.0
> 经过进半年的静默，你终于重获新生！

## 依赖

+ python 3.6
+ wxpy 0.3.9.8
+ mysql 5.6
+ face++ apikey and apisecret
+ tuling apikey

## 功能简介

### 每日天气推送

爬取[新浪天气](http://weather.sina.com.cn/)页面，进行分析并做缓存，并在指定时间进行发送。

### 课程推送

每学期开学爬取女朋友她们学校的教务网站，并解析制作sql更新后端数据库。（事实上这么少的数据用json或者sqlite更好）
每天计算当前周次在数据库中查找相应数据。

### 壁纸推送

调showapi的接口获取每日壁纸，数据源是必应的，质量还可以。

### 笑话推送

爬去一个很古老的[笑话网站](http://m.kaixinhui.com/)（里面的评论都是零几年的），内容一般，下个版本换数据源。

### tuling机器人自动回复消息

[wxpy](https://github.com/youfou/wxpy)封装的小组件，很实用，省下大部分的开发量，只需在[图灵机器人](http://www.turingapi.com/)注册账号拿到apikey即可

### 洗衣机监控

可以返回女朋友她们宿舍洗衣机的使用情况，是否占用和还剩余几分钟。很实用的功能。

### face++人脸识别

#### beautify

利用face++接口实现美图

#### detect face

利用face++的接口实现图片人脸探测，标注颜值加以分析。很有趣的功能。