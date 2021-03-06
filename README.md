# SFE-auto-checkin

### 简介

快捷通过简幻欢平台签到验证，获取签到内容

## 使用方法

#### 项目依赖
* Python >= 3.7

#### 克隆本仓库
```shell
git clone https://github.com/Radekyspec/SFE-auto-checkin.git
```

#### 进入仓库文件夹
```shell
cd SFE-auto-ckeckin
```

#### 安装依赖
```shell
pip install -r requirements.txt
```

#### 运行！
```shell
python sfe_check_in.py [-h] -u "注册SFE平台的QQ账号" -p "SFE平台的密码" 
```

#### 在go-cqhttp中使用
```shell
打开[gocq] sfe_check_in.py并根据注释填写账号密码

将所有py文件注册成插件

Enjoy！
```

## 模块化
`sfe_check_in.py`文件主体为`SFEAutoCheckIn`类，调用`sfe_login.py`进行登录操作和获取cookies。该类必要参数为`username`和`password`，调用该类的`run`函数即可

## 自动化
~~建议配合[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)与[APScheduler](https://github.com/agronholm/apscheduler)实现全自动签到<br>
通过[BeautifulSoup](https://pypi.org/project/beautifulsoup4)库识别html元素，判定何时需要签到，准确率高，即使当次循环签到失败也不用担心~~<br>
已上传go-cqhttp版本，将三个文件注册成为go-cqhttp的插件即可使用。注意在使用前需要前往`[gocq] sfe_check_in.py`文件并根据注释填写账号密码
