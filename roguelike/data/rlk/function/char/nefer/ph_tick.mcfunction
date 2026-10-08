# 환영극 진행 (@s = 플레이어): 0 네페르 1타 · 6 네페르 2타 + 그림자 1타 · 9 그림자 2타 · 15 그림자 3타 · 19 그림자 사라짐
scoreboard players add @s nfPT 1
execute if score @s nfPT matches 2 at @e[tag=rlk_body,limit=1] run function rlk:char/nefer/ph_self {a:25,e:15,fx:104}
execute if score @s nfPT matches 8 at @e[tag=rlk_body,limit=1] run function rlk:char/nefer/ph_self {a:32,e:19,fx:105}
execute if score @s nfPT matches 8 run function rlk:char/nefer/ph_shadow {e:13,a:20}
execute if score @s nfPT matches 11 run function rlk:char/nefer/ph_shadow {e:13,a:245}
execute if score @s nfPT matches 17 run function rlk:char/nefer/ph_shadow {e:18,a:65}
execute if score @s nfPT matches 17 at @e[tag=rlk_nfsp,limit=1] run function rlk:char/nefer/shadow_fin
execute if score @s nfPT matches 21.. run function rlk:char/nefer/ph_end
