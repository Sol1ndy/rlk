"""The event logic of 홍련 (Scarlet) after the clear: ev/{roll,apply,item,buff,title,record,reset} and the FN-b reward
hook F:boss/scarlet/reward (PLAN §7.3). OWNER: S3.

D0 stub: S3 replaces this file. Contract: SERVICES = [...] (non-empty once ev/** exists) built with
W = api.Writer('S3', api.OWN['S3']) into ev/** and reward only; names api.EV_CALLS, api.EV_FP, api.EV_FORCE,
api.TAGS['ev'], api.EVENT, api.ITEM_ID, api.BUFF_OBJ, api.BUFF_FP. While SERVICES is empty api.ev_apply() /
api.ev_title() return '' so seq/event (S2b) loads without these files.
"""
from . import api  # noqa: F401

SERVICES = []
