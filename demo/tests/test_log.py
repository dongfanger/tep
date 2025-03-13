from tep.libraries.Log import Log


def test():
    Log.logger().info('user')
    Log.sys_logger().info('sys')
