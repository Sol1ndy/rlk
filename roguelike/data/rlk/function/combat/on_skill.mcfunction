# 스킬 사용 시 호출 (@s = 플레이어, at @s). 원소전투 스킬·원소폭발 발동 때 char/cast_* 가 부른다
# 스킬 데미지를 줄 때는 combat/apply 호출 전에 '#skillDmg tmp' 를 1로 설정한다(금단의 도서 페이지 획득 등에 사용).
function rlk:items/hook/on_skill
# 휘두르던 평타는 끝난다: 남은 평타 간격 동안 걷기를 늦추거나 점프를 막지 않는다(player/swing/cut)
function rlk:player/swing/cut
