from enum import Enum
from typing import Dict, Optional

DOMAIN = "loock_lock_extend"

class LockState(Enum):
    """智能门锁状态枚举"""
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    DOOR_OPEN = "door_open"
    DOOR_AJAR = "door_ajar"
    
    def __str__(self) -> str:
        return self.value
    
    def friendly_name(state) -> str:
        """返回状态的友好名称"""
        friendly_names = {
            LockState.LOCKED: "已上锁",
            LockState.UNLOCKED: "已解锁", 
            LockState.DOOR_OPEN: "门已开启",
            LockState.DOOR_AJAR: "门虚掩"
        }
        return friendly_names.get(state, "未知状态")


class StateRange:
    """状态码范围定义"""
    def __init__(self, start: int, end: int, state: LockState):
        self.start = start
        self.end = end
        self.state = state
    
    def contains(self, code: int) -> bool:
        """检查状态码是否在此范围内"""
        return self.start <= code <= self.end
    
    def __repr__(self) -> str:
        return f"StateRange({self.start}-{self.end}: {self.state.value})"


# 状态码范围配置 - 更语义化和易维护
STATE_RANGES = [
    StateRange(16, 28, LockState.LOCKED),      # 锁定状态范围
    StateRange(32, 44, LockState.UNLOCKED),    # 解锁状态范围
    StateRange(48, 60, LockState.DOOR_OPEN),   # 门开启状态范围
    StateRange(64, 76, LockState.DOOR_AJAR),   # 门虚掩状态范围
]


class StateMapper:
    """状态映射器 - 提供更优雅的状态查询API"""
    
    def __init__(self, ranges: list[StateRange]):
        self.ranges = ranges
        # 缓存映射表以提高性能
        self._cache: Dict[int, LockState] = {}
        self._build_cache()
    
    def _build_cache(self) -> None:
        """构建状态码缓存映射表"""
        for range_obj in self.ranges:
            for code in range(range_obj.start, range_obj.end + 1, 4):  # 按4递增
                self._cache[code] = range_obj.state
    
    def get_state(self, code: int) -> Optional[LockState]:
        """根据状态码获取状态"""
        return self._cache.get(code)
    
    def get_state_str(self, code: int) -> Optional[str]:
        """根据状态码获取状态字符串"""
        state = self.get_state(code)
        return state.value if state else None
    
    def is_locked(self, code: int) -> bool:
        """检查是否为锁定状态"""
        return self.get_state(code) == LockState.LOCKED
    
    def is_unlocked(self, code: int) -> bool:
        """检查是否为解锁状态"""
        return self.get_state(code) == LockState.UNLOCKED
    
    def is_door_open(self, code: int) -> bool:
        """检查门是否开启"""
        return self.get_state(code) == LockState.DOOR_OPEN
    
    def is_door_ajar(self, code: int) -> bool:
        """检查门是否虚掩"""
        return self.get_state(code) == LockState.DOOR_AJAR
    
    def get_all_codes_for_state(self, state: LockState) -> list[int]:
        """获取指定状态的所有状态码"""
        return [code for code, cached_state in self._cache.items() 
                if cached_state == state]
    
    def get_state_summary(self) -> Dict[str, list[int]]:
        """获取状态摘要信息"""
        summary = {}
        for state in LockState:
            summary[state.value] = self.get_all_codes_for_state(state)
        return summary


# 全局状态映射器实例
state_mapper = StateMapper(STATE_RANGES)

# 向后兼容的STATE_MAP
STATE_MAP = state_mapper._cache
# 转换为字符串值以保持向后兼容
STATE_MAP = {code: state.value for code, state in STATE_MAP.items()}