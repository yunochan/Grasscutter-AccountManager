async function banAccount() {
    const username = document.getElementById('ban_username').value;
    const isBanned = document.querySelector('input[name="ban_status"]:checked').value;

    // 根据 isBanned 的值设置时间戳
    const fixedBanStartTime = (isBanned === 'true') ? -1313677 : 0;
    const fixedBanEndTime = (isBanned === 'true') ? 1924876800 : 0;

    const response = await fetch('/accounts/ban', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            username: username, 
            isBanned: (isBanned === 'true'),
            banStartTime: fixedBanStartTime,
            banEndTime: fixedBanEndTime
        })
    });

    const result = await response.json();
    if (result.status === 'success') {
        Swal.fire("提交成功", result.message, "success")
    } else {
        Swal.fire("提交失败", result.message || "未知错误", "error")
    }
}
