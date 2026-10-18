# 달빛 고치 removed (the meter reached 15 % of max HP) -> 달빛 축복 받음: CRIT RATE +15 % and CRIT DMG
# +50 % (items/hook/stat_buffs: #mbCritAdd / #mbCritDmgAdd; user: "피해 +50%가 아니라 치명타 피해 +50%야")
# until the next 달빛 고치 or the fight's end. The kit's cure fx at the player's feet (about 20 t: gold beam down, gold
# burst + ring, gold emblem with sparkles) and chime, the badges (coc_off, buff_on), the actionbar notice and the big
# reward badge.
scoreboard players set #bfCoc mb 0
scoreboard players set #bfBuff mb 1
scoreboard players set #bfDmgPct mb 100
scoreboard players set #mbCritAdd mb 15
scoreboard players set #mbCritDmgAdd mb 50
scoreboard players set #mbHealPct mb 100
scoreboard players set #bfCure mb 0
scoreboard players set #bkCureP mb 0
# the hint "달빛 고치 — 체력 15% 회복하면 해제" still typing or held on the subtitle line goes now: its steps would blank the reward pop
# below and it would stay 3 s after the cure (review fix FX-3)
execute if score #mbLn mb matches 1 if data storage rlk:mboss {ln:{t:"달빛 고치 — 체력 15% 회복하면 해제"}} run function rlk:mboss/line/clear
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/wx/cure/start
function rlk:mboss/butterfly/fx/hud/coc_off
function rlk:mboss/butterfly/fx/hud/buff_on
function rlk:mboss/butterfly/fx/hud/ab_buff
function rlk:mboss/butterfly/fx/hud/pop_buff
function rlk:mboss/butterfly/hud/refresh
