# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如果没有，为None
REDIS_PASSWORD = '12345'

# 有序集合的key
REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODE = [200, 302]

# 代理池数量上限
POOL_UPPER_LIMIT = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '127.8.8.1'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLE = True
API_ENABLE = True

# 最大批测试量
BATCH_TEST_SIZE = 10
