"""The event logic of 홍련 (Scarlet) after the clear: ev/{roll,apply,item,buff,title,record,reset} and the FN-b reward
hook F:boss/scarlet/reward (PLAN §7.3, §7.1.4; OWNER: S3).

- ev/roll (death_start; the hook when the ending never reached it): #hrEv hr 1 item / 2 buff, #hrEvDone / #hrEvDrop 0.
  Order: the test override storage rlk:hr ev.force "item" | "buff" (tests 91 / 92) -> no duplicate (the player holds
  sword_hwamu: it_sword_hwamu >= 1 -> buff; hrMoon >= 1 -> item) -> `random value 1..1000` <= api.EVENT['item_pm'] (a
  literal: regenerate to change) -> item, else buff.
- ev/apply (seq/event at E56 through api.ev_apply(), or the hook for a cut coda): once per kill (#hrEvDone), as the
  player: ev/item = the star raised to api.EVENT['item_enh'] (items/enh_get / enh_add by id, before the item is built),
  the capacity check of F:root/give:4-5 (rlk:pinv order >= invCap -> #hrEvDrop 1: never a give into a full inventory),
  items/give {id:"sword_hwamu"}; ev/buff = hrMoon 1 (items/stat_light applies it within 2 t).
- ev/title (seq/event at E56 through api.ev_title()): the item's name / the buff's name + numbers (score components of
  api.BUFF_FP) as the title, vBig / ttlT for its 54 t.
- reward (FN-b; @s = the player, not positioned; once per kill after the reward title and the level-up, before the rift
  collapse): a missing roll, a missing grant, the pending drop at the player's body (items/drop: a ground item with
  [회수] / [판매]) + the full-inventory notice, the chat record (ev/record), then ev/reset (#hrEv* 0, ev.force removed).
The scores api.EV_FP live in objective hr and are never touched by the module cleanup; spawn and uninstall clear them.
Every text is api.EV_TEXT verbatim.
"""
import re

from . import api
from . import s3lib as S
from .s3lib import sset, fn

OBJ = api.OBJ
ID = api.ITEM_ID
T = api.EV_TEXT


def _item_name():
    """The item's display name at the granted star (= api.EV_TEXT item_title for item_enh 1)."""
    e = int(api.EVENT['item_enh'])
    name = f'[ MYTHIC ] {api.ITEM_NAME} ' + '★' * e + '☆' * (3 - e)
    if e == 1:
        assert name == T['item_title'], (name, T['item_title'])
    return name


def _buff_sub():
    """The buff subtitle as components: the text of api.EV_TEXT buff_sub with its three numbers as score components of
    api.BUFF_FP (tmp; SR sets them in load's 조절 지점), so the 'forever' scope shows its own values."""
    parts = re.split(r'\+(\d+)%', T['buff_sub'])
    nums = [int(x) for x in parts[1::2]]
    assert nums == list(api.BUFF_VALUES['run']) and len(nums) == len(api.BUFF_FP), nums
    comp = ['""']
    for i, txt in enumerate(parts[0::2]):
        lead = txt + ('+' if i < len(nums) else '')
        if i > 0:
            lead = '%' + lead
        if lead:
            comp.append(f'{{text:"{lead}",color:"#FFE08A"}}')
        if i < len(nums):
            comp.append(f'{{score:{{name:"{api.BUFF_FP[i]}",objective:"tmp"}},color:"#FFE08A"}}')
    return '[' + ','.join(comp) + ']'


LIGHT_SHADOW = -8730          # 0xFFFFDDE6: a light pink text shadow under the dark_red item name (legible on the red field)
TITLE_T = api.EV_T['black'] - api.EV_T['grant']   # 54: the event title holds E56 .. E110


