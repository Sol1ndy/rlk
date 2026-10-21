# 포식성 jaw: look idle (pred_jaw_idle). @s = the husk.
execute on passengers if entity @s[tag=rlk_ap_om_jaw] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/apep_om/pred_jaw_idle"
