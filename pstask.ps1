###########################
# 任务描述：
# 从PowerShell在线教程页面抓取所有的HTML页面，
# 并下载保存至当前html子目录。
############################
 
# 全局配置
[int]$MaxJobCount=5
[string]$OutputDir=  (mkdir 'Html' -Force).FullName
 
# 生成任务
$request=Invoke-WebRequest 'http://www.pstips.net/powershell-online-tutorials.html' -UseBasicParsing
$links = $request.Links | where { $_.href.endswith('.html') } | select -ExpandProperty href
 
#将任务存储到线程安全的队列
$taskQueue = New-Object  'System.Collections.Concurrent.ConcurrentQueue[string]'
$links | foreach {
 $taskQueue.Enqueue($_)
}
 
#函数：从队列执行任务
function Run-TaskFromQueue{
 if($taskQueue.Count -gt 0)
 {
  $link=[string]::Empty
  #尝试从队列中出列一个任务
  if($taskQueue.TryDequeue([ref]$link))
  {
     #启动一个Job来执行任务
     $task = Start-Job -ScriptBlock {
        param([uri]$url,$OutputDir)
 
        #下载和保存页面
        Invoke-RestMethod $url | Out-File "$OutputDir\$($url.Segments[-1])" -Force
     } -ArgumentList $link,$OutputDir
  
     # 注册一个事件订阅，当当前任务结束后，开始执行队列中的下一个任务
     Register-ObjectEvent -InputObject $task -EventName StateChanged -Action {
      Run-TaskFromQueue
      Unregister-Event $eventsubscriber.SourceIdentifier
      Remove-Job $eventsubscriber.SourceIdentifier
      } | Out-Null
    }
  }
}
 
#并行执行队列中的任务
for($i=0;$i -lt $MaxJobCount ;$i++)
{
 Run-TaskFromQueue
}