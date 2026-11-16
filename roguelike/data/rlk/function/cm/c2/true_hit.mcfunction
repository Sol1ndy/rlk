# @s 에게 진짜 피해 #c2zd (combat/apply 경로: 처치 · 보상 · 숫자). combat/apply 안에서는 부르지 않는다(cm/clean 에서만)
scoreboard players add #hitLanded tmp 0
scoreboard players operation #c2SaveHL tmp = #hitLanded tmp
scoreboard players add #basic itv 0
scoreboard players operation #c2SaveB tmp = #basic itv
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = #c2zd tmp
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #basic itv 0
scoreboard players set #bowHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #tfm tmp 1
scoreboard players set #trueDmg tmp 1
function rlk:combat/apply
scoreboard players set #trueDmg tmp 0
scoreboard players set #tfm tmp 0
scoreboard players operation #hitLanded tmp = #c2SaveHL tmp
scoreboard players operation #basic itv = #c2SaveB tmp
