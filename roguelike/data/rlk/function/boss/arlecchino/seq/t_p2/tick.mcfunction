# Transition T (PLAN §3.2: stagger, kneel, the crimson pillar, blackout + the crimson arena, rise, the form swap, six blade legs, twin scythes, title, launch). @s = the body; #sq kn 1.. = the clip tick shown this game tick.
execute if score #sq kn matches 0 at @s run function rlk:boss/arlecchino/fx/snd/t_stagger
execute if score #sq kn matches 0 at @s run function rlk:boss/arlecchino/rig/anchor/chest
execute if score #sq kn matches 0 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/embers_puff
execute if score #sq kn matches 24 at @s run function rlk:boss/arlecchino/fx/snd/t_pillar
execute if score #sq kn matches 24 at @s run function rlk:boss/arlecchino/fx/p/pillar {r:12}
execute if score #sq kn matches 50 at @s run function rlk:boss/arlecchino/fx/snd/t_dark
execute if score #sq kn matches 50 run effect give @a[tag=player] minecraft:blindness 1 0 true
execute if score #sq kn matches 50 run function rlk:mboss/arena/fl_ruins/look/crimson
execute if score #sq kn matches 56 as @e[type=marker,tag=rlk_kn_wisp_1,limit=1] at @s run function rlk:boss/arlecchino/fx/p/wisp_turn {c:2}
execute if score #sq kn matches 62 as @e[type=marker,tag=rlk_kn_wisp_2,limit=1] at @s run function rlk:boss/arlecchino/fx/p/wisp_turn {c:2}
execute if score #sq kn matches 70 at @s run summon minecraft:marker ~ ~7 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_prop","rlk_kn_moon"]}
execute if score #sq kn matches 70 as @e[type=marker,tag=rlk_kn_moon,limit=1] at @s run function rlk:boss/arlecchino/fx/prop/moon_halo
execute if score #sq kn matches 90 at @s run function rlk:boss/arlecchino/fx/snd/t_swap
execute if score #sq kn matches 90 at @s run function rlk:boss/arlecchino/fx/p/pillar {r:16}
execute if score #sq kn matches 110 at @s run function rlk:boss/arlecchino/fx/snd/t_legs
execute if score #sq kn matches 110 at @s run function rlk:boss/arlecchino/rig/anchor/spine
execute if score #sq kn matches 110 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/legs_burst
execute if score #sq kn matches 116 at @s run function rlk:boss/arlecchino/fx/snd/t_legs
execute if score #sq kn matches 116 at @s run function rlk:boss/arlecchino/rig/anchor/spine
execute if score #sq kn matches 116 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/legs_burst
execute if score #sq kn matches 122 at @s run function rlk:boss/arlecchino/fx/snd/t_legs
execute if score #sq kn matches 122 at @s run function rlk:boss/arlecchino/rig/anchor/spine
execute if score #sq kn matches 122 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/legs_burst
execute if score #sq kn matches 130 at @s run function rlk:boss/arlecchino/fx/snd/t_scythes
execute if score #sq kn matches 130 at @s run function rlk:boss/arlecchino/rig/anchor/hand_r
execute if score #sq kn matches 130 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/scythe_form
execute if score #sq kn matches 130 at @s run function rlk:boss/arlecchino/rig/anchor/hand_l
execute if score #sq kn matches 130 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/scythe_form
execute if score #sq kn matches 140 at @s run function rlk:boss/arlecchino/fx/snd/t_title
execute if score #sq kn matches 140 at @s run function rlk:mboss/title {title:"두 세계 불의 잔재",sub:"페르엘",color:"#C8102E"}
execute if score #sq kn matches 140 at @s run function rlk:boss/arlecchino/fx/hud/line {id:11}
execute if score #sq kn matches 150 at @s run function rlk:boss/arlecchino/fx/snd/t_launch
execute if score #sq kn matches 150 at @s run function rlk:boss/arlecchino/fx/p/leap_flare
execute if score #sq kn matches 150 run kill @e[type=marker,tag=rlk_kn_moon]
execute if score #sq kn matches 170 at @s run function rlk:boss/arlecchino/rig/look/glow/normal
execute if score #sq kn matches 180.. run scoreboard players set #sqdone kn 1
