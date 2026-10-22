# 기본 shield: look on (basic_shield_on). @s = the husk.
execute on passengers if entity @s[tag=rlk_ap_om_shield] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/apep_om/basic_shield_on"
