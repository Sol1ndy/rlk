# strike clock 15
# the trailing vertical crescent at the end of the swoop (H), a teal underlay; a second swish
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11h,limit=1] positioned ~ ~0.8 ~ run function rlk:mboss/butterfly/fx/p/wing_flare
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11h,limit=1] positioned ^ ^0.8 ^-0.1 run function rlk:mboss/butterfly/fx/card {kind:"cres_lime",pos:"~ ~0.2 ~",rot:"~ -90",bb:"fixed",roll:90,spin:-60,s0:3.7,s1:5.7,move:"0f,0f,0f",life:7,fade:3,col:2322810}
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.17
playsound minecraft:block.azalea_leaves.break hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
function rlk:mboss/butterfly/wx/u/fwd {d:0.12}
