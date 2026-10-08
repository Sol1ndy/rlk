# 떨어져 죽은 몹의 보상 (@s = 몹, 위치 = 플레이어의 안전한 자리). combat/apply 의 처치 부분과 같다
function rlk:combat/heal_orb_roll
function rlk:combat/kill_xp
function rlk:combat/gold_drop
execute if score #charN tmp matches 2 run function rlk:char/yoimiya/aur_move
execute if score #charN tmp matches 5 run function rlk:char/arlecchino/dir_death
