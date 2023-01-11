---
sidebar-position: 1
description: 一切的开始

options:
  menu:
    weight: 10
    category: guide
---

# 从零开始

## 前情提要

### 下载Mirai

如果你已经有了一个[Mirai Bot](https://docs.mirai.mamoe.net/)并且安装了[Mirai HTTP API插件](https://docs.mirai.mamoe.net/mirai-api-http/), 那么你可以跳过这个部分

如果没有的话, 那请去如下地址查看Mirai官方文档

> [**传送门**](https://docs.mirai.mamoe.net/UserManual.html#%E5%90%AF%E5%8A%A8-mirai)
>
> 推荐使用[**纯命令行版本**](https://docs.mirai.mamoe.net/ConsoleTerminal.html#%E5%AE%89%E8%A3%85)

接下来, 请按照[**Mirai HTTP API官方文档**](https://docs.mirai.mamoe.net/mirai-api-http/#%E4%BD%BF%E7%94%A8-mirai-console-loader-%E5%AE%89%E8%A3%85mirai-api-http)进行安装

### 配置Mirai HTTP API

如果你只登录一个账号,你可以直接复制如下配置到该路径`config/net.mamoe.mirai-api-http/setting.yml`

多账户请看[官方文档](https://docs.mirai.mamoe.net/mirai-api-http/#setting-yml-%E6%A8%A1%E6%9D%BF)
```yml title=config/net.mamoe.mirai-api-http/setting.yml
## 配置文件中的值，全为默认值

## 启用的 adapter, 内置有 http, ws, reverse-ws, webhook
adapters:
  - http
  - ws

## 是否开启认证流程, 若为 true 则建立连接时需要验证 verifyKey
## 建议公网连接时开启
enableVerify: false
verifyKey: 1234567890

## 开启一些调式信息
debug: false

## 是否开启单 session 模式, 若为 true，则自动创建 session 绑定 console 中登录的 bot
## 开启后，接口中任何 sessionKey 不需要传递参数
## 若 console 中有多个 bot 登录，则行为未定义
## 确保 console 中只有一个 bot 登陆时启用
singleMode: true

## 历史消息的缓存大小
## 同时，也是 http adapter 的消息队列容量
cacheSize: 4096

## adapter 的单独配置，键名与 adapters 项配置相同
adapterSettings:
  ## 详情看 http adapter 使用说明 配置
  http:
    host: 0.0.0.0
    port: 20000
    cors: [*]
  
  ## 详情看 websocket adapter 使用说明 配置
  ws:
    host: 0.0.0.0
    port: 20001
    reservedSyncId: -1
```

### 可选配置

配置[Mirai Console自动登录](https://docs.mirai.mamoe.net/ConsoleTerminal.html#%E8%87%AA%E5%8A%A8%E7%99%BB%E5%BD%95)

关于[`/autoLogin`](https://docs.mirai.mamoe.net/console/BuiltInCommands.html#autologincommand)的相关参数, 你也可以通过在命令行中输入`/help`查看

推荐修改登录device类型(默认`ANDROID_PHONE`), 手动修改config/Console/AutoLogin.yml

```yml title=config/Console/AutoLogin.yml
accounts: 
  - # 账号, 现只支持 QQ 数字账号
    account: 123456
    password: 
      # 密码种类, 可选 PLAIN 或 MD5
      kind: PLAIN
      # 密码内容, PLAIN 时为密码文本, MD5 时为 16 进制
      value: pwd
    # 账号配置. 可用配置列表 (注意大小写):
    # "protocol": "ANDROID_PHONE" / "ANDROID_PAD" / "ANDROID_WATCH" / "MACOS" / "IPAD"
    # "device": "device.json"
    # "enable": true
    # "heartbeatStrategy": "STAT_HB" / "REGISTER" / "NONE"
    configuration: 
      protocol: ANDROID_PHONE
      device: device.json
```

将默认的`ANDROID_PHONE`修改为其他可用的任意值(如"ANDROID_PAD" / "ANDROID_WATCH" / "MACOS" / "IPAD")

:::tip
~~原因是`ANDROID_PHONE`的风控风险大于其他任何值, 此内容并未被官方明确提出, 但很多人均认可~~
:::


## 下载幻海Bot酱

```bash 
git clone git@github.com:phantom-sea-limited/Bot.git
```

```bash
git clone https://github.com/phantom-sea-limited/Bot.git
```

或者在github页面选择Download ZIP, 以上均可, 但是为了便于更新, 推荐使用Git方式

在下载完成后, Linux系统请输入```bash install.sh```进行依赖安装

Windows请稍后, 鞠躬.jpg