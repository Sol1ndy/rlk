# @s = a new aux made with #auxHbY mb (aux/setup after mob/setup, cm.md 13.12): its HP-bar passengers (mob/hb_spawn: bar,
# fill, number at 0.25 b, level 0.43 b, icon 0.82 b) moved up by #auxHbY tenths of a block (negative = down).
scoreboard players operation #t mb = #auxHbY mb
scoreboard players operation #t mb *= #c10 mb
scoreboard players add #t mb 25
execute on passengers if entity @s[tag=rlk_hb_bg] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
execute on passengers if entity @s[tag=rlk_hb_fg] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
execute on passengers if entity @s[tag=rlk_hb_num] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
scoreboard players add #t mb 18
execute on passengers if entity @s[tag=rlk_hb_lv] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
scoreboard players add #t mb 39
execute on passengers if entity @s[tag=rlk_hb_icon] store result entity @s transformation.translation[1] float 0.01 run scoreboard players get #t mb