def build(W):
    w = W.w
    pm = int(api.EVENT['item_pm'])
    assert 0 <= pm <= 1000
    w('ev/roll', [
        '# The event roll (PLAN §7.3.1; death_start, or the reward hook when the ending never reached it): #hrEv 1 item / 2 buff.',
        sset('#hrEv', 0), sset('#hrEvDone', 0), sset('#hrEvDrop', 0),
        f'execute if data storage {api.STORAGE} {{ev:{{force:"item"}}}} run return run {sset("#hrEv", api.EV_BRANCH["item"])}',
        f'execute if data storage {api.STORAGE} {{ev:{{force:"buff"}}}} run return run {sset("#hrEv", api.EV_BRANCH["buff"])}',
        f'execute as {S.PL} if score @s {api.ITEM_SCORE} matches 1.. run return run {sset("#hrEv", api.EV_BRANCH["buff"])}',
        f'execute as {S.PL} if score @s {api.BUFF_OBJ} matches 1.. run return run {sset("#hrEv", api.EV_BRANCH["item"])}',
        f'execute store result score #t {OBJ} run random value 1..1000',
        f'execute if score #t {OBJ} matches ..{pm} run return run {sset("#hrEv", api.EV_BRANCH["item"])}',
        sset('#hrEv', api.EV_BRANCH['buff'])])
    w('ev/apply', [
        '# The grant (seq/event at E56, or the reward hook for a cut coda; @s any): once per kill, as the player.',
        f'execute if score #hrEvDone {OBJ} matches 1 run return 0',
        f'execute unless score #hrEv {OBJ} matches 1..2 run {fn("ev/roll")}',
        sset('#hrEvDone', 1),
        f'execute if score #hrEv {OBJ} matches {api.EV_BRANCH["item"]} as {S.PL} run {fn("ev/item")}',
        f'execute if score #hrEv {OBJ} matches {api.EV_BRANCH["buff"]} as {S.PL} run {fn("ev/buff")}'])
    e = int(api.EVENT['item_enh'])
    star = []
    for i in range(e):
        star += ['scoreboard players set #enh tmp 0', f'function rlk:items/enh_get {{id:"{ID}"}}',
                 f'execute if score #enh tmp matches ..{i} run function rlk:items/enh_add {{id:"{ID}"}}']
    w('ev/item', [
        f'# The item (@s = the player): the star raised to {e} before the item is built (by id, held or not), the capacity check',
        '# of F:root/give:4-5 (a full inventory: the drop waits for the rift, #hrEvDrop 1), else items/give.']
      + star + ['execute store result score #ol tmp run data get storage rlk:pinv order',
                f'execute if score #ol tmp >= @s invCap run return run {sset("#hrEvDrop", 1)}',
                f'function rlk:items/give {{id:"{ID}"}}'])
    w('ev/buff', [f'# The buff {api.BUFF_NAME} (@s = the player): {api.BUFF_OBJ} 1 (SR: items/hook/stat_buffs, reset_one).',
                  f'scoreboard players set @s {api.BUFF_OBJ} 1'])
    name = _item_name()
    w('ev/title', [
        f'# The event title at E56 (seq/event; @s any): the item\'s display name (dark_red, a light shadow) / its notice, or the',
        f'# buff\'s name / numbers; held {TITLE_T} t (vBig / ttlT pause the F5 crosshair title).',
        'title @a[tag=player] times 6 44 4',
        f'execute if score #hrEv {OBJ} matches 1 run title @a[tag=player] subtitle {{text:"{T["item_sub"]}",color:"#E8E2D0"}}',
        f'execute if score #hrEv {OBJ} matches 1 run title @a[tag=player] title {{text:"{name}",color:"dark_red",shadow_color:{LIGHT_SHADOW}}}',
        f'execute if score #hrEv {OBJ} matches 2 run title @a[tag=player] subtitle {_buff_sub()}',
        f'execute if score #hrEv {OBJ} matches 2 run title @a[tag=player] title {{text:"{T["buff_title"]}",color:"#DDE6FF",bold:true}}',
        f'scoreboard players set @a[tag=player] vBig {TITLE_T}', f'scoreboard players set @a[tag=player] ttlT {TITLE_T}'])
    w('ev/record', [
        '# The chat record at the rift (the reward hook; @s = the player): the item\'s name, or the buff with its numbers.',
        f'execute if score #hrEv {OBJ} matches 1 run tellraw @s [{{text:"{T["chat_item"]}",color:"#FFE08A"}},{{text:"{name}",color:"dark_red"}}]',
        f'execute if score #hrEv {OBJ} matches 2 run tellraw @s {{text:"{T["chat_buff"]}",color:"#DDE6FF"}}'])
    w('ev/reset', ['# The event state gone (the end of the reward hook): #hrEv / #hrEvDone / #hrEvDrop 0, the test override removed.']
      + [sset(k, 0) for k in api.EV_FP] + [f'data remove storage {api.STORAGE} {api.EV_FORCE}'])
    w(api.REWARD_HOOK, [
        '# FN-b reward hook (mboss/sp/reward: @s = the player, not positioned; once per kill after the reward title and the level',
        '# up, before the rift collapse; no fight tick any more): the roll / the grant the coda did not reach (a /reload while',
        '# dying), the pending drop at the player (the return point is a checked floor) + its notice, the chat record, the reset.',
        f'execute unless score #hrEv {OBJ} matches 1..2 run {fn("ev/roll")}',
        f'execute unless score #hrEvDone {OBJ} matches 1 run {fn("ev/apply")}',
        f'execute if score #hrEvDrop {OBJ} matches 1 at {S.PLAYER} run function rlk:items/drop {{id:"{ID}"}}',
        f'execute if score #hrEvDrop {OBJ} matches 1 run tellraw @s {{text:"{T["chat_full"]}",color:"gray"}}',
        fn('ev/record'), fn('ev/reset')])


SERVICES = [api.Service('ev', api.EV_CLIPS, build)]
