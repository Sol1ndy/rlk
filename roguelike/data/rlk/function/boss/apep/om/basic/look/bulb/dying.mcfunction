# 기본 bulb: look dying (basic_bulb_dying). @s = the husk.
execute on passengers if entity @s[tag=rlk_ap_om_bulb] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/apep_om/basic_bulb_dying"
