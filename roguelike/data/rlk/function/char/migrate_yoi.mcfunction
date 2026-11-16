# 11-10 요이미야(활) 삭제 — 그녀로 저장된 플레이어 옮기기, 플레이어 쪽 (@s = 플레이어; player/tick 에서 rlk:mig yoi 가 있을 때 한 번)
# 저장소의 지금 캐릭터는 load 가 이미 루미네로 바꿨다(char/migrate_yoi_load). 서버가 다시 켜지면 load 는 플레이어가 들어오기 전에 돌아
# load_cur 의 clear @a 가 옛 활 무기 · 캐릭터 정보 아이템을 못 지우므로, 여기서 루미네를 다시 골라 지우고 다시 만든다(아바타 스킨 포함)
data remove storage rlk:mig yoi
function rlk:char/select {id:"lumine"}
# 다시 고르기의 player_init 이 하지 않는 그녀의 흔적(날아가는 화살은 player_init 이 모두 지움): 활 조준 감속 · 사이드바 줄 · 바닥의 캐릭터 카드
attribute @s minecraft:movement_speed modifier remove rlk:bow_aim
scoreboard players reset 염초정화 stacks
scoreboard players reset 소매불 stacks
scoreboard players reset 염초화살 stacks
execute as @e[type=minecraft:item,tag=rlk_ditem] if items entity @s contents *[minecraft:custom_data~{rlk_ditem:{id:"char_yoimiya"}}] run function rlk:char/migrate_yoi_drop
