# @s = 플레이어. 아바타가 받은 타격을 플레이어의 체력으로
scoreboard players operation @s hurtElem = #e tmp
scoreboard players operation @s hurtLv = #alv tmp
execute at @e[tag=rlk_av,limit=1] positioned ~ ~1.62 ~ run function rlk:player/take_damage
