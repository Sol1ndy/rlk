# 방패 파괴: 1.5초 경직, 방패가 손에서 사라짐
scoreboard players set @s cmSh 0
function rlk:cm/sh/rig/break
scoreboard players operation #cid tmp = @s cmId
function rlk:cm/cancel
scoreboard players set @s cmT 0
function rlk:mob/stun
effect give @s minecraft:slowness 2 250 true
scoreboard players set @s stunT 30
execute as @e[tag=rlk_cmv,distance=..5] if score @s cmId = #cid tmp run item replace entity @s weapon.mainhand with minecraft:air
execute on passengers if entity @s[tag=rlk_cmshbar] run kill @s
particle minecraft:block{block_state:"minecraft:iron_block"} ~ ~1.3 ~ 0.4 0.4 0.4 0.1 25
execute unless score #k94 snd matches 1 run function rlk:snd/f101
summon minecraft:text_display ~ ~2.6 ~ {billboard:"center",Tags:["dmgText"],background:0,shadow:true,alignment:"center",see_through:true,brightness:{sky:15,block:15},text:{text:"방패 파괴!",color:"#9FD8FF",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]}}
