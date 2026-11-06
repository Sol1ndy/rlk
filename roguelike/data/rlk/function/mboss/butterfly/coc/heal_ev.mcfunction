# The player received heals since the last module tick (rlk:mboss/player_heal counted them and added their amounts
# to #mbHealAmt, already reduced to 60 %, overheal included). While 달빛 고치 is on they fill the cure meter
# #bfCure (user: "일정 체력 이상 회복해야 하게"; it used to be any heal): at 15 % of max HP (#bfCureT) it is
# cured, below that a small chime and the meter on the actionbar (the boss-bar sub-line reads it live).
execute if score #bfCoc mb matches 1 run scoreboard players operation #bfCure mb += #mbHealAmt mb
scoreboard players set #mbHealEv mb 0
scoreboard players set #mbHealAmt mb 0
execute unless score #bfCoc mb matches 1 run return 0
execute as @a[tag=player,limit=1] run function rlk:mboss/butterfly/coc/meter
execute if score #bfCure mb >= #bfCureT mb run return run function rlk:mboss/butterfly/coc/cure
execute as @a[tag=player,limit=1] at @s run function rlk:mboss/butterfly/coc/progress
