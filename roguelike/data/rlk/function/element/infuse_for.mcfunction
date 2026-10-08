# 시간 제한 원소 부여 (@s = 플레이어). 사용: /function rlk:element/infuse_for {id:"fire",sec:10}
$function rlk:element/infuse {id:"$(id)"}
$scoreboard players set @s infuseT $(sec)
scoreboard players operation @s infuseT *= #st20 tmp
