功能简介
==============
Python 渗透工具，或者渗透测试工具框架可能需要用到的组件：带结果反馈的线程池，支持大字典流式读取
以及进度保存的字典解析模块，以进程方式启动并加以监视控制与结果反馈的任务管理器，带有装饰器接口的日志
记录工具，除此之外，utils 还包含了一些有用的小工具：打印带颜色的文字，指定路径的 import 工具，
ip 计算工具，更加方便的 Python 自省工具。

线程池组件
-----------------

简介
^^^^^^^^
线程池的出现极大的方便了密集型任务的编程，在线程池组件的帮助下，一个任务密集型的程序将会极大被简化，
只需要维护一个稳定的任务队列并且定时从线程池的结果队列中获取任务反馈。

Quick Look
^^^^^^^^^^^^^^^^

.. code-block:: python

  import time
  from g3ar import ThreadPool

  def func(arg1):
    #
    # Do something intersting
    #
    time.sleep(5)
    return arg1

  pool = ThreadPool()
  pool.start()
  pool.feed(target_func=func, arg1=4)
  queue = pool.get_result_queue()
  result = queue.get()
  print(result)
  pool.stop()


这个最简单的例子，就是我们使用 ThreadPool 做的一个最简单的事情，也就是执行一个函数，然后再异步
收集结果。

我们分布来讲解这一段小代码：

.. code-block:: python

  from g3ar import ThreadPool
  def func(arg1):
    #
    # Do something intersting
    #
    time.sleep(5)
    return arg1


导入我们需要的 ThreadPool 然后并定义一个函数。

.. code-block:: python

  pool = ThreadPool()
  pool.start()

新建一个 ThreadPool 对象，然后开启线程池（start）。启动线程池之后，线程池对象会在内部启动若干
个线程，然后这些线程就会进入等待状态。当任务队列中出现任务的时候，线程就会提取任务队列中的任务，
然后执行相应的任务，把任务的执行情况放在结果队列中

.. code-block:: python

  pool.feed(target_func=func, arg1=4)

传入需要运行的函数，并且在 target_func 后输入其他的参数，例如在 func 中，arg1 是 func 的唯
一参数，因为后面必须要写出形参的名称和形参的值。

.. code-block:: python

  queue = pool.get_result_queue()
  result = queue.get()
  print(result)
  pool.stop()


通过 pool.get_result_queue()， 获取一个 Queue.Queue 对象，这个对象是 Python 内置的对象，
所以不做过多的说明，通过 queue.get() 来获取函数执行的结果。

当获取到需要的结果之后，通过 pool.stop() 来关闭线程池。

你会发现，这个线程池使用起来非常的简单，事实上，简单已经是一切了对不对？

大字典读取
-----------------

在进行 Python 渗透工具编写的过程中，我们经常需要用到各种各样的字典（当然不是用来查生词的字典），
比如你有一个 300MB 的字典，你想用它去跑密码，然后整个脚本都需要在短时间内完成，这个时候应该怎么办呢？

当然大家直到使用文件流去读取是最好不过的，但是实际上，可能你整天都在忙着渗透测试的业务并没有太多
去关注编程方面的东西，那么你难道真的就那样整个把字典加载进内存？而且还很麻烦做字典分片啊，进度
保存啊之类的基础性工作。实际上，这些工作，g3ar 都可以替你完成喔！

.. code-block:: python

  from g3ar import DictParser

  dparser = DictParser('bigdict.txt')
  for i in dparser:
    #
    # Do What you want!
    #
    pass

看！实际的使用，就这么简单，但是然后呢？我们设想一些复杂的场景：我的字典大概跑了有 2000 条，
然后临时有事情，我需要暂停下来，然后等我忙完了事情接下来再跑这个字典，那么应该怎么做呢？当然是有
好办法啦！DictParser 提供了基于 session 控制的可选进度保存操作。

首先我们假定我们有一个叫 demodict 的字典文件::

  6666123
  12341
  346
  245!#$%@#$^#
  325
  12341adfas
  asd
  re
  yq
  dahy
  ar
  r
  34
  awe
  g
  da
  haf
  dh
  ad
  s
  dasdtdassd

针对这一个字典文件，我们需要读取这个字典文件中的内容，然后并且进行进度保存，那么我们应该怎么做呢？

TAKL IS CHEAP, LET ME SHOW YOU THE CODES!

.. code-block:: python

  from g3ar import DictParser
  from g3ar.utils.print_utils import print_bar

  #
  # 创建一个 DictParser, 把 demosession 作为 session_id 传入 DictParser 对象中
  #
  dparser = DictParser(filename='demodict', session_id='demosession')

  #
  # 读取前十行：因为 DictParser 本质上是一个迭代器，所以可以使用 foreach 的形式也可以直接调用 next
  # 去获取相应的值
  #
  print_bar('GET 10 LINES')
  for i in xrange(10):
  print(dparser.next())
  print_bar('END')
  print()

  #
  # 强制保存当前字典读取的进度
  #
  dparser.force_save()

  #
  # 删除字典（自动关闭文件）
  #
  del dparser

  #
  # 重新创建一个 DictParser， 然后把之前使用的 session_id 传入，然后设置 do_continue 为 True
  # 这样得到的一个 DictParser 就是一个接着上一次读写字典进度的一个字典解析器
  #
  dparser_continue = DictParser(filename='demodict', session_id='demosession', do_continue=True)
  #
  # 那么我们现在来验证后面的字典剩下的内容是不是紧接着我们上一次保存的进度之后？
  #
  print_bar('GET NEXT ALL LINE')
  for i in dparser_continue:
  print(i)

然后上面就是我们完成保存进度使用的接口，我们查看一下最终的结果来检查是不是按照我们的期望进行工作!::

  =============================GET 10 LINES=============================
  6666123
  12341
  346
  245!#$%@#$^#
  325
  12341adfas
  asd
  re
  yq
  dahy
  =================================END=================================
  ()
  ==========================GET NEXT ALL LINE==========================
  ar
  r
  34
  awe
  g
  da
  haf
  dh
  ad
  s
  dasdtdassd

接下来我们对比一下之前我们创建的字典文件，发现确实实现字典的进度保存。那么现在，你可以使用它
去完成你想要的操作了！我觉得你现在可能已经想到它可以用在哪里了！

其他相关连接
---------------------

* `首页 <index.html>`_
* `总览 <overview.html>`_
* `功能简介 <func_quicklook.html>`_
