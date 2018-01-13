# check daily report
Automatically check whether the daily report has sent and reminding the unsent.  
  
### how to use?  
add crontab task like "*/15 20 * * * python check_daily_report.py"  

### description
检查每日邮箱标题里含有“\_日报\_”字段的邮件，21点前发短信，21点后打电话，提醒未发送的人。  

短信和电话通道用的是linkedsee云通道，详情戳[Linkedsee](https://www.linkedsee.com)。

自己日常需要，老是提醒别人很麻烦，就写了这么一个脚本，其中邮件格式和通道之类的都可根据自己需要自行替换。
