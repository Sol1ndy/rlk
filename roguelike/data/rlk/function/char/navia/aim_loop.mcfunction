# 조준 진입 모션이 끝났는데 아직 누르고 있음 (@s = 플레이어, events/navia/skill_aim_in 에서): 반복 조준 모션으로
# #nvKeep 이 있는 동안 control/cancel 은 조준을 취소하지 않는다(같은 조준의 다음 모션)
scoreboard players set #nvKeep tmp 1
function rlk:char/motion/start {char:"navia",clip:"skill_aim"}
scoreboard players set #nvKeep tmp 0
