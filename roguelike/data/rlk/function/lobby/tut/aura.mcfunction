execute store result score #t lob run data get storage rlk:chars cur.elem
scoreboard players set #elU tmp 1000
execute if score #t lob matches 1 as @e[tag=rlk_dummy,tag=rlk_tutE] run function rlk:element/attach {e:"Water"}
execute if score #t lob matches 2 as @e[tag=rlk_dummy,tag=rlk_tutE] run function rlk:element/attach {e:"Fire"}
execute if score #t lob matches 3 as @e[tag=rlk_dummy,tag=rlk_tutE] run function rlk:element/attach {e:"Water"}
execute if score #t lob matches 4..6 as @e[tag=rlk_dummy,tag=rlk_tutE] run function rlk:element/attach {e:"Fire"}
execute if score #t lob matches 7 as @e[tag=rlk_dummy,tag=rlk_tutE] run function rlk:element/attach {e:"Water"}
execute if score #t lob matches 8.. as @e[tag=rlk_dummy,tag=rlk_tutE] run function rlk:element/attach {e:"Fire"}
