这个文件是存储di对应的json文件，文件格式为

```json
{
  "FUNCTION_TIPS_AND_MODEL": {
    "model": "HTML4",
    "tip": ""
  },
  "PARAMETERS_AND_MODEL": {
    "cvatXMLPath": [
      "file"
    ]
  }
}
```

其中FUNCTION_TIPS_AND_MODEL中是存储文件的提示提示文本的，其中model参数为提示文本的显示模式，分别为HTML4和txt，所以在书写的时候可以书写这两个参数，而tip参数则为提示文本的内容



PARAMETERS_AND_MODEL参数是参数的输入模式和对输入模式的一些设置，里面是用字典来进行存储，key为字符串类型，value则为列表类型

value中的一个参数为输入模式有5种，分别为file,dir,radio,txt,json5种模式

file后续参数：弹出框标题，默认目录，过滤字符串，默认过滤字符串（这些参数都是字符串类型）

dir后续参数：弹出框标题，默认目录（这些参数都是字符串类型）

radio后续参数：存放选项名字的列表

txt后续参数：文本输入的类型（int，float，str），文本输入框的默认长度（整型）

json后续参数：没有