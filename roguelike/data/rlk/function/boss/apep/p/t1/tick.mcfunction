# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
function rlk:boss/apep/heart/tick
execute if score #apPT mb matches 20 run execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned ~ 201 ~ run function rlk:boss/apep/fx/p/root_chunks
execute if score #apPT mb matches 20 run execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned ~ 201 ~ run function rlk:boss/apep/fx/snd/p1_dive
execute if score #apPT mb matches 30 run execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned ~ 201 ~ run function rlk:boss/apep/fx/p/root_chunks
execute if score #apPT mb matches 6 run function rlk:boss/apep/svc/lib_clear
execute if score #apPT mb matches 6 run scoreboard players set #mbNoLeash mb 1
execute if score #apPT mb matches 45 run function rlk:boss/apep/svc/park
execute if score #apPT mb matches 45 run function rlk:boss/apep/om/heart/play/cradle_rise
execute if score #apPT mb matches 45 run execute positioned 440 201 8 run function rlk:boss/apep/fx/dress/swirl {r:35}
execute if score #apPT mb matches 45 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/cradle_dust
execute if score #apPT mb matches 45 run execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/t1_cradle
execute if score #apPT mb matches 50 run function rlk:boss/apep/om/heart/play/heart_lower
execute if score #apPT mb matches 50 run execute positioned 440 221 8 run function rlk:boss/apep/fx/snd/t1_lower
execute if score #apPT mb matches 100 run function rlk:boss/apep/om/heart/play/heart_drop
execute if score #apPT mb matches 106 run execute positioned 440 201 8 run function rlk:boss/apep/fx/p/heart_beam
execute if score #apPT mb matches 106 run execute positioned 440 202.6 8 run function rlk:boss/apep/fx/snd/t1_land
execute if score #apPT mb matches 106 run function rlk:boss/apep/p/t1/heart_on
execute if score #apPT mb matches 108 run function rlk:mboss/line/say {t:"마물을 처치해서 소생 진행도를 올리세요",c:"#EDCF63",gap:2,hold:100,snd:2}
execute if score #apPT mb matches 108 run function rlk:boss/apep/svc/cine_off
execute if score #apPT mb matches 116 run function rlk:boss/apep/rev/wave_t1
execute if score #apPT mb matches 117..136 run function rlk:boss/apep/org/pend_tick
execute if score #apPT mb matches 136.. run function rlk:boss/apep/p/t1/done
scoreboard players operation #apM mb = #apPT mb
scoreboard players operation #apM mb %= #apK10 mb
execute if score #apM mb matches 0 positioned 440 201 8 run function rlk:boss/apep/fx/p/haze_withered
