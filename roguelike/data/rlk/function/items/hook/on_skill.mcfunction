# 스킬 사용 시 아이템 효과 (@s = 플레이어, at @s). combat/on_skill 에서 호출
# 데모노미콘: 스킬 4회마다 강력한 마법데미지
execute if score @s it_demonomicon matches 1.. run scoreboard players add @s bookPages 1
execute if score @s it_demonomicon matches 1.. if score @s bookPages matches 4.. at @e[tag=rlk_body,limit=1] run function rlk:items/proc/demono_proc
# 고통 & 절망: 스킬 사용 시 공속/이속 스택
execute if score @s it_pain_despair matches 1.. run function rlk:items/proc/pd_gain
