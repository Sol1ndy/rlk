scoreboard players set #cmDmg tmp 14
function rlk:cm/hit_me
execute at @e[tag=rlk_body,limit=1] run particle minecraft:sweep_attack ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 1 1.2
