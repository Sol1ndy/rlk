# 캐릭터 선택 (@s = 플레이어). 사용: /function rlk:char/select {id:"lumine"}
$execute unless data storage rlk:chars registry.$(id) run return run tellraw @s [{"text":"[캐릭터] ","color":"red"},{"text":"없는 캐릭터: $(id)","color":"gray"}]
$data modify storage rlk:chars cur set value {id:"$(id)"}
function rlk:char/load_cur with storage rlk:chars cur
function rlk:char/player_init
# 핫바/정보 아이템 다시 만들기
clear @s *[minecraft:custom_data~{rlk_ui:{}}]
clear @s *[minecraft:custom_data~{rlk_char:1b}]
tellraw @s [{"text":"[캐릭터] ","color":"gold","bold":true},{"nbt":"cur.info.name","storage":"rlk:chars","color":"white","bold":false},{"text":" 선택","color":"gray","bold":false}]
# 숄더뷰 아바타: 새 캐릭터의 스킨으로 + 손에 든 무기를 곧 다시 복사
execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/reskin with storage rlk:chars cur.info
# 스커크는 뱀의 계략 0에서 시작
execute if score #charN tmp matches 3 run scoreboard players set @s energy 0
