import logging
def log():
    if len(logging.getLogger().handlers) > 0:
        return logging.getLogger()
    # 创建一个logger
    logger = logging.getLogger()
    # Log等级总开关,低于此级别的都不会记录
    logger.setLevel(logging.DEBUG)
    # 自定义log目录
    logfile = './logs.log'
    # 创建一个handler，用于写入日志文件
    filehandler=logging.FileHandler(filename=logfile,encoding='utf-8')
    # 用于写到file的等级开关
    filehandler.setLevel(logging.DEBUG)
    # 再创建一个handler,用于输出到控制台
    consolehandler=logging.StreamHandler()
    # 输出到console的log等级的开关
    consolehandler.setLevel(logging.INFO)
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(thread)s - %(levelname)s - %(message)s')
    filehandler.setFormatter(formatter)
    consolehandler.setFormatter(formatter)
    # 将logger添加到handler里面
    logger.addHandler(filehandler)
    logger.addHandler(consolehandler)
    return logger
