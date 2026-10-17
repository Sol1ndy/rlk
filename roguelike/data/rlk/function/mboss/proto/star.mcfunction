# Test (pattern id 90): a breakable star 4 b in front of the boss. 40 HP pool, RES 80 % (x0.238), immune to
# Pyro (aux_hit); breaking it deals 10 % of the boss's max HP as true damage.
kill @e[tag=rlk_mb_proto_star]
kill @e[tag=rlk_mb_proto_starv]
scoreboard players set #auxHp mb 40
scoreboard players set #auxRes mb 80
execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4 positioned ~ 201 ~ run function rlk:mboss/aux/spawn
tag @e[tag=rlk_mb_auxlast,limit=1] add rlk_mb_proto_star
execute at @e[tag=rlk_mb_proto_star,limit=1] run summon minecraft:block_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_proto_starv"],block_state:{Name:"minecraft:amethyst_block"},teleport_duration:1,brightness:{sky:15,block:15},transformation:{translation:[-0.35f,-0.35f,-0.35f],left_rotation:[0.3647f,0.2798f,0.1159f,0.8806f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}
function rlk:mboss/line/say {t:"별을 부숴 보아라.",c:"#C9A8FF",gap:2,hold:24,snd:1}
