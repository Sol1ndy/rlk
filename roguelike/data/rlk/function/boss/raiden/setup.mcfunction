function rlk:room/mob_init
attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
scoreboard players set @s rdCycle 0
scoreboard players set @s rdPrev 0
scoreboard players set @s rdTurns 0
function rlk:boss/raiden/reload
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
title @a[tag=player] times 8 60 16
title @a[tag=player] subtitle {text:"바닥의 보랏빛 예고를 보고 회피하세요",color:"white"}
title @a[tag=player] title {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 84
scoreboard players set @a[tag=player] ttlT 84
scoreboard players set #rdCap rd 1
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.7 0.62 0.3
