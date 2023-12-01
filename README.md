[关键字驱动框架教程](https://dongfanger.gitee.io/blog/%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE/001-%E3%80%90%E6%A1%86%E6%9E%B6%E3%80%91%E5%85%B3%E9%94%AE%E5%AD%97%E9%A9%B1%E5%8A%A8%E6%A1%86%E6%9E%B6.html)

教程会在每月底发布版本后进行更新，如果热修复版本发布，也会进行更新。

🌟更新日志🌟

- ✅V2.1.2
  - 优化Har，支持指定目录，按增量/全量转换pytest用例
- V2.1.1
  - HAR包转换pytest用例功能纳入脚手架，主推，内容写入教程“快速入门”章节
  - 脚手架.gitignore文件后缀问题修复
- V2.1.0
  - 支持HTTP/2协议，httpx库实现
  - 支持HAR包转换为pytest用例，支持HTTP1和HTTP2协议
  - 基于HAR包的回放对比，字段对比输出TXT，文本对比输出HTML
  - 自定义日志对象，logger和sys_logger输出到用户/系统不同文件
  - 支持接口重试，CODE码/异常匹配，超时设置等，tenacity库实现
- V2.0.1 cli修改，查看版本`tep -V`，V大写，创建脚手架`tep new demo`，使用new
- V2.0.0 tep关键字驱动框架
- V1.0.0 tep小工具完整教程
- V0.2.3 tep小工具首次开源