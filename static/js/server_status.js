async function fetchStatusData() {
    try {
        const response = await fetch('/server/status');
        const data = await response.json();

        if (data.error) {
            console.error('获取数据时出错:', data.error);
            document.getElementById('error_banner').textContent = "无法解析服务器状态信息，请检查格式是否正确。";
            document.getElementById('error_banner').style.display = 'block';
            document.getElementById('player_count').style.display = 'none';
            document.getElementById('server_version').style.display = 'none';
        } else {
            document.getElementById('player_count').textContent = `在线玩家数: ${data.playerCount}`;
            document.getElementById('server_version').textContent = `服务端版本: ${data.version}`;
        }
    } catch (error) {
        console.error('错误:', error);
        document.getElementById('error_banner').textContent = "无法解析服务器状态信息，请检查格式是否正确。";
        document.getElementById('error_banner').style.display = 'block';
        document.getElementById('player_count').style.display = 'none';
        document.getElementById('server_version').style.display = 'none';
    }
}


 // 每1.5秒获取一次数据
 fetchStatusData();
 setInterval(fetchStatusData, 1500);