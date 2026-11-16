# Every 20 t while the domes stand: a player inside a formed dome (feet within its radius) heals 1 % max HP
# (plan Q25 "소생의 찬가"; player/heal, so the item heal hooks see it).
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ if entity @e[type=minecraft:marker,tag=rlk_mb_ap_dome,distance=..4.8] as @a[tag=player,scores={dead=0}] run function rlk:boss/apep/p/aftermath/heal1
