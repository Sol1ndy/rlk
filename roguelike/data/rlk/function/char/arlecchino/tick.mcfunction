# 아를레키노 매 틱 (@s = 플레이어, at 몸): 붉은 죽음의 가면(생명의 계약이 최대 체력의 #arMaskMin% 이상) · 핏값 표시
function rlk:player/bol/pct
scoreboard players set #t1 tmp 0
execute if score #bolNow tmp >= #arMaskMin tmp run scoreboard players set #t1 tmp 1
execute if score #t1 tmp matches 1 unless score @s arM matches 1 run function rlk:char/arlecchino/mask_on
execute if score #t1 tmp matches 0 if score @s arM matches 1 run function rlk:char/arlecchino/mask_off
execute if score @s arM matches 1 run particle minecraft:dust{color:[0.88f,0.2f,0.3f],scale:0.9f} ~ ~0.9 ~ 0.3 0.5 0.3 0 1
execute store result score #ynow tmp run time query gametime
# 핏값 표식(디스플레이): 새로 생긴 건 키우고, 끝난 건 지운다
execute if entity @e[tag=rlk_armk_new,limit=1] run function rlk:char/arlecchino/mk_grow
function rlk:char/arlecchino/mk_clean
# 재가 된 만상: 사라져 있는 중
execute if score @s arSk matches 1.. run function rlk:char/arlecchino/skill_wait