# 2초마다 (@s = 플레이어)
scoreboard players set #t view 0
effect give @s minecraft:invisibility infinite 0 true
attribute @s minecraft:camera_distance base set 0
execute unless score @s bowT matches 1.. run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0
# 법구(로노바): 아바타는 아무것도 들지 않는다(법구는 옆에 떠 있음)
execute if score #charN tmp matches 7..8 run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand with minecraft:air
# 불러와진 청크에 예전 아바타가 남아 있으면 지운다
execute as @e[tag=rlk_av] unless score @s avId = #avId view run kill @s
# 아바타는 경직용 팀에
team join rlk_stun @e[tag=rlk_av,team=!rlk_stun]
