# FN-29 fallback: move the rlk_hb_* HP-bar passengers of @s (the husk) so the bar sits 2.8 b above its feet.
execute on passengers if entity @s[tag=rlk_hb_bg] run data merge entity @s {transformation:{translation:[-0.8f,.8f,0f]}}
execute on passengers if entity @s[tag=rlk_hb_fg] run data merge entity @s {transformation:{translation:[-0.8f,.8f,0.01f]}}
execute on passengers if entity @s[tag=rlk_hb_num] run data merge entity @s {transformation:{translation:[0f,.8f,0.06f]}}
execute on passengers if entity @s[tag=rlk_hb_lv] run data merge entity @s {transformation:{translation:[0f,.98f,0.06f]}}
execute on passengers if entity @s[tag=rlk_hb_icon] run data merge entity @s {transformation:{translation:[0f,1.37f,0.06f]}}
