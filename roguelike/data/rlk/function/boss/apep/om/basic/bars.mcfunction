# FN-29 fallback: move the rlk_hb_* HP-bar passengers of @s (the husk) so the bar sits 1.6 b above its feet.
execute on passengers if entity @s[tag=rlk_hb_bg] run data merge entity @s {transformation:{translation:[-0.8f,-.4f,0f]}}
execute on passengers if entity @s[tag=rlk_hb_fg] run data merge entity @s {transformation:{translation:[-0.8f,-.4f,0.01f]}}
execute on passengers if entity @s[tag=rlk_hb_num] run data merge entity @s {transformation:{translation:[0f,-.4f,0.06f]}}
execute on passengers if entity @s[tag=rlk_hb_lv] run data merge entity @s {transformation:{translation:[0f,-.22f,0.06f]}}
execute on passengers if entity @s[tag=rlk_hb_icon] run data merge entity @s {transformation:{translation:[0f,.17f,0.06f]}}
