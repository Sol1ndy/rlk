# A 1 HP heal through the real path (player/heal -> items/hook/on_heal -> mboss/player_heal).
scoreboard players set #heal tmp 1
execute as @a[tag=player,limit=1] run function rlk:player/heal
