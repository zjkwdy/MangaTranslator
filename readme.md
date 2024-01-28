# 简易漫画批量翻译器

基于 https://cotrans.touhou.ai/

环境搭建

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

准备材料

(将欲翻译漫画整个文件夹放到input),其中图片支持jpg/png

```
mkdir input
cp xxxxx input/
```

翻译配置可见`translate_all.py`

跑起来!

```
while true ;do python translate_all.py ;done #忽略所有崩溃,一直跑到完活
```



ps.没写错误处理,但是有一个简陋的断点续传,网络错误就重来,没问题的()
