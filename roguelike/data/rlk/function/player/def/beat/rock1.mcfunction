# @s = 리그 부품, at @s rotated ~ 0: 발을 축으로 뒤로 16도(display 의 pitch 는 모델 전체를 기울인다), 0.2칸 뒤 · 0.06칸 위(앞쪽 부품이 바닥 밑으로 가지 않게)
tp @s ^ ^0.06 ^-0.2 ~ -16
tag @s add rlk_bt_rk
