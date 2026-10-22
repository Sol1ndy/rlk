# @s = player: 13 % of max HP rounded up (red herb boosts orb heals as for the normal heal orbs), at least 1,
# through player/heal (so items/hook/on_heal: 달빛 고치 -40 % and the cure meter). Rounded up so two orbs always fill
# the 15 % meter under the debuff whatever the max HP (13 % x 0.6 = 7.8 %).
scoreboard players operation #heal tmp = @s maxHealth
scoreboard players operation #heal tmp *= #bfDewPct mb
scoreboard players add #heal tmp 99
scoreboard players operation #heal tmp /= #c100 mb
execute if score @s it_red_herb matches 1.. run function rlk:items/proc/herb
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
function rlk:player/heal
