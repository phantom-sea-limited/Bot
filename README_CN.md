# Rush B

## 咋启动?

1. `bash install.sh`

## 需要改的设置

1. [`plugins.Bot`](https://github.com/phantom-sea-limited/Bot/blob/main/Lib/Bot.py)

   L11 改成你的BOT的HTTP-Adapter地址

   L29 verifyKey

   L37 sessionKey和qq

   L145 sessionKey和qq

   L159/160 二选一,SINGLE_SESSION模式不改动,反之相反
   
   在[这](https://docs.mirai.mamoe.net/mirai-api-http/adapter/HttpAdapter.html)看更多
   
2. [`plugins.Timer#L18`](https://github.com/phantom-sea-limited/Bot/blob/main/plugins/Timer.py#L18)

    修改群号为你的群号,这个群号会定时发送涩图,如果需要支持多个群,可以自己写一点功能
    
3. 用这个关键词进行全局搜索: `c:/wwwroot/api.phantom-sea-limited.ltd/`

    像下面一样进行修改:
    
    FROM
    
    `kill.finish(MessageChain(MessageSegment.image(path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/chat/kill.png")))`
    
    TO
    
    `kill.finish(MessageChain(MessageSegment.image(url=f"https://api.phantom-sea-limited.ltd/image/chat/kill.png")))`
    
    如果你会使用本地图片,你可以把云端图片下下来自己搞

## 更多

1. 为了使得 `plugins.Reload` 工作正常, `FASTAPI_RELOAD` 应该被设置成 `false`

# 感谢

部分代码来源

- [nonebot-plugin-reboot](https://github.com/18870/nonebot-plugin-reboot)

- [nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)