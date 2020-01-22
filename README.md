# Daily Writing

This tiny app is for record the word number of daily writing.

此小工具用来记录每天写作的字数，激励自己写作。

## Features

* 默认统计和记录“文档”和桌面上的.md 文件的字数，可以加入其它文件夹
* 支持英文和中文字数统计
* 支持windows系统。（经过稍微修改就可以支持其它系统）
* 自动定期运行（使用windows下的管理工具“任务计划程序”）
* 在桌面上创建文件，提示当前字数和目标字数

## Acknowledge

* 本项目使用了https://blog.csdn.net/lixiaowang_327/article/details/79151163 中字数统计的函数，进行了些许修改

## TODO

* [ ] 撰写使用手册
* [ ] 使用系统配置文件，包含监视目录，目标字数
* [ ] 使用索引进行监视
* [ ] 在统计字数之前，首先验证修改时间，以此提高效率
* [ ] 不把删除的字数加和到总字数中
* [ ] 新的桌面提醒方法
* [ ] 多种文件类型支持，doc
* [ ] 统计代码行数
* [ ] 目录迭代