###########################
# ����������
# ��PowerShell���߽̳�ҳ��ץȡ���е�HTMLҳ�棬
# �����ر�������ǰhtml��Ŀ¼��
############################
 
# ȫ������
[int]$MaxJobCount=5
[string]$OutputDir=  (mkdir 'Html' -Force).FullName
 
# ��������
$request=Invoke-WebRequest 'http://www.pstips.net/powershell-online-tutorials.html' -UseBasicParsing
$links = $request.Links | where { $_.href.endswith('.html') } | select -ExpandProperty href
 
#������洢���̰߳�ȫ�Ķ���
$taskQueue = New-Object  'System.Collections.Concurrent.ConcurrentQueue[string]'
$links | foreach {
 $taskQueue.Enqueue($_)
}
 
#�������Ӷ���ִ������
function Run-TaskFromQueue{
 if($taskQueue.Count -gt 0)
 {
  $link=[string]::Empty
  #���ԴӶ����г���һ������
  if($taskQueue.TryDequeue([ref]$link))
  {
     #����һ��Job��ִ������
     $task = Start-Job -ScriptBlock {
        param([uri]$url,$OutputDir)
 
        #���غͱ���ҳ��
        Invoke-RestMethod $url | Out-File "$OutputDir\$($url.Segments[-1])" -Force
     } -ArgumentList $link,$OutputDir
  
     # ע��һ���¼����ģ�����ǰ��������󣬿�ʼִ�ж����е���һ������
     Register-ObjectEvent -InputObject $task -EventName StateChanged -Action {
      Run-TaskFromQueue
      Unregister-Event $eventsubscriber.SourceIdentifier
      Remove-Job $eventsubscriber.SourceIdentifier
      } | Out-Null
    }
  }
}
 
#����ִ�ж����е�����
for($i=0;$i -lt $MaxJobCount ;$i++)
{
 Run-TaskFromQueue
}