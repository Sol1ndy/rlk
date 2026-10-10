# 설정 오브젝트 이름표에 지금 값
function rlk:lobby/set/cfg
execute if score #on view matches 1 if score #vmode view matches 1 run data modify entity @e[tag=rlk_lk20,limit=1] text set value {"text": "숄더뷰", "color": "#D0D0D0"}
execute if score #on view matches 1 if score #vmode view matches 2 run data modify entity @e[tag=rlk_lk20,limit=1] text set value {"text": "3인칭 (F5 필요)", "color": "#D0D0D0"}
execute unless score #on view matches 1 run data modify entity @e[tag=rlk_lk20,limit=1] text set value {"text": "1인칭", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{dist:0} run data modify entity @e[tag=rlk_lk21,limit=1] text set value {"text": "가까이", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{dist:1} run data modify entity @e[tag=rlk_lk21,limit=1] text set value {"text": "보통", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{dist:2} run data modify entity @e[tag=rlk_lk21,limit=1] text set value {"text": "멀리", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{side:0} run data modify entity @e[tag=rlk_lk22,limit=1] text set value {"text": "캐릭터가 왼쪽", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{side:1} run data modify entity @e[tag=rlk_lk22,limit=1] text set value {"text": "캐릭터가 오른쪽", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{h:0} run data modify entity @e[tag=rlk_lk23,limit=1] text set value {"text": "낮게", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{h:1} run data modify entity @e[tag=rlk_lk23,limit=1] text set value {"text": "보통", "color": "#D0D0D0"}
execute if data storage rlk:lobby cfg{h:2} run data modify entity @e[tag=rlk_lk23,limit=1] text set value {"text": "높게", "color": "#D0D0D0"}
execute if data storage rlk:view opt{smooth:0} run data modify entity @e[tag=rlk_lk24,limit=1] text set value {"text": "0틱 (빠름)", "color": "#D0D0D0"}
execute if data storage rlk:view opt{smooth:1} run data modify entity @e[tag=rlk_lk24,limit=1] text set value {"text": "1틱", "color": "#D0D0D0"}
execute if data storage rlk:view opt{smooth:2} run data modify entity @e[tag=rlk_lk24,limit=1] text set value {"text": "2틱", "color": "#D0D0D0"}
execute if data storage rlk:view opt{smooth:3} run data modify entity @e[tag=rlk_lk24,limit=1] text set value {"text": "3틱 (가장 부드러움)", "color": "#D0D0D0"}
execute if data storage rlk:view opt{lead:0} run data modify entity @e[tag=rlk_lk25,limit=1] text set value {"text": "끔", "color": "#D0D0D0"}
execute if data storage rlk:view opt{lead:1} run data modify entity @e[tag=rlk_lk25,limit=1] text set value {"text": "1틱", "color": "#D0D0D0"}
execute if data storage rlk:view opt{lead:2} run data modify entity @e[tag=rlk_lk25,limit=1] text set value {"text": "2틱", "color": "#D0D0D0"}
execute if data storage rlk:view opt{lead:3} run data modify entity @e[tag=rlk_lk25,limit=1] text set value {"text": "3틱", "color": "#D0D0D0"}
data modify entity @e[tag=rlk_lk26,limit=1] text set value {"text": "1개 (사파이어로 해금 예정)", "color": "#D0D0D0"}

# F5 위쪽 시점에는 좌우·부드러움·회전 예측이 필요 없음
execute if score #on view matches 1 if score #vmode view matches 2 run data modify entity @e[tag=rlk_lk22,limit=1] text set value {"text": "F5 시점에서는 쓰지 않음", "color": "#D0D0D0"}
execute if score #on view matches 1 if score #vmode view matches 2 run data modify entity @e[tag=rlk_lk24,limit=1] text set value {"text": "F5 시점에서는 쓰지 않음", "color": "#D0D0D0"}
execute if score #on view matches 1 if score #vmode view matches 2 run data modify entity @e[tag=rlk_lk25,limit=1] text set value {"text": "F5 시점에서는 쓰지 않음", "color": "#D0D0D0"}