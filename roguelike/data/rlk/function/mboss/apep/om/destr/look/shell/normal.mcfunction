# 파괴 shell: look normal (destr_shell_normal). @s = the husk.
execute on passengers if entity @s[tag=rlk_ap_om_shell] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/apep_om/destr_shell_normal"
