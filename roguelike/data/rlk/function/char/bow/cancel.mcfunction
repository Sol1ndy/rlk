# 조준 끝(발사·취소 공통): 상태 정리 + 활을 원래 모양으로
scoreboard players set @s bowT 0
scoreboard players set @s bowSt 0
scoreboard players set @s bowK 0
scoreboard players set @s bowPm -1
scoreboard players set #bowChg tmp 0
scoreboard players reset 염초화살 stacks
attribute @s minecraft:movement_speed modifier remove rlk:bow_aim
execute if items entity @s hotbar.0 *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run item modify entity @s hotbar.0 {type:"minecraft:set_components",components:{"minecraft:item_model":"minecraft:bow"}}
execute if entity @e[tag=rlk_av,limit=1] run item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0
