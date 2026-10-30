# 결정 축포 충전 1회 사용 (@s = 플레이어): 누른 순간 소모. 실제 발사(char/navia/fire)는 모션의 발사 틱에
scoreboard players remove @s nvC 1
scoreboard players set @s nvFcd 4
# 충전이 다 차 있었으면 지금부터 다음 충전 시작(재사용 대기 감소 효과 반영)
execute if score @s nvC matches 1 run scoreboard players set @s nvCT 0
scoreboard players operation @s skillCd = #nvCd tmp
function rlk:char/cd_reduce
scoreboard players operation @s nvCdE = @s skillCd
# 발사 대기: 모션 이벤트(events/navia/skill 7틱 · skill_fire 3틱)가 char/navia/fire 를 부른다
scoreboard players set @s nvShot 1
