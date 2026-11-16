# 홍련일섬 준비됨 (@s = 플레이어, at 몸, hw_due: 재사용 대기가 끝난 시각): 대기 해제 · 검집에 넣는 딸깍 소리 · 번개 불꽃 4개
scoreboard players set #hwSlCd itv 0
execute unless score #k359 snd matches 1 run function rlk:snd/f429
particle minecraft:electric_spark ~ ~1.2 ~ 0.3 0.4 0.3 0.05 4
