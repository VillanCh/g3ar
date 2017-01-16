什么是 g3ar？如何安装？
================================
作为一个网络安全爱好者的你，喜欢搞一些奇怪的事情？但是苦于自己的 Python 编程实在是太糟糕了
，想要的东西都不会写。比如你早就想要个可以很快的调度多线程的东西了？
不用每次遍历 + 单线程去解决一些事情。或者说你很烦为你的工具去添加日志，
因为整个流程在关键地方打日志（处理异常）繁琐到爆炸会让人崩溃的。
或者说你很讨厌一些爆破工具只能加载小型的字典，但是面对上百兆的字典，
你无能为力……

g3ar 就是这样一个模块：专门为你解决你在进行奇奇怪怪编程中的“小麻烦”：例如，
你有更方便的可以收集结果的线程池，并且还能监视你的任务执行成功还是失败，而不必每次为
了多线程而烦恼；甚至说你还可以通过 g3ar 中的一个叫 TaskBulter 去启动真正的进程，
然后去监控进程中的线程存活性（比如关键线程的工作状况？当前进程有多少存活的线程？）……
当然，强大的 g3ar 的功能远远不止如此。

作者
-------
v1ll4n

作者是一个不折不扣的网络安全狂热爱好者。

特别鸣谢与赞助列表
-------------------------
Fugitiv3

Saferman

Stardust

TB

HQ

依赖问题与环境说明
------------------------------------------------------
推荐使用 Python2.7 +，
但是 Python3 也做了一定适配，基本可以正常运行。

.. code-block:: bash

  colorama==0.3.7
  decorator==4.0.10
  IPy==0.83
  ipython==5.1.0
  ipython-genutils==0.1.0
  pexpect==4.2.1
  pickleshare==0.7.4
  prompt-toolkit==1.0.9
  ptyprocess==0.5.1
  Pygments==2.1.3
  simplegeneric==0.8.1
  six==1.10.0
  traitlets==4.3.1
  wcwidth==0.1.7


安装方法
---------------------------------------------------------
通过 pip 或者 easy_install 安装（以下命令任意选择一个都可以）

.. code-block::  bash

  pip install g3ar
  easy_install g3ar

通过 github 安装：

.. code-block:: bash

  git clone https://github.com/VillanCh/g3ar.git
  cd g3ar
  python setup.py install


其他相关连接
--------------------------------------------------

* `首页 <index.html>`_
* `总览 <overview.html>`_
* `功能简介 <func_quicklook.html>`_
