# Intro (PLAN §3: hang in the cables, drop, lie, push up, rise, cape, hair, visor, skull, draw, ignite, stance). @s = the body; #sq tk 1.. = the clip tick shown this game tick.
execute if score #sq tk matches 0 at @s run function rlk:boss/tachy/fx/snd/hang_amb
execute if score #sq tk matches 0 at @s run function rlk:boss/tachy/fx/p/ambient_dust
execute if score #sq tk matches 10 at @s run function rlk:boss/tachy/fx/snd/chain_step
execute if score #sq tk matches 22 at @s run function rlk:boss/tachy/fx/snd/chain_step
execute if score #sq tk matches 30 at @s run function rlk:boss/tachy/fx/snd/cable_snap
execute if score #sq tk matches 33 at @s run function rlk:boss/tachy/fx/snd/cable_snap
execute if score #sq tk matches 36 at @s run function rlk:boss/tachy/fx/snd/cable_snap
execute if score #sq tk matches 42 at @s run function rlk:boss/tachy/fx/snd/body_land
execute if score #sq tk matches 42 at @s run function rlk:boss/tachy/fx/p/dust_ring {r:30}
execute if score #sq tk matches 48 at @s run function rlk:boss/tachy/fx/snd/heartbeat
execute if score #sq tk matches 56 at @s run function rlk:boss/tachy/fx/snd/heartbeat
execute if score #sq tk matches 62 at @s run function rlk:boss/tachy/fx/snd/servo
execute if score #sq tk matches 74 at @s run function rlk:boss/tachy/fx/snd/armor
execute if score #sq tk matches 96 at @s run function rlk:boss/tachy/fx/snd/bulb
execute if score #sq tk matches 108 at @s run function rlk:boss/tachy/fx/snd/cape_gust
execute if score #sq tk matches 108 at @s run function rlk:boss/tachy/fx/p/ambient_dust
execute if score #sq tk matches 116 at @s run function rlk:boss/tachy/fx/snd/hair
execute if score #sq tk matches 126 at @s run function rlk:boss/tachy/fx/snd/visor_close
execute if score #sq tk matches 136 at @s run function rlk:boss/tachy/fx/snd/skull_ignite
execute if score #sq tk matches 142 at @s run function rlk:boss/tachy/fx/snd/sword_draw
execute if score #sq tk matches 156 run function rlk:mboss/title {title:"타키",sub:"잠식된 제7공수대원",color:"#F2C230"}
execute if score #sq tk matches 156 at @s run function rlk:boss/tachy/fx/snd/blade_ignite
execute if score #sq tk matches 156 at @s run function rlk:boss/tachy/fx/p/ignite_blade
execute if score #sq tk matches 170 at @s run function rlk:boss/tachy/fx/snd/stance
execute if score #sq tk matches 170 at @s run function rlk:boss/tachy/fx/p/ember_burst
execute if score #sq tk matches 170 at @s run function rlk:boss/tachy/rig/prop/clear
execute if score #sq tk matches 184.. run scoreboard players set #sqdone tk 1
