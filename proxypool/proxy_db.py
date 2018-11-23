"""Redis数据库操作类"""
import redis
from random import choice
from proxypool.exceptions import PoolEmptyException
from proxypool.settings import *


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """初始化"""
        # 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """添加代理，设置分数为初始值"""
        # ZSCORE key member
        # 返回有序集 key 中，成员 member 的 score 值，以字符串形式表示
        # 如果 member 元素不是有序集 key 的成员，或 key 不存在，返回 nil
        if not self.db.zscore(REDIS_KEY, proxy):
            # ZADD key score member [[score member] [score member] ...]
            # 将一个或多个 member 元素及其 score 值加入到有序集 key 当中。
            # 如果某个 member 已经是有序集的成员，那么更新这个 member 的 score 值，并通过重新插入这个 member 元素，来保证该 member 在正确的位置上。
            # 如果 key 不存在，则创建一个空的有序集并执行 ZADD 操作
            # 当 key 存在但不是有序集类型时，返回一个错误
            # 返回值：被成功添加的新成员的数量，不包括那些被更新的、已经存在的成员
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则异常"""
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            # ZREVRANGE key start stop [WITHSCORES]
            # 中返回有序集 key 中，指定区间内的成员。
            # core 值递减(从大到小)来排列。具有相同 score 值的成员按字典序的逆序(reverse lexicographical order)排列。
            # zrange递增排序；除了成员按 score 值递减的次序排列这一点外， ZREVRANGE 命令的其他方面和 ZRANGE 命令一样。
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyException

    def decrease(self, proxy):
        """代理值减分，小于最小值则删除"""
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理：%s,当前分数：%s, 减1' % (proxy, score))
            # 为有序集 key 的成员 member 的 score 值加上增量 increment
            # 可以通过传递一个负数值 increment ，让 score 减去相应的值，比如 ZINCRBY key -5 member ，就是让 member 的 score 值减去 5 。
            # 当 key 不存在，或 member 不是 key 的成员时， ZINCRBY key increment member 等同于 ZADD key increment member 。
            # 当 key 不是有序集类型时，返回一个错误。
            # score 值可以是整数值或双精度浮点数。
            # 返回值:member 成员的新 score 值，以字符串形式表示。
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """判断是否存在"""
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """将代理设置为MAX_SCORE"""
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """获取数量"""
        # ZCARD key
        # 返回有序集 key 的基数。
        # 返回值:
        # 当 key 存在且是有序集类型时，返回有序集的基数。
        # 当 key 不存在时，返回 0 。
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """获取全部代理"""
        # ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
        # 返回有序集 key 中，所有 score 值介于 min 和 max 之间(包括等于 min 或 max )的成员。
        # 有序集成员按 score 值递增(从小到大)次序排列。
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(60, 80)
    print(result)
