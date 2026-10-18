# 달빛 고치 removed -> 달빛 축복 받음: CRIT +15 %, DMG +50 % until the next 달빛 고치 or the fight's end.
# The kit's cure fx at the player's feet (about 20 t: gold beam down, gold burst + ring, gold emblem with
# sparkles) and chime, the badges (coc_off, buff_on), the actionbar notice and the big reward badge.
scoreboard players set #bfCoc mb 0
scoreboard players set #bfBuff mb 1
scoreboard players set #bfDmgPct mb 150
scoreboard players set #mbCritAdd mb 15
scoreboard players set #mbHealPct mb 100
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/fx/p/cure
execute at @e[tag=rlk_body,limit=1] run function rlk:mboss/butterfly/fx/snd/cure_chime
function rlk:mboss/butterfly/fx/hud/coc_off
function rlk:mboss/butterfly/fx/hud/buff_on
function rlk:mboss/butterfly/fx/hud/ab_buff
function rlk:mboss/butterfly/fx/hud/pop_buff
function rlk:mboss/butterfly/hud/refresh
