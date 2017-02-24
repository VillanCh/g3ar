# g3ar 渗透编程工具包： 极速打造渗透测试工具
完美支持： Python2  
单元测试通过： Python3

[![Build Status](https://travis-ci.org/VillanCh/g3ar.svg?branch=master)](https://travis-ci.org/VillanCh/g3ar)

## 功能概述

1. 多线程与多进程管理：
	* 线程池与多线程调用极简化
	* 异步
	* Taskbulter 对进程内的线程监控与管理
* 爆破用字典管理：
	* 支持任意大小的字典读取（大字典不再发愁）
	* 进度保存
	* 获取当前进行进度
* 日志记录器：
	* 日志管理极简化
	* 装饰器接口
	* 自动追踪函数，日志记录函数的调用，Trace，和异常情况

## 安装

### By pip

	pip install g3ar

### By easy_install

    easy_install g3ar

### By Github：

	git clone https://github.com/VillanCh/g3ar.git
  cd g3ar
	pip install -r requirements.txt
	python setup.py install

## 帮助手册与 Quick Look

查看 `docs/build/html/index.html`
