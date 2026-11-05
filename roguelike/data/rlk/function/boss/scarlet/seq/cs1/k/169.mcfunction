# cs1 at #sq 169 (@s = the body).
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.3 ~ facing entity @s feet rotated ~ 0 run function rlk:boss/scarlet/fx/p/scarlet_line {len:600,yaw:90,roll:13}
function rlk:boss/scarlet/fx/hud/ovl {g:"red_tint",in:0,hold:4,out:20}
function rlk:boss/scarlet/fx/snd/iai_slash
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"split"}
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/petal_burst {r:20}
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/clash_spark
