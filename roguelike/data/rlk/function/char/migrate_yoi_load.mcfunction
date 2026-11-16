# 11-10 요이미야(활) 삭제 — 그녀로 저장된 월드 옮기기, 저장소 쪽 (load 의 char/setup 에서 load_cur 전에; 플레이어가 없어도 됨)
# 지금 캐릭터가 요이미야면 루미네로. 플레이어 쪽 정리(옛 활 무기 · 아바타 스킨 · 조준 감속)는 접속한 플레이어의 틱에서 한 번(char/migrate_yoi)
execute if data storage rlk:chars cur{id:"yoimiya"} run data modify storage rlk:mig yoi set value 1b
execute if data storage rlk:chars cur{id:"yoimiya"} run data modify storage rlk:chars cur set value {id:"lumine"}
execute if data storage rlk:config {start_char:"yoimiya"} run data modify storage rlk:config start_char set value "lumine"
# 남아 있는 레벨 업 선택지 · 돌아갈 때 떨굴 목록에서 그녀의 캐릭터 카드(char_yoimiya)를 뺀다(바닥에 떨어진 것은 load 가 드롭 아이템을 모두 치움)
execute if data storage rlk:lvpick {choices:["char_yoimiya"]} run function rlk:char/migrate_yoi_list {l:"choices"}
execute if data storage rlk:lvpick {dropq:["char_yoimiya"]} run function rlk:char/migrate_yoi_list {l:"dropq"}
