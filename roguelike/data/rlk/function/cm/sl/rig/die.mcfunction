# 큰 슬라임 터짐 (@s = 뿌리): 부풀고 → 2칸 안의 다른 슬라임에 방전 → 작은 슬라임 셋으로 분열
function rlk:cm/sl/rig/pose/50
execute unless score #c2sldeath snd matches 1 run function rlk:cm/c2/snd/sldeath
function rlk:cm/c2/discharge
function rlk:cm/sl/split
