class PoolEmptyException(Exception):
    def __init__(self):
        # 执行父类的构造方法
        # Exception.__init__(self)
        super().__init__(self)

    def __str__(self):
        # repr() 函数将对象转化为供解释器读取的形式
        # repr(object)
        # object -- 对象
        # 返回一个对象的 string 格式
        return repr('代理池为空')
