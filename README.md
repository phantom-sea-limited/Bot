# run

> Other languages:
>
> - [Simplified Chinese (简体中文)](/README_CN.md)

## How to start

1. `bash install.sh`

## Something need to setting

1. [`plugins.Bot#L11`](https://github.com/phantom-sea-limited/Bot/blob/main/Lib/Bot.py#L11)

   Need to change to yours BOT-Http-Adapter-Address
   
   see more [here](https://docs.mirai.mamoe.net/mirai-api-http/adapter/HttpAdapter.html)
   
2. [`plugins.Timer#L18`](https://github.com/phantom-sea-limited/Bot/blob/main/plugins/Timer.py#L18)

    change the input number to yours group which you need to send the anime image periodically
    
3. Search all code using this keyword: `c:/wwwroot/api.phantom-sea-limited.ltd/`

    change them like this example:
    
    FROM
    
    `kill.finish(MessageChain(MessageSegment.image(path=f"c:/wwwroot/api.phantom-sea-limited.ltd/image/chat/kill.png")))`
    
    TO
    
    `kill.finish(MessageChain(MessageSegment.image(url=f"https://api.phantom-sea-limited.ltd/image/chat/kill.png")))`
    
    if you know how to use local image, you can download these image using in your ways

## Something more

1. to keep the `plugins.Reload` work in the right way, `FASTAPI_RELOAD` in .env should be `false`
