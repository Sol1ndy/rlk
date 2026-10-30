# Show the ring overlay (riding @s, the husk). Idempotent.
function rlk:boss/apep/om/nurt/ring/off
tag @s add rlk_ap_om_v
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_ring","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/nurt_ring_on"}}}
execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new] run ride @s mount @e[tag=rlk_ap_om_v,limit=1]
tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new
tag @s remove rlk_ap_om_v
execute rotated as @s on passengers if entity @s[tag=rlk_ap_om_ring] run rotate @s ~ 0
