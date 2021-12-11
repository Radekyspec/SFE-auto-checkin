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
python sfe_check_in.py [-h] -c "你的cookies值" 
```

## 模块化
文件主体为`SFEAutoCheckIn`类，调用该类的`run`函数即可
