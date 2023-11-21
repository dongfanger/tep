import os.path
import time

from loguru import logger

from tep.libraries.Config import Config


class Log:
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    log_dir = os.path.join(Config.BASE_DIR, "log")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    @staticmethod
    def logger():
        logger.add(os.path.join(Log.log_dir, "{}.log".format(Log.current_time)), filter=lambda record: record["extra"].get("name") == "user")
        log = logger.bind(name="user")
        return log

    @staticmethod
    def sys_logger():
        logger.add(os.path.join(Log.log_dir, "sys_{}.log".format(Log.current_time)), filter=lambda record: record["extra"].get("name") == "sys")
        log = logger.bind(name="sys")
        return log
