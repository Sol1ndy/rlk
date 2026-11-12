# Death (PLAN §3.3: no last words; she lowers both scythes, they dissolve into embers, she straightens, crimson flames climb her, she vanishes in a flame burst; the wisps turn white again; the rig ends hidden). @s = the body; #sq kn 1.. = the clip tick shown this game tick.
execute if score #sq kn matches 10 at @s run function rlk:boss/arlecchino/fx/snd/death_lower
execute if score #sq kn matches 30 at @s run function rlk:boss/arlecchino/rig/anchor/blade_r
execute if score #sq kn matches 30 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/embers_puff
execute if score #sq kn matches 30 at @s run function rlk:boss/arlecchino/rig/anchor/blade_l
execute if score #sq kn matches 30 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/embers_puff
execute if score #sq kn matches 70 at @s run function rlk:boss/arlecchino/fx/snd/death_flames
execute if score #sq kn matches 70 at @s run function rlk:boss/arlecchino/fx/p/death_flames
execute if score #sq kn matches 96 at @s run function rlk:boss/arlecchino/fx/snd/death_gone
execute if score #sq kn matches 96 at @s run function rlk:boss/arlecchino/fx/p/final_burst {r:20}
execute if score #sq kn matches 96 at @s run function rlk:boss/arlecchino/rig/anchor/chest
execute if score #sq kn matches 96 at @e[type=marker,tag=rlk_kn_anchor,limit=1] rotated as @s run function rlk:boss/arlecchino/fx/p/embers_puff
execute if score #sq kn matches 100 as @e[type=marker,tag=rlk_kn_wisp] at @s run function rlk:boss/arlecchino/fx/p/wisp_turn {c:1}
execute if score #sq kn matches 110 at @s run function rlk:boss/arlecchino/rig/state/hidden
execute if score #sq kn matches 110.. run scoreboard players set #sqdone kn 1
