# 시간 제한 원소 부여 (@s = 플레이어). 사용: /function rlk:element/infuse_for {id:"fire",sec:10}  ({id:"help",sec:0}: 원소 id 목록)
$data modify storage rlk:tmp hq set value "$(id)"
execute if data storage rlk:tmp {hq:"help"} run return run function rlk:element/help {cmd:"/function rlk:element/infuse_for {id:…,sec:…}",pre:'/function rlk:element/infuse_for {id:"',post:'",sec:10}'}
$function rlk:element/infuse {id:"$(id)"}
$scoreboard players set @s infuseT $(sec)
scoreboard players operation @s infuseT *= #st20 tmp
