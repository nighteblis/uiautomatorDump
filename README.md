# uiautomatorDump
use adb &amp; uiautomator dump  to automate test
This is sample to show use adb & uiautomator dump to test.  
No other software need to be installed except two of below.

1. adb installed
2. your device or emulator support uiautomator.  

原理:

利用uiautomator dump 出来当前页面的所有元素, 保存为一个xml文件. 根据xml解析ui元素后, 获取到坐标,通过adb shell input 命令来进行ui测试.
解析xml文件可以用xml.etree.ElementTree来进行.  这样我们可以快速开发脚本来进行android ui 测试. 
