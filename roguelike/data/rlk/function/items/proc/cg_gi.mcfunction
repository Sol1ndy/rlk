# 중력 간섭 (@s = 플레이어, 위치 = 몸): 가장 많이 쌓인 종류(같으면 감전 > 개화 > 결정)로 주변 6칸에 달 반응 피해
scoreboard players set #cgIn itv 1
scoreboard players set #lnT tmp 1
execute if score #cgG2 itv > #cgG1 itv run scoreboard players set #lnT tmp 2
execute if score #lnT tmp matches 1 if score #cgG3 itv > #cgG1 itv run scoreboard players set #lnT tmp 3
execute if score #lnT tmp matches 2 if score #cgG3 itv > #cgG2 itv run scoreboard players set #lnT tmp 3
scoreboard players set #lnEl tmp 3
execute if score #lnT tmp matches 2 run scoreboard players set #lnEl tmp 7
execute if score #lnT tmp matches 3 run scoreboard players set #lnEl tmp 5
# 기본 피해 = 반응 기준 × #cgGI%
function rlk:element/src_player
scoreboard players operation #lnB tmp = #rBase tmp
scoreboard players operation #lnB tmp *= #cgGI tmp
scoreboard players operation #lnB tmp /= #100 tmp
scoreboard players operation #cgB itv = #lnB tmp
scoreboard players operation #cgT itv = #lnT tmp
scoreboard players operation #cgE itv = #lnEl tmp
execute if score #lnT tmp matches 1 run function rlk:items/proc/cg_gi_fx1
execute if score #lnT tmp matches 2 run function rlk:items/proc/cg_gi_fx2
execute if score #lnT tmp matches 3 run function rlk:items/proc/cg_gi_fx3
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
execute as @e[tag=rlk_mob,distance=..6] at @s run function rlk:items/proc/cg_gi_hit
function rlk:char/after_hit
scoreboard players set #cgG itv 0
scoreboard players set #cgG1 itv 0
scoreboard players set #cgG2 itv 0
scoreboard players set #cgG3 itv 0
scoreboard players set #cgIn itv 0
